#!/usr/bin/env python3
"""Generate browser conformance fixtures from the Python reference core."""

import json
from pathlib import Path

from edufsm.parser import parse
from edufsm.trace import record_trace
from edufsm.analysis import reachable_states, unreachable_states

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "turnstile": ("examples/turnstile.fsm", ("coin", "push", "coin")),
    "traffic-light": ("examples/traffic-light.fsm", ("timer", "timer", "timer")),
    "digital-lock": ("examples/digital-lock.fsm", ("1", "2", "3", "reset")),
}

out = {"format": "edufsm-web-conformance-v1", "cases": []}
for name, (relative, events) in CASES.items():
    source = (ROOT / relative).read_text(encoding="utf-8")
    machine = parse(source)
    trace = record_trace(machine, events)
    out["cases"].append({
        "name": name,
        "source": source,
        "events": list(events),
        "initial": machine.initial,
        "final": trace.final,
        "reachable": list(reachable_states(machine)),
        "unreachable": list(unreachable_states(machine)),
        "steps": [
            {"source": s.source, "event": s.event, "target": s.target}
            for s in trace.steps
        ],
    })

path = ROOT / "simulator" / "web" / "conformance.json"
path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(path)
