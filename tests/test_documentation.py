"""Tests that keep documentation aligned with executable repository behavior."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOCUMENTS_WITH_LOCAL_LINKS = (
    ROOT / "README.md",
    ROOT / "ROADMAP.md",
    ROOT / "BACKLOG.md",
    ROOT / "spec" / "v0.1.md",
    ROOT / "protocols" / "ifp" / "spec.md",
    ROOT / "protocols" / "ifp" / "tip-handoff.md",
    ROOT / "docs" / "cli.md",
    ROOT / "docs" / "validation.md",
)

COMMAND_SURFACES = (
    ROOT / "README.md",
    ROOT / "docs" / "cli.md",
    ROOT / "docs" / "validation.md",
    ROOT / ".github" / "workflows" / "validate.yml",
)

CANONICAL_COMMANDS = (
    "python -m tip validate examples/json/",
    "python -m tip validate-ifp examples/ifp/",
    (
        "python -m tip validate-handoff "
        "examples/handoff/project-to-next-step.handoff.json "
        "--ifp examples/ifp/project-initialization.ifp.json "
        "--tip examples/json/repository-next-step.tip.json"
    ),
    "python -m unittest discover -s tests -v",
)

CANONICAL_HANDOFF_PATH = "examples/handoff/project-to-next-step.handoff.json"

RELEASE_ARTIFACTS = (
    "spec/v0.1.md",
    "protocols/ifp/spec.md",
    "protocols/ifp/tip-handoff.md",
    "schemas/tip-record.schema.json",
    "schemas/ifp-record.schema.json",
    "schemas/ifp-tip-handoff.schema.json",
    "examples/json/startup-pivot.tip.json",
    "examples/json/bounded-learning-pilot.tip.json",
    "examples/json/pilot-review.tip.json",
    "examples/ifp/project-initialization.ifp.json",
    "examples/handoff/project-to-next-step.handoff.json",
    "tip/validator.py",
    "tip/ifp_validator.py",
    "tip/handoff_validator.py",
    ".github/workflows/validate.yml",
)

README_STRUCTURE_PATHS = (
    "tests/test_validator.py",
    "tests/test_ifp_validator.py",
    "tests/test_handoff_validator.py",
    "tests/test_documentation.py",
    "examples/json/bounded-learning-pilot.tip.json",
)

MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SCHEME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def normalize_command_text(text: str) -> str:
    """Collapse Markdown and YAML command formatting into comparable text."""

    return " ".join(text.replace("\\\n", " ").split())


def local_markdown_targets(text: str) -> list[str]:
    """Return repository-local Markdown link targets from one document."""

    targets: list[str] = []
    for match in MARKDOWN_LINK_PATTERN.finditer(text):
        target = match.group(1).strip().strip("<>")
        if not target or target.startswith(("#", "//")) or SCHEME_PATTERN.match(target):
            continue

        target = target.split("#", 1)[0].strip()
        if target:
            targets.append(target)
    return targets


class DocumentationConsistencyTests(unittest.TestCase):
    def test_local_markdown_links_point_to_existing_repository_paths(self) -> None:
        for document in DOCUMENTS_WITH_LOCAL_LINKS:
            with self.subTest(document=document.relative_to(ROOT)):
                self.assertTrue(document.is_file(), f"Missing canonical document: {document}")
                text = document.read_text(encoding="utf-8")

                for target in local_markdown_targets(text):
                    resolved = (document.parent / target).resolve()
                    try:
                        resolved.relative_to(ROOT.resolve())
                    except ValueError:
                        self.fail(f"{document}: local link escapes repository root: {target}")

                    self.assertTrue(
                        resolved.exists(),
                        f"{document}: local link target does not exist: {target}",
                    )

    def test_canonical_commands_match_across_docs_and_workflow(self) -> None:
        for surface in COMMAND_SURFACES:
            with self.subTest(surface=surface.relative_to(ROOT)):
                normalized = normalize_command_text(surface.read_text(encoding="utf-8"))
                for command in CANONICAL_COMMANDS:
                    self.assertIn(
                        command,
                        normalized,
                        f"{surface}: missing or stale canonical command: {command}",
                    )

    def test_handoff_surfaces_reference_the_canonical_example(self) -> None:
        surfaces = (
            ROOT / "README.md",
            ROOT / "docs" / "cli.md",
            ROOT / "docs" / "validation.md",
            ROOT / "protocols" / "ifp" / "tip-handoff.md",
        )

        for surface in surfaces:
            with self.subTest(surface=surface.relative_to(ROOT)):
                self.assertIn(
                    CANONICAL_HANDOFF_PATH,
                    surface.read_text(encoding="utf-8"),
                )

    def test_release_scope_and_readme_structure_reference_existing_files(self) -> None:
        roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        for relative_path in RELEASE_ARTIFACTS:
            with self.subTest(release_artifact=relative_path):
                self.assertTrue((ROOT / relative_path).is_file())
                self.assertIn(f"`{relative_path}`", roadmap)

        for relative_path in README_STRUCTURE_PATHS:
            with self.subTest(readme_structure=relative_path):
                self.assertTrue((ROOT / relative_path).is_file())
                self.assertIn(Path(relative_path).name, readme)


if __name__ == "__main__":
    unittest.main()
