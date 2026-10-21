"""Explicit evidence archives must preserve bytes and refuse unsafe restores."""
from contextlib import nullcontext
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import zipfile

import pytest

from scripts.evidence_archive import pack, restore, verify


def sample(tmp_path):
    root = tmp_path / 'repo'
    folder = root / 'evidence' / 'old'
    folder.mkdir(parents=True)
    (folder / 'a.bin').write_bytes(b'\x00original\r\nevidence\n\xff')
    (folder / 'b.txt').write_bytes(b'second')
    archive = tmp_path / 'archive.zip'
    names = ['evidence/old/a.bin', 'evidence/old/b.txt']
    return root, folder, archive, names


def write_zip(path, entries, *, extra=None, manifest=None):
    if manifest is None:
        files = {name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                 for name, data in entries}
        manifest = {'schema': 1, 'files': files, 'file_count': len(files),
                    'uncompressed_bytes': sum(item['bytes'] for item in files.values())}
    with zipfile.ZipFile(path, 'w') as target:
        for name, data in entries:
            target.writestr(name, data)
        for name, data in extra or []:
            target.writestr(name, data)
        target.writestr('ARCHIVE_MANIFEST.json', json.dumps(manifest))


def test_exact_explicit_selection_and_deterministic_manifest(tmp_path):
    root, folder, archive, names = sample(tmp_path)
    (folder / 'unselected.txt').write_text('not selected')
    receipt = pack(root, [names[0]], archive)
    manifest = verify(archive, root=root, check_sources=True)
    assert receipt['verified'] is True
    assert manifest['files'] == {
        names[0]: {'bytes': 21, 'sha256': hashlib.sha256((folder / 'a.bin').read_bytes()).hexdigest()}}
    with zipfile.ZipFile(archive) as source:
        assert source.namelist() == [names[0], 'ARCHIVE_MANIFEST.json']
        original_manifest = source.read('ARCHIVE_MANIFEST.json')
    other = tmp_path / 'other.zip'
    pack(root, [names[0]], other)
    with zipfile.ZipFile(other) as source:
        assert source.read('ARCHIVE_MANIFEST.json') == original_manifest


def test_archive_reproducible_regardless_selection_order(tmp_path):
    root, _, archive, names = sample(tmp_path)
    pack(root, names, archive)
    other = tmp_path / 'other.zip'
    pack(root, list(reversed(names)), other)
    assert archive.read_bytes() == other.read_bytes()


def test_pack_does_not_overwrite_archive_or_expand_directories(tmp_path):
    root, _, archive, names = sample(tmp_path)
    archive.write_bytes(b'keep')
    with pytest.raises(ValueError):
        pack(root, names, archive)
    assert archive.read_bytes() == b'keep'
    with pytest.raises(ValueError):
        pack(root, ['evidence/old'], tmp_path / 'directory.zip')


@pytest.mark.parametrize('name', [
    '../escape', 'a/../../escape', '/absolute', 'C:/drive', 'C:drive',
    'a\\backslash', 'a//b', './a', 'a/.', 'a/../b', 'a/', '',
    'a/.git/config', '.git/HEAD', 'a/.GiT/HEAD', 'a/alternate:stream',
    'a/trailing.', 'a/trailing ', 'a/NUL.txt', 'a/control\x01',
    'ARCHIVE_MANIFEST.json',
])
def test_pack_rejects_unsafe_member_names(tmp_path, name):
    root, _, archive, _ = sample(tmp_path)
    with pytest.raises(ValueError):
        pack(root, [name], archive)
    assert not archive.exists()


@pytest.mark.parametrize('names', [
    ['a', 'a'], ['a', 'A'], ['folder/a', 'FOLDER/b'], ['a', 'a/b'],
])
def test_pack_rejects_duplicates_case_aliases_and_file_parents(tmp_path, names):
    root, _, archive, _ = sample(tmp_path)
    with pytest.raises(ValueError):
        pack(root, names, archive)
    assert not archive.exists()


@pytest.mark.parametrize('link_kind', ['file', 'parent', 'root'])
def test_pack_rejects_symlinks_in_every_path_component(tmp_path, link_kind):
    root, folder, archive, names = sample(tmp_path)
    outside = tmp_path / 'outside'
    outside.mkdir()
    (outside / 'data').write_bytes(b'outside')
    try:
        if link_kind == 'file':
            (folder / 'linked').symlink_to(outside / 'data')
            selected = ['evidence/old/linked']
        elif link_kind == 'parent':
            (root / 'linked').symlink_to(outside, target_is_directory=True)
            selected = ['linked/data']
        else:
            linked_root = tmp_path / 'linked-root'
            linked_root.symlink_to(root, target_is_directory=True)
            root = linked_root
            selected = names
    except OSError as error:
        pytest.skip(f'Symlink creation unavailable: {error}')
    with pytest.raises(ValueError):
        pack(root, selected, archive)


