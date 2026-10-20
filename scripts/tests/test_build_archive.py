"""Cleanup cannot discard changed/unrecorded bytes or escape build/."""
from pathlib import Path
import pytest
from scripts.build_archive import pack,prune,restore,verify,safe_build_path


def sample(tmp_path):
    root=tmp_path/'repo';d=root/'build'/'old';d.mkdir(parents=True)
    (d/'evidence.txt').write_bytes(b'original\r\nevidence\n')
    archive=tmp_path/'archive.zip'
    pack(root,['old'],archive)
    return root,d,archive


def test_verified_roundtrip(tmp_path):
    root,d,z=sample(tmp_path)
    prune(z,root=root)
    assert not d.exists()
    restore(z,root=root,directory='old')
    assert (d/'evidence.txt').read_bytes()==b'original\r\nevidence\n'
    verify(z,root=root,check_sources=True)


@pytest.mark.parametrize('change',['modified','new'])
def test_prune_refuses_any_post_archive_change(tmp_path,change):
    root,d,z=sample(tmp_path)
    (d/('evidence.txt' if change=='modified' else 'new.txt')).write_text('new work')
    with pytest.raises(ValueError):prune(z,root=root)
    assert d.exists()


def test_restore_refuses_overwrite(tmp_path):
    root,d,z=sample(tmp_path)
    (d/'evidence.txt').write_text('user edit')
    with pytest.raises(ValueError):restore(z,root=root)
    assert (d/'evidence.txt').read_text()=='user edit'


@pytest.mark.parametrize('name',['../docs/x','build/../../outside','/build/old/x','docs/a','build'])
def test_member_path_boundary(tmp_path,name):
    with pytest.raises(ValueError):safe_build_path(tmp_path,name)


def test_top_level_alias_cannot_select_another_directory(tmp_path):
    root=tmp_path/'repo';target=root/'build'/'keep';target.mkdir(parents=True)
    (target/'evidence').write_text('keep')
    alias=root/'build'/'old'
    alias.symlink_to(target,target_is_directory=True)
    with pytest.raises(ValueError):pack(root,['old'],tmp_path/'archive.zip')
    assert (target/'evidence').read_text()=='keep'


@pytest.mark.parametrize("duplicate", ["old", "old/.", "OLD"])
def test_duplicate_prune_selection_is_rejected(tmp_path,duplicate):
    root=tmp_path/'repo';target=root/'build'/'old';target.mkdir(parents=True)
    (target/'data').write_text('data')
    with pytest.raises(ValueError):pack(root,['old',duplicate],tmp_path/'archive.zip')
