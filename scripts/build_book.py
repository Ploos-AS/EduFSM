#!/usr/bin/env python3
"""Build canonical EduFSM course sources from language manifests."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def manifest_paths(language: str):
    manifest = ROOT / "docs" / language / "BOOK.md"
    text = manifest.read_text(encoding="utf-8")
    for match in re.finditer(r"^\d+\.\s+(.+\.md)\s*$", text, re.MULTILINE):
        path = (manifest.parent / match.group(1)).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError(f"chapter escapes repository: {path}")
        if not path.is_file():
            raise FileNotFoundError(path)
        yield path


def combined_markdown(language: str) -> str:
    chapters = list(manifest_paths(language))
    if not chapters:
        raise ValueError(f"no chapters in {language} manifest")
    title = "EduFSM — Tilstandsmaskiner" if language == "no" else "EduFSM — Finite State Machines"
    parts = [f"# {title}\n"]
    for chapter in chapters:
        parts.append(chapter.read_text(encoding="utf-8").strip())
    heading = "Eksempeldiagrammer" if language == "no" else "Example diagrams"
    intro = "Generert fra de samme .fsm-filene som simulatoren og testene bruker." if language == "no" else "Generated from the same .fsm files used by the simulator and tests."
    diagrams = [f"# {heading}\n\n{intro}"]
    for name in ("turnstile", "traffic-light", "digital-lock", "command-parser", "protocol-controller", "lexer-identifier", "uart-receiver", "dfa-ends-in-1"):
        diagrams.append(f"## {name}\n\n![{name}](diagrams/{name}.png)")
    parts.append("\n\n".join(diagrams))
    return "\n\n---\n\n".join(parts) + "\n"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2 or argv[0] not in ("no", "en"):
        print("usage: build_book.py no|en OUTPUT.md", file=sys.stderr)
        return 2
    output = Path(argv[1])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(combined_markdown(argv[0]), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
