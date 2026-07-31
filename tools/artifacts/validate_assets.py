#!/usr/bin/env python3
"""Compatibility entry point for v0.2 asset and release validation."""

from __future__ import annotations

try:
    from .validate import main
except ImportError:  # pragma: no cover - direct script execution
    from validate import main


if __name__ == "__main__":
    raise SystemExit(main())
