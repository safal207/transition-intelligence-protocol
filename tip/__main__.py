"""Command-line interface for Transition Intelligence Protocol."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable

from tip.ifp_validator import DEFAULT_IFP_SCHEMA_PATH, validate_ifp_target
from tip.validator import DEFAULT_SCHEMA_PATH, ValidationResult, validate_target


Validator = Callable[[Path, Path], list[ValidationResult]]


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

    ifp_parser = subparsers.add_parser(
        "validate-ifp",
        help="Validate one IFP record or a directory of .ifp.json records.",
    )
    ifp_parser.add_argument(
        "target",
        type=Path,
        help="Path to an .ifp.json file or a directory containing .ifp.json files.",
    )
    ifp_parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_IFP_SCHEMA_PATH,
        help="Path to the IFP record JSON schema.",
    )

    return parser


def run_validation(target: Path, schema: Path, validator: Validator) -> int:
    try:
        results = validator(target, schema)
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
        return run_validation(args.target, args.schema, validate_target)

    if args.command == "validate-ifp":
        return run_validation(args.target, args.schema, validate_ifp_target)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
