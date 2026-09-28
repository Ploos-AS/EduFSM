from dataclasses import dataclass

@dataclass(frozen=True)
class Transition:
    source: str
    event: str
    target: str

@dataclass(frozen=True)
class Machine:
    states: tuple[str, ...]
    initial: str
    transitions: tuple[Transition, ...]
    accepting: tuple[str, ...] = ()

    @property
    def alphabet(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(t.event for t in self.transitions))

    def next_state(self, state: str, event: str) -> str:
        matches=[t.target for t in self.transitions if t.source==state and t.event==event]
        if not matches: raise ValueError(f"No transition from {state!r} for event {event!r}")
        if len(matches)!=1: raise ValueError(f"Machine is not deterministic at {state!r} / {event!r}")
        return matches[0]

    def accepts(self, symbols) -> bool:
        state=self.initial
        for symbol in symbols:
            state=self.next_state(state, symbol)
        return state in self.accepting
