"""Digital implementation helpers for deterministic FSMs."""

from dataclasses import dataclass
from math import ceil, log2
from .model import Machine

@dataclass(frozen=True)
class StateEncoding:
    bits: int
    codes: tuple[tuple[str, str], ...]

    def code(self, state: str) -> str:
        values=dict(self.codes)
        if state not in values:
            raise ValueError(f"unknown encoded state {state!r}")
        return values[state]

def binary_encoding(machine: Machine) -> StateEncoding:
    """Assign compact binary codes in declared state order."""
    bits=max(1,ceil(log2(len(machine.states))))
    return StateEncoding(bits,tuple(
        (state,format(index,f"0{bits}b"))
        for index,state in enumerate(machine.states)
    ))

def one_hot_encoding(machine: Machine) -> StateEncoding:
    """Assign one flip-flop per state."""
    bits=len(machine.states)
    return StateEncoding(bits,tuple(
        (state,format(1 << (bits-index-1),f"0{bits}b"))
        for index,state in enumerate(machine.states)
    ))

def transition_truth_table(machine: Machine, encoding: StateEncoding):
    """Return (present bits, input, next bits) rows for defined transitions."""
    return tuple(
        (encoding.code(t.source),t.event,encoding.code(t.target))
        for t in machine.transitions
    )
