"""Load byte-pinned historical code with module-local sibling imports.

No changes to sys.path, sys.meta_path, builtins.__import__, or bare module names.
The only runtime patch is the documented separator-safe gate hash checker.
"""
from __future__ import annotations

import builtins
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import sys
import threading
import types

PACKAGE_ROOT = Path(__file__).resolve().parent
SNAPSHOT_ROOT = PACKAGE_ROOT / "_snapshot"
RUNTIME_PREFIX = __package__ + "._runtime"
_LOCK = threading.RLock()
_MANIFEST = json.loads((PACKAGE_ROOT / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
_MODULES = {PurePosixPath(name).stem for name in _MANIFEST["files"]
            if "/" not in name and name.endswith(".py")}


def snapshot_path(name, *, root=SNAPSHOT_ROOT):
    """Resolve a relative POSIX/Windows receipt key without accepting escape."""
    root = Path(root).resolve()
    name = str(name).replace("\\", "/")
    relative = PurePosixPath(name)
    if relative.is_absolute() or ":" in name or ".." in relative.parts:
        raise ValueError("Snapshot names must be relative and cannot escape the snapshot")
    path = root.joinpath(*relative.parts).resolve()
    if not path.is_relative_to(root):
        raise ValueError("Snapshot path escapes its root")
    return path


def _check_hashes(hashes, root=None):
    """Same byte comparison as the frozen checker, with portable key parsing."""
    root = SNAPSHOT_ROOT if root is None else root
    changed = []
    for name, expected in hashes.items():
        try:
            path = snapshot_path(name, root=root)
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                changed.append(name)
        except (ValueError, OSError):
            changed.append(name)
    return changed


def _scoped_import(name, globals=None, locals=None, fromlist=(), level=0):
    if level == 0 and name in _MODULES:
        return load_module(name)
    return builtins.__import__(name, globals, locals, fromlist, level)


def load_module(name):
    """Private implementation loader; mutation/runner APIs are not public."""
    if name not in _MODULES:
        raise ImportError(f"Unknown frozen LieSymm module: {name}")
    fullname = RUNTIME_PREFIX + "." + name
    with _LOCK:
        if fullname in sys.modules:
            return sys.modules[fullname]
        if RUNTIME_PREFIX not in sys.modules:
            package = types.ModuleType(RUNTIME_PREFIX)
            package.__path__ = []
            package.__package__ = RUNTIME_PREFIX
            package.__spec__ = importlib.util.spec_from_loader(RUNTIME_PREFIX, loader=None, is_package=True)
            sys.modules[RUNTIME_PREFIX] = package
        path = snapshot_path(name + ".py")
        content = path.read_bytes()
        expected = _MANIFEST["files"][name + ".py"]["sha256"]
        if hashlib.sha256(content).hexdigest() != expected:
            raise ImportError(f"Frozen source hash mismatch: {name}.py")
        spec = importlib.util.spec_from_file_location(fullname, path)
        module = importlib.util.module_from_spec(spec)
        module.__builtins__ = dict(vars(builtins), __import__=_scoped_import)
        sys.modules[fullname] = module
        try:
            exec(compile(content, str(path), "exec"), module.__dict__)
            if name == "gatekeeper":
                module.check_hashes = _check_hashes
            module.__liesymm_import_adapter__ = "module-local sibling import v1"
        except BaseException:
            sys.modules.pop(fullname, None)
            raise
        return module
