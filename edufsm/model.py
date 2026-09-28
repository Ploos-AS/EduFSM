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

    def missing_transitions(self) -> tuple[tuple[str, str], ...]:
        present={(t.source,t.event) for t in self.transitions}
        return tuple((state,symbol) for state in self.states for symbol in self.alphabet if (state,symbol) not in present)

    @property
    def is_complete(self) -> bool:
        return not self.missing_transitions()

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

@dataclass(frozen=True)
class MooreMachine:
    machine: Machine
    outputs: tuple[tuple[str, str], ...]

    def output(self, state: str) -> str:
        values=dict(self.outputs)
        if state not in values: raise ValueError(f"No Moore output for state {state!r}")
        return values[state]

    def step(self, state: str, event: str) -> tuple[str, str]:
        target=self.machine.next_state(state,event)
        return target,self.output(target)

@dataclass(frozen=True)
class MealyTransition:
    source: str
    event: str
    target: str
    output: str

@dataclass(frozen=True)
class MealyMachine:
    states: tuple[str, ...]
    initial: str
    transitions: tuple[MealyTransition, ...]

    def step(self, state: str, event: str) -> tuple[str, str]:
        matches=[t for t in self.transitions if t.source==state and t.event==event]
        if not matches: raise ValueError(f"No transition from {state!r} for event {event!r}")
        if len(matches)!=1: raise ValueError(f"Machine is not deterministic at {state!r} / {event!r}")
        return matches[0].target,matches[0].output
