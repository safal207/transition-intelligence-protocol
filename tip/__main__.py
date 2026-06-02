"""Command-line interface for Transition Intelligence Protocol."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tip.validator import DEFAULT_SCHEMA_PATH, validate_target


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tip",
        description="Transition Intelligence Protocol command-line tools.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate one TIP record or a directory of .tip.json records.",
    )
    validate_parser.add_argument(
        "target",
        type=Path,
        help="Path to a .tip.json file or a directory containing .tip.json files.",
    )
    validate_parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA_PATH,
        help="Path to the TIP record JSON schema.",
    )

    return parser


def run_validate(target: Path, schema: Path) -> int:
    try:
        results = validate_target(target, schema)
    except FileNotFoundError as exc:
        print(f"FAIL {exc}")
        return 1

    failed = False
    for result in results:
        if result.ok:
            print(f"OK   {result.path}")
            continue

        failed = True
        print(f"FAIL {result.path}")
        for error in result.errors:
            print(f"  - {error}")

    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        return run_validate(args.target, args.schema)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
