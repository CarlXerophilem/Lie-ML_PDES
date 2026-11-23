"""Serial Linux node runner using /proc and wait4; no psutil substitutions.

Sampling cannot recover threads that exit between observations. Accordingly
parallel mode is unavailable and thread accounting is explicitly incomplete.
This is an operational receipt, never a mathematical acceptance certificate.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import time


def save(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def available_memory():
    for line in Path('/proc/meminfo').read_text().splitlines():
        if line.startswith('MemAvailable:'):
            return int(line.split()[1]) * 1024
    raise RuntimeError('MemAvailable unavailable')


def group_absent(pid):
    try:
        os.killpg(pid, 0)
    except ProcessLookupError:
        return True
    except PermissionError:
        return False
    return False


def kill_owned_group(pid):
    try:
        os.killpg(pid,signal.SIGKILL)
    except ProcessLookupError:
        # The owned child may not have reached setsid yet. Kill the child
        # itself rather than blocking forever waiting for its later exec.
        try:
            os.kill(pid,signal.SIGKILL)
        except ProcessLookupError:
            pass


def snapshot(root):
    queue, seen, rows = [root], set(), []
    while queue:
        pid = queue.pop()
        if pid in seen:
            continue
        seen.add(pid)
        try:
            base = Path('/proc') / str(pid)
            stat = (base / 'stat').read_text().rsplit(')', 1)[1].split()
            # Fields after comm start at field 3 (state).
            process = dict(pid=pid, ppid=int(stat[1]), start_ticks=int(stat[19]),
                           user_ticks=int(stat[11]), system_ticks=int(stat[12]),
                           rss_bytes=int(stat[21]) * os.sysconf('SC_PAGE_SIZE'), threads=[])
            for task in (base / 'task').iterdir():
                try:
                    tid = int(task.name)
                    fields = (task / 'stat').read_text().rsplit(')', 1)[1].split()
                    sched = (task / 'schedstat').read_text().split()
                    process['threads'].append(dict(tid=tid, user_ticks=int(fields[11]),
                        system_ticks=int(fields[12]), runtime_ns=int(sched[0]),
                        affinity=sorted(os.sched_getaffinity(tid)), last_cpu=int(fields[36])))
                    queue.extend(int(p) for p in (task / 'children').read_text().split())
                except (FileNotFoundError, ProcessLookupError):
                    pass
            rows.append(process)
        except (FileNotFoundError, ProcessLookupError):
            pass
    return rows


def run_node(campaign, name, argv, *, timeout=1800, cwd=None):
    if not argv or not 0 < timeout <= 1800:
        raise ValueError('An argv and node limit in (0,1800] seconds are required')
    if Path(name).name != name or name in ('', '.', '..'):
        raise ValueError('Node name must be one path component')
    campaign = Path(campaign).resolve()
    campaign.mkdir(parents=True, exist_ok=True)
    # The lock serializes verification and computation alike in this campaign.
    with (campaign / 'serial.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        config_path = campaign / 'campaign.json'
        if config_path.exists():
            config = json.loads(config_path.read_text())
        else:
            config = dict(start_monotonic=time.monotonic(),
                          boot_id=Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
                          start_utc=datetime.now(timezone.utc).isoformat(),
                          memory_budget_bytes=min(4 * 1024**3, available_memory() - 2 * 1024**3),
                          parallel_enabled=False)
            save(config_path, config)
        if config['boot_id'] != Path('/proc/sys/kernel/random/boot_id').read_text().strip():
            raise RuntimeError('Campaign cannot resume across a reboot')
        config['memory_budget_bytes'] = min(config['memory_budget_bytes'], 4 * 1024**3)
        if config.get('cleanup_unconfirmed'):
            raise RuntimeError('Previous process group cleanup is unconfirmed')
        elapsed = time.monotonic() - config['start_monotonic']
        if elapsed >= 110 * 60:
            raise RuntimeError('No new node after minute 110')
        if config['memory_budget_bytes'] <= 0:
            raise RuntimeError('Insufficient controller memory reserve')
        node = campaign / name
        node.mkdir(exist_ok=False)
        started = time.monotonic()
        limit = min(timeout, 115 * 60 - elapsed)
        cpus = sorted(os.sched_getaffinity(0))[:1]
        receipt = dict(argv=argv, cwd=str(Path(cwd or os.getcwd()).resolve()),
                       runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                       start_utc=datetime.now(timezone.utc).isoformat(),
                       timeout_seconds=limit, cpu_affinity=cpus,
                       memory_budget_bytes=config['memory_budget_bytes'],
                       clock_ticks_per_second=os.sysconf('SC_CLK_TCK'),
                       poll_interval_seconds=0.05, thread_accounting_complete=False,
                       parallel_enabled=False, mathematical_acceptance=False)
        with (node / 'stdout.log').open('xb') as out, (node / 'stderr.log').open('xb') as err, \
                (node / 'samples.jsonl').open('x') as samples:
            pid = os.fork()
            if pid == 0:
                try:
                    os.setsid()
                    os.sched_setaffinity(0, cpus)
                    os.chdir(receipt['cwd'])
                    os.dup2(out.fileno(), 1)
                    os.dup2(err.fileno(), 2)
                    os.execvp(argv[0], argv)
                except BaseException as exc:
                    os.write(2, (str(exc) + '\n').encode())
                    os._exit(127)
            receipt['pid'] = pid
            peak, reason = 0, 'exited'
            try:
                while True:
                    rows = snapshot(pid)
                    rss = sum(row['rss_bytes'] for row in rows)
                    peak = max(peak, rss)
                    samples.write(json.dumps(dict(elapsed=time.monotonic()-started, processes=rows))+'\n')
                    done, status, usage = os.wait4(pid, os.WNOHANG)
                    if done:
                        break
                    if time.monotonic()-started >= limit:
                        reason = 'timeout'
                    elif rss > config['memory_budget_bytes']:
                        reason = 'memory-limit'
                    elif os.fstat(out.fileno()).st_size + os.fstat(err.fileno()).st_size > 8_000_000:
                        reason = 'output-limit'
                    if reason != 'exited':
                        kill_owned_group(pid)
                        _, status, usage = os.wait4(pid, 0)
                        break
                    time.sleep(0.05)
            except BaseException as interrupted:
                kill_error=None
                try:
                    kill_owned_group(pid)
                except OSError as exc:
                    kill_error=str(exc)
                try:
                    done,status,usage=os.wait4(pid,os.WNOHANG if kill_error else 0)
                except ChildProcessError:
                    done,status,usage=0,0,None
                config['cleanup_unconfirmed'] = not group_absent(pid)
                save(config_path, config)
                receipt.update(exit_reason='controller-interrupted',error=repr(interrupted),
                    kill_error=kill_error,elapsed_seconds=time.monotonic()-started,
                    cleanup_confirmed=not config['cleanup_unconfirmed'],
                    returncode=os.waitstatus_to_exitcode(status) if done else None,
                    user_seconds=usage.ru_utime if usage else None,
                    system_seconds=usage.ru_stime if usage else None,
                    wait4_maxrss_bytes=usage.ru_maxrss*1024 if usage else None,
                    sampled_tree_peak_rss_bytes=peak,
                    stdout_bytes=os.fstat(out.fileno()).st_size,
                    stderr_bytes=os.fstat(err.fileno()).st_size,
                    output_complete=False,exit_accounting_complete=bool(done))
                save(node/'receipt.json',receipt)
                raise
            # An exiting leader is not evidence that its descendants exited.
            absent = group_absent(pid)
            if not absent:
                kill_owned_group(pid)
                absent = group_absent(pid)
            config['cleanup_unconfirmed'] = not absent
            save(config_path, config)
            sizes = dict(stdout_bytes=os.fstat(out.fileno()).st_size,
                         stderr_bytes=os.fstat(err.fileno()).st_size)
            if sum(sizes.values()) > 8_000_000:
                reason = 'output-limit'
            receipt.update(sizes, exit_reason=reason, returncode=os.waitstatus_to_exitcode(status),
                           elapsed_seconds=time.monotonic()-started,
                           user_seconds=usage.ru_utime, system_seconds=usage.ru_stime,
                           wait4_maxrss_bytes=usage.ru_maxrss * 1024,
                           sampled_tree_peak_rss_bytes=peak,
                           cleanup_confirmed=absent, output_complete=sum(sizes.values()) <= 8_000_000,
                           limitations=['Per-thread lifetimes and CPU migration between polls are not observed',
                                        'wait4 CPU totals include only descendants waited for by their parent',
                                        'RSS sum is sampled and can count shared pages more than once'])
            save(node / 'receipt.json', receipt)
        return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--campaign', type=Path, required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--timeout', type=float, default=1800)
    parser.add_argument('argv', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = args.argv[1:] if args.argv[:1] == ['--'] else args.argv
    receipt = run_node(args.campaign, args.name, argv, timeout=args.timeout)
    print(json.dumps(receipt, indent=2))
    return 0 if (receipt['returncode'] == 0 and receipt['exit_reason'] == 'exited'
                 and receipt['cleanup_confirmed'] and receipt['output_complete']) else 1


if __name__ == '__main__':
    raise SystemExit(main())