@pytest.mark.parametrize('names', [
    ['../escape'], ['nested/.git/HEAD'], ['a', 'A'],
    ['dir/a', 'DIR/b'], ['a', 'a/b'], ['a\\b'],
])
def test_verify_rejects_unsafe_archive_members(tmp_path, names):
    archive = tmp_path / 'bad.zip'
    write_zip(archive, [(name, b'data') for name in names])
    with pytest.raises(ValueError):
        verify(archive)


@pytest.mark.parametrize('defect', ['missing', 'undeclared', 'duplicate', 'hash', 'size'])
def test_verify_rejects_inconsistent_members_and_tampering(tmp_path, defect):
    archive = tmp_path / 'bad.zip'
    manifest = {'schema': 1, 'files': {'data': {'bytes': 4, 'sha256': hashlib.sha256(b'data').hexdigest()}},
                'file_count': 1, 'uncompressed_bytes': 4}
    entries = [] if defect == 'missing' else [('data', b'evil' if defect == 'hash' else b'data')]
    extra = [('other', b'extra')] if defect == 'undeclared' else None
    if defect == 'duplicate':
        extra = [('data', b'data')]
    if defect == 'size':
        manifest['files']['data']['bytes'] = 5
    with pytest.warns(UserWarning) if defect == 'duplicate' else nullcontext():
        write_zip(archive, entries, extra=extra, manifest=manifest)
    with pytest.raises(ValueError):
        verify(archive)


def test_verify_rejects_zip_symlinks(tmp_path):
    archive = tmp_path / 'bad.zip'
    info = zipfile.ZipInfo('linked')
    info.create_system = 3
    info.external_attr = (stat.S_IFLNK | 0o777) << 16
    write_zip(archive, [(info, b'target')], manifest={
        'schema': 1, 'files': {'linked': {'bytes': 6, 'sha256': hashlib.sha256(b'target').hexdigest()}},
        'file_count': 1, 'uncompressed_bytes': 6})
    with pytest.raises(ValueError):
        verify(archive)


def test_verify_rejects_dos_directory_member_even_without_trailing_slash(tmp_path):
    archive = tmp_path / 'directory.zip'
    info = zipfile.ZipInfo('not-a-regular-file')
    info.create_system = 0
    info.external_attr = stat.FILE_ATTRIBUTE_DIRECTORY
    write_zip(archive, [(info, b'data')], manifest={
        'schema': 1, 'files': {info.filename: {'bytes': 4, 'sha256': hashlib.sha256(b'data').hexdigest()}},
        'file_count': 1, 'uncompressed_bytes': 4})
    with pytest.raises(ValueError):
        verify(archive)


def test_check_sources_is_explicit_and_detects_changes(tmp_path):
    root, folder, archive, names = sample(tmp_path)
    pack(root, names, archive)
    (folder / 'a.bin').write_bytes(b'changed')
    verify(archive)
    with pytest.raises(ValueError):
        verify(archive, check_sources=True)
    with pytest.raises(ValueError):
        verify(archive, root=root, check_sources=True)


@pytest.mark.parametrize('conflict', ['bytes', 'parent-file', 'parent-link', 'file-link', 'root-link'])
def test_restore_preflights_entire_selection_without_partial_writes(tmp_path, conflict):
    root, _, archive, names = sample(tmp_path)
    pack(root, names, archive)
    destination = tmp_path / 'destination'
    destination.mkdir()
    if conflict == 'parent-file':
        (destination / 'evidence').write_bytes(b'keep')
    else:
        folder = destination / 'evidence' / 'old'
        folder.mkdir(parents=True)
        if conflict == 'bytes':
            (folder / 'b.txt').write_bytes(b'keep')
        else:
            outside = tmp_path / 'outside'
            outside.mkdir()
            (outside / 'b.txt').write_bytes(b'second')
            try:
                if conflict == 'file-link':
                    (folder / 'b.txt').symlink_to(outside / 'b.txt')
                elif conflict == 'parent-link':
                    names = ['other/a', 'linked/b.txt']
                    archive = tmp_path / 'links.zip'
                    write_zip(archive, [(names[0], b'first'), (names[1], b'second')])
                    (destination / 'linked').symlink_to(outside, target_is_directory=True)
                else:
                    alias = tmp_path / 'destination-alias'
                    alias.symlink_to(destination, target_is_directory=True)
                    destination = alias
            except OSError as error:
                pytest.skip(f'Symlink creation unavailable: {error}')
    with pytest.raises(ValueError):
        restore(archive, destination)
    assert not (destination / names[0]).exists()


