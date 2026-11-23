"""Hash-verified build archives with guarded pruning and non-overwriting restore."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[1]


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def safe_build_path(root,name):
    path=PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or len(path.parts)<2 or path.parts[0]!='build':
        raise ValueError('Archive member must be under build/: '+name)
    target=(Path(root)/name).resolve()
    base=(Path(root)/'build').resolve()
    if not target.is_relative_to(base) or target==base:
        raise ValueError('Archive path escaped the build directory')
    return target


def inventory(root,directories):
    root=Path(root).resolve();build=(root/'build').resolve();files={}
    if len(directories)!=len(set(directories)):
        raise ValueError('Duplicate build directory')
    seen_paths=set()
    for directory in directories:
        raw=build/directory
        if raw.parent!=build or raw.is_symlink() or raw.is_junction():
            raise ValueError('Expected an unlinked direct build child: '+str(raw))
        path=raw.resolve()
        if path.parent!=build or not path.is_dir():
            raise ValueError('Expected an existing direct build child: '+str(path))
        if path in seen_paths:
            raise ValueError('Duplicate resolved build directory: '+str(path))
        seen_paths.add(path)
        if (path/'.git').exists():
            raise ValueError('A Git checkout is not disposable build output')
        for item in sorted(path.rglob('*')):
            if item.is_symlink() or item.is_junction():
                raise ValueError('Refusing linked build entries: '+str(item))
            if item.name=='.git':
                raise ValueError('Nested Git checkout: '+str(item))
            if item.is_file():
                rel=item.relative_to(root).as_posix()
                files[rel]={'sha256':sha(item),'bytes':item.stat().st_size}
    return files


def pack(root,directories,archive):
    root=Path(root).resolve();archive=Path(archive).resolve()
    if archive.exists():raise ValueError('Do not overwrite an archive')
    if archive.is_relative_to((root/'build').resolve()):
        raise ValueError('Archive must be outside the tree being archived')
    files=inventory(root,directories)
    if not files:raise ValueError('No files to archive')
    manifest={'schema':1,'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
              'original_root':str(root),'directories':list(directories),'files':files,
              'file_count':len(files),'uncompressed_bytes':sum(x['bytes'] for x in files.values())}
    archive.parent.mkdir(parents=True,exist_ok=True)
    temporary=archive.with_suffix(archive.suffix+'.partial')
    if temporary.exists():raise ValueError('Preserve/investigate existing partial archive')
    with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
        for name in files:z.write(root/name,name)
        z.writestr('ARCHIVE_MANIFEST.json',json.dumps(manifest,indent=2,ensure_ascii=False))
    verify(temporary,root=root,check_sources=True)
    temporary.rename(archive)
    return {**manifest,'archive':str(archive),'archive_sha256':sha(archive),
            'archive_bytes':archive.stat().st_size,'verified':True}


def verify(archive,*,root=ROOT,check_sources=False):
    with zipfile.ZipFile(archive) as z:
        manifest=json.loads(z.read('ARCHIVE_MANIFEST.json'))
        names=z.namelist()
        if len(names)!=len(set(names)) or set(names)!=set(manifest['files'])|{'ARCHIVE_MANIFEST.json'}:
            raise ValueError('Duplicate, missing or undeclared archive member')
        for name,item in manifest['files'].items():
            target=safe_build_path(root,name)
            with z.open(name) as stream:
                actual=hashlib.file_digest(stream,'sha256').hexdigest()
            if actual!=item['sha256'] or z.getinfo(name).file_size!=item['bytes']:
                raise ValueError('Archive integrity failure: '+name)
            if check_sources and (not target.is_file() or sha(target)!=item['sha256']):
                raise ValueError('Source changed since archiving: '+name)
        if manifest['file_count']!=len(manifest['files']):raise ValueError('Manifest count mismatch')
    return manifest


def prune(archive,*,root=ROOT):
    root=Path(root).resolve()
    manifest=verify(archive,root=root,check_sources=True)
    # Re-inventory detects new files as well as changed bytes before deletion.
    if inventory(root,manifest['directories'])!=manifest['files']:
        raise ValueError('Directory contents changed; refuse pruning')
    paths=[safe_build_path(root,'build/'+name) for name in manifest['directories']]
    for path in paths:
        if path.parent!=(root/'build').resolve():raise ValueError('Prune target is not a direct build child')
    print(json.dumps({'verified_prune_targets':[str(p) for p in paths]},indent=2),flush=True)
    for path in paths:shutil.rmtree(path)
    return {'pruned_directories':manifest['directories'],'archive_sha256':sha(archive)}


def restore(archive,*,root=ROOT,directory=None):
    root=Path(root).resolve();manifest=verify(archive,root=root)
    if directory is not None and directory not in manifest['directories']:
        raise ValueError('Directory is not in this archive')
    selected={k:v for k,v in manifest['files'].items()
              if directory is None or PurePosixPath(k).parts[1]==directory}
    for name,item in selected.items():
        target=safe_build_path(root,name)
        if target.exists() and (not target.is_file() or sha(target)!=item['sha256']):
            raise ValueError('Refuse to overwrite different bytes: '+name)
    with zipfile.ZipFile(archive) as z:
        for name,item in selected.items():
            target=safe_build_path(root,name)
            if target.exists():continue
            target.parent.mkdir(parents=True,exist_ok=True)
            with z.open(name) as src,target.open('xb') as dst:shutil.copyfileobj(src,dst)
            if sha(target)!=item['sha256']:raise ValueError('Restored hash mismatch')
    return {'restored_files':len(selected),'directory':directory}


def old_directories(root,cutoff,keep):
    boundary=dt.datetime.fromisoformat(cutoff).timestamp();result=[]
    for path in sorted((Path(root)/'build').iterdir()):
        if not path.is_dir() or path.name in keep:continue
        times=[p.stat().st_mtime for p in path.rglob('*') if p.is_file()]
        if times and max(times)<boundary:result.append(path.name)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation',choices=('pack-old','pack','verify','restore','prune'))
    parser.add_argument('--archive',type=Path,required=True)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--cutoff',default='2026-10-19')
    parser.add_argument('--keep',nargs='*',default=['week-4'])
    parser.add_argument('--directories',nargs='+')
    parser.add_argument('--directory')
    parser.add_argument('--receipt',type=Path)
    args=parser.parse_args()
    if args.operation in ('pack','pack-old'):
        directories=args.directories if args.operation=='pack' else old_directories(args.root,args.cutoff,args.keep)
        if not directories:parser.error('No selected build directories')
        result=pack(args.root,directories,args.archive)
    elif args.operation=='verify':result=verify(args.archive,root=args.root)
    elif args.operation=='prune':result=prune(args.archive,root=args.root)
    else:result=restore(args.archive,root=args.root,directory=args.directory)
    if args.receipt:
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2,ensure_ascii=False))


if __name__=='__main__':main()
