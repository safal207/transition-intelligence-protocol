"""Command-line interface for Transition Intelligence Protocol."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable

from tip.handoff_validator import validate_ifp_to_tip_handoff
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

    handoff_parser = subparsers.add_parser(
        "validate-handoff",
        help="Validate provenance across one ready IFP record and one TIP record.",
    )
    handoff_parser.add_argument(
        "tip_record",
        type=Path,
        help="Path to the TIP record receiving the initialized state.",
    )
    handoff_parser.add_argument(
        "ifp_record",
        type=Path,
        help="Path to the ready IFP source record.",
    )
    handoff_parser.add_argument(
        "--tip-schema",
        type=Path,
        default=DEFAULT_SCHEMA_PATH,
        help="Path to the TIP record JSON schema.",
    )
    handoff_parser.add_argument(
        "--ifp-schema",
        type=Path,
        default=DEFAULT_IFP_SCHEMA_PATH,
        help="Path to the IFP record JSON schema.",
    )

    return parser


def print_results(results: list[ValidationResult]) -> int:
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


def run_validation(target: Path, schema: Path, validator: Validator) -> int:
    try:
        results = validator(target, schema)
    except FileNotFoundError as exc:
        print(f"FAIL {exc}")
        return 1

    return print_results(results)


def run_handoff_validation(
    tip_record: Path,
    ifp_record: Path,
    tip_schema: Path,
    ifp_schema: Path,
) -> int:
    try:
        result = validate_ifp_to_tip_handoff(
            tip_record,
            ifp_record,
            tip_schema,
            ifp_schema,
        )
    except FileNotFoundError as exc:
        print(f"FAIL {exc}")
        return 1

    return print_results([result])


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        return run_validation(args.target, args.schema, validate_target)

    if args.command == "validate-ifp":
        return run_validation(args.target, args.schema, validate_ifp_target)

    if args.command == "validate-handoff":
        return run_handoff_validation(
            args.tip_record,
            args.ifp_record,
            args.tip_schema,
            args.ifp_schema,
        )

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
