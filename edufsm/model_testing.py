"""Deterministic model-based test generation for EduFSM."""

import random

from .model import Machine
from .trace import Trace, record_trace


def generate_events(machine: Machine, steps: int, seed: int = 0) -> tuple[str, ...]:
    """Generate a reproducible valid event sequence by walking the model."""
    if steps < 0:
        raise ValueError("steps must be non-negative")
    rng = random.Random(seed)
    state = machine.initial
    events = []
    for _ in range(steps):
        choices = [t for t in machine.transitions if t.source == state]
        if not choices:
            break
        transition = choices[rng.randrange(len(choices))]
        events.append(transition.event)
        state = transition.target
    return tuple(events)


def generate_trace(machine: Machine, steps: int, seed: int = 0) -> Trace:
    """Generate and execute a reproducible valid model-based trace."""
    return record_trace(machine, generate_events(machine, steps, seed))


def generated_transition_coverage(machine: Machine, runs: int, steps: int, seed: int = 0):
    """Measure transition coverage across deterministic generated walks."""
    if runs < 0:
        raise ValueError("runs must be non-negative")
    covered = set()
    for run in range(runs):
        trace = generate_trace(machine, steps, seed + run)
        covered.update((s.source, s.event, s.target) for s in trace.steps)
    total = len(machine.transitions)
    percent = 100.0 if total == 0 else 100.0 * len(covered) / total
    return len(covered), total, percent
