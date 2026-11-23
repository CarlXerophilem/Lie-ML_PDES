"""Namespaced compatibility entrypoint; prefer importing from symm.LieSymm."""
from .core import *
from .cli import main as cli

if __name__ == "__main__":
    raise SystemExit(cli())