def test_restore_preserves_stubs_and_is_idempotent(tmp_path):
    root, folder, archive, names = sample(tmp_path)
    expected = {name: (root / name).read_bytes() for name in names}
    pack(root, names, archive)
    destination = tmp_path / 'destination'
    target = destination / 'evidence' / 'old'
    target.mkdir(parents=True)
    (target / 'ARCHIVED.md').write_bytes(b'preserve this stub')
    restore(archive, destination)
    first = {name: (destination / name).stat().st_mtime_ns for name in names}
    restore(archive, destination)
    assert {name: (destination / name).read_bytes() for name in names} == expected
    assert {name: (destination / name).stat().st_mtime_ns for name in names} == first
    assert (target / 'ARCHIVED.md').read_bytes() == b'preserve this stub'
    verify(archive, root=destination, check_sources=True)


def test_restore_prefix_filters_at_component_boundary(tmp_path):
    archive = tmp_path / 'archive.zip'
    write_zip(archive, [('a/first', b'yes'), ('also/second', b'no')])
    root = tmp_path / 'destination'
    root.mkdir()
    restore(archive, root, prefix='a')
    assert (root / 'a' / 'first').read_bytes() == b'yes'
    assert not (root / 'also').exists()
    with pytest.raises(ValueError):
        restore(archive, root, prefix='../escape')
    with pytest.raises(ValueError):
        restore(archive, root, prefix='absent')


def test_restore_uses_the_same_archive_handle_for_validation_and_copy(tmp_path, monkeypatch):
    archive = tmp_path / 'archive.zip'
    replacement = tmp_path / 'replacement.zip'
    write_zip(archive, [('data', b'original')])
    write_zip(replacement, [('data', b'altered!')])
    destination = tmp_path / 'destination'
    original_zipfile = zipfile.ZipFile
    opens = 0

    class ArchiveChangedOnReopen(original_zipfile):
        def __init__(self, file, mode='r', *args, **kwargs):
            nonlocal opens
            if Path(file) == archive and mode == 'r':
                opens += 1
                if opens == 2:
                    archive.write_bytes(replacement.read_bytes())
            super().__init__(file, mode, *args, **kwargs)

    monkeypatch.setattr(zipfile, 'ZipFile', ArchiveChangedOnReopen)
    restore(archive, destination)
    assert (destination / 'data').read_bytes() == b'original'


@pytest.mark.skipif(os.name != 'nt', reason='Windows junction regression')
@pytest.mark.parametrize('operation', ['pack', 'restore'])
@pytest.mark.parametrize('component', ['root', 'parent'])
def test_junction_components_are_rejected(tmp_path, operation, component):
    real = tmp_path / 'real'
    real.mkdir()
    (real / 'data').write_bytes(b'data')
    link = tmp_path / 'junction'
    command = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(real)],
                             capture_output=True, text=True)
    assert command.returncode == 0, command.stderr
    root = link if component == 'root' else tmp_path
    name = 'data' if component == 'root' else 'junction/data'
    archive = tmp_path / 'archive.zip'
    if operation == 'restore':
        write_zip(archive, [(name, b'data')])
    with pytest.raises(ValueError):
        if operation == 'pack':
            pack(root, [name], archive)
        else:
            restore(archive, root)


def test_cli_pack_verify_restore_and_receipt(tmp_path):
    root, _, archive, names = sample(tmp_path)
    selection = tmp_path / 'files.json'
    selection.write_text(json.dumps(names), encoding='utf-8')
    receipt = tmp_path / 'receipt.json'
    script = Path(__file__).resolve().parents[1] / 'evidence_archive.py'
    result = subprocess.run([sys.executable, str(script), 'pack', '--root', str(root),
                             '--files', str(selection), '--archive', str(archive),
                             '--receipt', str(receipt)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(receipt.read_text(encoding='utf-8'))['verified'] is True
    result = subprocess.run([sys.executable, str(script), 'verify', '--root', str(root),
                             '--archive', str(archive), '--check-sources'], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    destination = tmp_path / 'destination'
    destination.mkdir()
    result = subprocess.run([sys.executable, str(script), 'restore', '--root', str(destination),
                             '--archive', str(archive), '--prefix', 'evidence/old'], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (destination / names[0]).read_bytes() == (root / names[0]).read_bytes()
