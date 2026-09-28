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


def input_codes(machine: Machine) -> tuple[tuple[str, str], ...]:
    """Assign compact binary codes to input symbols."""
    symbols=machine.alphabet
    if not symbols: return ()
    bits=max(1,ceil(log2(len(symbols))))
    return tuple((symbol,format(index,f"0{bits}b")) for index,symbol in enumerate(symbols))

def next_state_equations(machine: Machine, encoding: StateEncoding) -> tuple[tuple[str, str], ...]:
    """Generate canonical SOP equations for D flip-flop inputs.

    Q bits represent present state; X bits represent encoded input symbols.
    Only explicitly defined transitions contribute minterms.
    """
    inputs=input_codes(machine)
    if not inputs: return tuple((f"D{i}","0") for i in range(encoding.bits))
    input_map=dict(inputs)
    terms=[[] for _ in range(encoding.bits)]
    for t in machine.transitions:
        present=encoding.code(t.source)
        event=input_map[t.event]
        nxt=encoding.code(t.target)
        literals=[]
        for i,bit in enumerate(present):
            name=f"Q{i}"
            literals.append(name if bit=="1" else f"!{name}")
        for i,bit in enumerate(event):
            name=f"X{i}"
            literals.append(name if bit=="1" else f"!{name}")
        term=" & ".join(literals)
        for i,bit in enumerate(nxt):
            if bit=="1": terms[i].append(f"({term})")
    return tuple((f"D{i}"," | ".join(bits) if bits else "0") for i,bits in enumerate(terms))


def reset_value(machine: Machine, encoding: StateEncoding) -> str:
    """Return the encoded value loaded into the state register on reset."""
    return encoding.code(machine.initial)

def moore_output_table(machine, encoding: StateEncoding) -> tuple[tuple[str, str], ...]:
    """Return encoded-state/output rows for a Moore machine."""
    return tuple((encoding.code(state),machine.output(state)) for state in machine.machine.states)

def clocked_step(machine: Machine, encoding: StateEncoding, state_bits: str, event: str, reset: bool=False) -> str:
    """Model one active clock edge of a synchronous state register."""
    if reset:
        return reset_value(machine,encoding)
    reverse={code:state for state,code in encoding.codes}
    if state_bits not in reverse:
        raise ValueError(f"invalid encoded state {state_bits!r}")
    return encoding.code(machine.next_state(reverse[state_bits],event))
