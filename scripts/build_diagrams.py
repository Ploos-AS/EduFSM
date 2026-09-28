#!/usr/bin/env python3
"""Generate deterministic Graphviz sources for EduFSM book examples."""
from pathlib import Path
from edufsm.parser import parse
from edufsm.render import dot

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "diagrams"
EXAMPLES = (
    "turnstile",
    "traffic-light",
    "digital-lock",
    "command-parser",
    "protocol-controller",
    "lexer-identifier",
    "uart-receiver",
    "dfa-ends-in-1",
)

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name in EXAMPLES:
        source = ROOT / "examples" / f"{name}.fsm"
        machine = parse(source.read_text(encoding="utf-8"))
        (OUT / f"{name}.dot").write_text(dot(machine), encoding="utf-8")
        print(OUT / f"{name}.dot")

if __name__ == "__main__":
    main()
