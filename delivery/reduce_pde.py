#!/usr/bin/env python3
"""Compatibility entry point. New installations can use `lie-reduce`."""
from lie_reduce.cli import load_pde_spec, run_pipeline, main

if __name__ == "__main__":
    raise SystemExit(main())
