#!/usr/bin/env python3
"""Extract exercise sections from the canonical EduFSM book manifests."""
from pathlib import Path
import re
import sys
from build_book import manifest_paths

ROOT = Path(__file__).resolve().parents[1]
HEADINGS = {
    "no": {"øvelse", "oppgaver", "eksperiment"},
    "en": {"exercise", "exercises", "experiment"},
}

def exercise_markdown(language: str) -> str:
    title = "EduFSM — Oppgaver" if language == "no" else "EduFSM — Exercises"
    parts = [f"# {title}"]
    count = 0
    for chapter in manifest_paths(language):
        lines = chapter.read_text(encoding="utf-8").splitlines()
        chapter_title = next((x.lstrip("# ").strip() for x in lines if x.startswith("# ")), chapter.stem)
        i = 0
        while i < len(lines):
            m = re.match(r"^(##+)\s+(.+?)\s*$", lines[i])
            if not m or m.group(2).strip().lower() not in HEADINGS[language]:
                i += 1
                continue
            level = len(m.group(1))
            j = i + 1
            while j < len(lines):
                nxt = re.match(r"^(#+)\s+", lines[j])
                if nxt and len(nxt.group(1)) <= level:
                    break
                j += 1
            body = "\n".join(lines[i + 1:j]).strip()
            if body:
                parts.append(f"## {chapter_title}\n\n{body}")
                count += 1
            i = j
    if not count:
        raise ValueError(f"no exercise sections found for {language}")
    return "\n\n---\n\n".join(parts) + "\n"

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2 or argv[0] not in ("no", "en"):
        print("usage: build_exercises.py no|en OUTPUT.md", file=sys.stderr)
        return 2
    output = Path(argv[1])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(exercise_markdown(argv[0]), encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
