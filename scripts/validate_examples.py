#!/usr/bin/env python3
"""Validate TIP JSON examples against the canonical schema.

Usage:
    python scripts/validate_examples.py
    python -m tip validate examples/json/
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tip.__main__ import main as tip_main


if __name__ == "__main__":
    sys.exit(tip_main(["validate", str(ROOT / "examples" / "json")]))
