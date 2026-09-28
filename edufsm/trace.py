"""Deterministic trace and replay support for EduFSM."""

from dataclasses import dataclass
import json

from .model import Machine


@dataclass(frozen=True)
class TraceStep:
    source: str
    event: str
    target: str


@dataclass(frozen=True)
class Trace:
    initial: str
    steps: tuple[TraceStep, ...]

    @property
    def final(self) -> str:
        return self.steps[-1].target if self.steps else self.initial

    def to_json(self) -> str:
        return json.dumps({
            "format": "edufsm-trace-v1",
            "initial": self.initial,
            "steps": [
                {"source": s.source, "event": s.event, "target": s.target}
                for s in self.steps
            ],
        }, indent=2) + "\n"

    @classmethod
    def from_json(cls, text: str) -> "Trace":
        data = json.loads(text)
        if data.get("format") != "edufsm-trace-v1":
            raise ValueError("Unsupported EduFSM trace format")
        return cls(
            initial=data["initial"],
            steps=tuple(
                TraceStep(s["source"], s["event"], s["target"])
                for s in data["steps"]
            ),
        )


def record_trace(machine: Machine, events) -> Trace:
    """Execute events and record the exact deterministic transition sequence."""
    state = machine.initial
    steps = []
    for event in events:
        target = machine.next_state(state, event)
        steps.append(TraceStep(state, event, target))
        state = target
    return Trace(machine.initial, tuple(steps))


def replay_trace(machine: Machine, trace: Trace) -> str:
    """Replay and validate a trace against a machine, returning final state."""
    if trace.initial != machine.initial:
        raise ValueError(
            f"Trace initial state {trace.initial!r} does not match machine initial state {machine.initial!r}"
        )
    state = machine.initial
    for index, step in enumerate(trace.steps):
        if step.source != state:
            raise ValueError(
                f"Trace step {index} source {step.source!r} does not match current state {state!r}"
            )
        actual = machine.next_state(state, step.event)
        if actual != step.target:
            raise ValueError(
                f"Trace step {index} expected target {step.target!r}, machine produced {actual!r}"
            )
        state = actual
    return state
