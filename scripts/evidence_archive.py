"""Explicit-file, hash-verified evidence ZIPs; no deletion or pruning commands."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'ARCHIVE_MANIFEST.json'
_RESERVED = {'CON', 'PRN', 'AUX', 'NUL'} | {
    stem + str(number) for stem in ('COM', 'LPT') for number in range(1, 10)}


def _name(name):
    if not isinstance(name, str) or not name or '\\' in name:
        raise ValueError('Expected an exact slash-separated relative filename')
    parts = name.split('/')
    for part in parts:
        if (not part or part in ('.', '..') or part.casefold() == '.git'
                or part.endswith((' ', '.')) or part.split('.')[0].upper() in _RESERVED
                or any(ord(char) < 32 or ord(char) == 127 or char in ':*?<>|"' for char in part)):
            raise ValueError('Unsafe archive path: ' + repr(name))
    if parts[0].casefold() == MANIFEST.casefold():
        raise ValueError('Reserved manifest path: ' + name)
    return name


def _names(names):
    seen = set()
    prefixes = {}
    for name in names:
        _name(name)
        if name in seen:
            raise ValueError('Duplicate archive path: ' + name)
        seen.add(name)
        parts = name.split('/')
        for length in range(1, len(parts) + 1):
            prefix = '/'.join(parts[:length])
            key = prefix.casefold()
            if key in prefixes and prefixes[key] != prefix:
                raise ValueError('Case-colliding archive paths: ' + prefix)
            prefixes[key] = prefix
    for name in seen:
        if any('/'.join(name.split('/')[:length]) in seen
               for length in range(1, len(name.split('/')))):
            raise ValueError('A file is also an archive parent: ' + name)


def _path(path, *, directory=False, missing=False):
    """Inspect the root and every existing ancestor without resolving links."""
    path = Path(path).absolute()
    for item in reversed((path, *path.parents)):
        try:
            info = item.lstat()
        except FileNotFoundError:
            if not missing:
                raise ValueError('Missing path: ' + str(item)) from None
            continue
        if (stat.S_ISLNK(info.st_mode)
                or getattr(info, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT):
            raise ValueError('Refusing linked path component: ' + str(item))
        expected_directory = item != path or directory
        if not (stat.S_ISDIR(info.st_mode) if expected_directory else stat.S_ISREG(info.st_mode)):
            raise ValueError('Expected a regular file or directory: ' + str(item))
    return path


def _sha(path):
    with Path(path).open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def _json_object(pairs):
    result = {}
    for name, value in pairs:
        if name in result:
            raise ValueError('Duplicate JSON key: ' + name)
        result[name] = value
    return result


def _manifest(value):
    if not isinstance(value, dict) or set(value) != {
            'schema', 'files', 'file_count', 'uncompressed_bytes'}:
        raise ValueError('Invalid schema-1 manifest fields')
    files = value['files']
    if type(value['schema']) is not int or value['schema'] != 1 or not isinstance(files, dict) or not files:
        raise ValueError('Expected nonempty schema-1 manifest')
    _names(files)
    for name, item in files.items():
        if (not isinstance(item, dict) or set(item) != {'bytes', 'sha256'}
                or type(item['bytes']) is not int or item['bytes'] < 0
                or not isinstance(item['sha256'], str)
                or not re.fullmatch('[0-9a-f]{64}', item['sha256'])):
            raise ValueError('Invalid file metadata: ' + name)
    if (type(value['file_count']) is not int or value['file_count'] != len(files)
            or type(value['uncompressed_bytes']) is not int
            or value['uncompressed_bytes'] != sum(item['bytes'] for item in files.values())):
        raise ValueError('Manifest count or byte total mismatch')
    return value


def _inspect(source):
    infos = source.infolist()
    names = [info.filename for info in infos]
    if len(names) != len(set(names)) or names.count(MANIFEST) != 1:
        raise ValueError('Duplicate or missing manifest/archive member')
    for info in infos:
        mode = info.external_attr >> 16
        if (info.orig_filename != info.filename or info.is_dir()
                or stat.S_IFMT(mode) not in (0, stat.S_IFREG)
                or info.external_attr & (stat.FILE_ATTRIBUTE_REPARSE_POINT | stat.FILE_ATTRIBUTE_DIRECTORY)):
            raise ValueError('Nonregular or linked ZIP member: ' + repr(info.filename))
    try:
        manifest = _manifest(json.loads(source.read(MANIFEST), object_pairs_hook=_json_object))
    except (UnicodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise ValueError('Invalid archive manifest') from error
    if set(names) != set(manifest['files']) | {MANIFEST}:
        raise ValueError('Missing or undeclared archive member')
    for name, item in manifest['files'].items():
        with source.open(name) as stream:
            actual = hashlib.file_digest(stream, 'sha256').hexdigest()
        if source.getinfo(name).file_size != item['bytes'] or actual != item['sha256']:
            raise ValueError('Archive integrity failure: ' + name)
    return manifest


def pack(root, files: list[str], archive):
    """Archive only the explicitly selected regular files and return a receipt."""
    if not isinstance(files, list) or not files:
        raise ValueError('Expected a nonempty list of exact filenames')
    _names(files)
    root = _path(root, directory=True)
    archive = _path(archive, missing=True)
    if archive.exists():
        raise ValueError('Do not overwrite an archive: ' + str(archive))
    temporary = _path(archive.with_name(archive.name + '.partial'), missing=True)
    if temporary.exists():
        raise ValueError('Preserve/investigate existing partial archive: ' + str(temporary))
    entries = {}
    for name in sorted(files):
        path = _path(root / name)
        entries[name] = {'bytes': path.stat().st_size, 'sha256': _sha(path)}
    manifest = {'schema': 1, 'files': entries, 'file_count': len(entries),
                'uncompressed_bytes': sum(item['bytes'] for item in entries.values())}
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(temporary, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as target:
        for name in [*entries, MANIFEST]:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o600) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            with target.open(info, 'w', force_zip64=True) as destination:
                if name == MANIFEST:
                    destination.write(json.dumps(manifest, sort_keys=True, ensure_ascii=False,
                                                 indent=2).encode('utf-8') + b'\n')
                else:
                    with _path(root / name).open('rb') as source:
                        shutil.copyfileobj(source, destination)
    verify(temporary, root=root, check_sources=True)
    # A hard-link publication cannot overwrite a concurrently created archive.
    os.link(temporary, archive)
    temporary.unlink()
    return {**manifest, 'archive': str(archive), 'archive_sha256': _sha(archive),
            'archive_bytes': archive.stat().st_size, 'verified': True}


def verify(archive, root=None, check_sources=False):
    """Verify every ZIP member; optionally compare all original source files."""
    archive = _path(archive)
    if check_sources and root is None:
        raise ValueError('Source verification requires an explicit root')
    if root is not None:
        root = _path(root, directory=True)
    try:
        with zipfile.ZipFile(archive) as source:
            manifest = _inspect(source)
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError) as error:
        raise ValueError('Invalid or corrupt ZIP archive') from error
    if check_sources:
        for name, item in manifest['files'].items():
            path = _path(root / name)
            if path.stat().st_size != item['bytes'] or _sha(path) != item['sha256']:
                raise ValueError('Source changed since archiving: ' + name)
    return manifest


def restore(archive, root, prefix=None):
    """Restore original paths after preflighting every selected destination."""
    root = _path(root, directory=True, missing=True)
    if prefix is not None:
        _name(prefix)
    try:
        with zipfile.ZipFile(_path(archive)) as source:
            manifest = _inspect(source)
            selected = {name: item for name, item in manifest['files'].items()
                        if prefix is None or name == prefix or name.startswith(prefix + '/')}
            if not selected:
                raise ValueError('Prefix does not select any archive files')
            existing = set()
            for name, item in selected.items():
                path = _path(root / name, missing=True)
                if path.exists():
                    if path.stat().st_size != item['bytes'] or _sha(path) != item['sha256']:
                        raise ValueError('Refuse to overwrite different bytes: ' + name)
                    existing.add(name)
            for name, item in selected.items():
                if name in existing:
                    continue
                path = _path(root / name, missing=True)
                path.parent.mkdir(parents=True, exist_ok=True)
                with source.open(name) as src, path.open('xb') as dst:
                    shutil.copyfileobj(src, dst)
                if path.stat().st_size != item['bytes'] or _sha(path) != item['sha256']:
                    raise ValueError('Restored integrity failure: ' + name)
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError) as error:
        raise ValueError('Invalid or corrupt ZIP archive') from error
    return {'restored_files': len(selected) - len(existing), 'unchanged_files': len(existing),
            'selected_files': len(selected), 'prefix': prefix, 'verified': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('pack', 'verify', 'restore'))
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--root', type=Path)
    parser.add_argument('--files', type=Path, help='JSON list of exact repository-relative filenames')
    parser.add_argument('--prefix', help='Restore only this exact path or directory prefix')
    parser.add_argument('--check-sources', action='store_true')
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    try:
        if args.operation == 'pack':
            if args.root is None or args.files is None:
                parser.error('pack requires --root and --files')
            result = pack(args.root, json.loads(args.files.read_text(encoding='utf-8-sig')), args.archive)
        elif args.operation == 'verify':
            result = verify(args.archive, root=args.root, check_sources=args.check_sources)
        else:
            result = restore(args.archive, root=args.root or ROOT, prefix=args.prefix)
        if args.receipt:
            receipt = _path(args.receipt, missing=True)
            receipt.parent.mkdir(parents=True, exist_ok=True)
            with receipt.open('x', encoding='utf-8', newline='\n') as stream:
                stream.write(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
