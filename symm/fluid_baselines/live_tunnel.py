"""Reconnect the private priestess simulation tunnel on this Windows machine.

python -B -m symm.fluid_baselines.live_tunnel --background
python -B -m symm.fluid_baselines.live_tunnel --stop
This supervisor does not install a Windows login task or modify SSH credentials.
"""
import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--background",action="store_true")
    parser.add_argument("--stop",action="store_true")
    parser.add_argument("--port",type=int,default=8879)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[2]
    directory=root/"research_artifacts"/"live-simulation-20260925"/"tunnel"
    directory.mkdir(parents=True,exist_ok=True)
    stop=directory/"stop.request"
    if args.stop:
        stop.write_text("stop\n",encoding="utf-8")
        print("Requested tunnel shutdown.");return
    if args.background:
        with socket.socket() as probe:
            probe.bind(("127.0.0.1",args.port))
        if stop.exists():stop.unlink()
        log=(directory/"supervisor.log").open("a",encoding="utf-8")
        process=subprocess.Popen([sys.executable,"-B",str(Path(__file__).resolve()),"--port",str(args.port)],
                                 stdin=subprocess.DEVNULL,stdout=log,stderr=log,cwd=root,
                                 creationflags=subprocess.CREATE_NO_WINDOW if os.name=="nt" else 0)
        print(json.dumps({"supervisor_pid":process.pid,"url":f"http://127.0.0.1:{args.port}/","directory":str(directory)}))
        return
    delay=1
    while not stop.exists():
        command=["ssh","-N","-o","BatchMode=yes","-o","ConnectTimeout=10",
                 "-o","ExitOnForwardFailure=yes","-o","ServerAliveInterval=15",
                 "-o","ServerAliveCountMax=3","-L",f"127.0.0.1:{args.port}:127.0.0.1:8879","priestess"]
        with (directory/"ssh.log").open("a",encoding="utf-8") as log:
            child=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=log,stderr=log,
                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name=="nt" else 0)
            (directory/"processes.json").write_text(json.dumps({"supervisor_pid":os.getpid(),"ssh_pid":child.pid,
                "port":args.port,"host":"priestess","started_epoch":time.time()},indent=2)+"\n",encoding="utf-8")
            started=time.monotonic()
            try:
                while child.poll() is None and not stop.exists():time.sleep(1)
            finally:
                if child.poll() is None:
                    child.terminate()
                    try:child.wait(timeout=5)
                    except subprocess.TimeoutExpired:child.kill();child.wait()
        if time.monotonic()-started>30:delay=1
        until=time.monotonic()+delay
        while not stop.exists() and time.monotonic()<until:time.sleep(.5)
        delay=min(delay*2,30)


if __name__=="__main__":main()
