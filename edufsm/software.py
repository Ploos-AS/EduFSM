"""Generate straightforward software implementations of deterministic FSMs."""

from .model import Machine


def _ident(name: str) -> str:
    """Convert an educational FSM name to a conservative identifier."""
    value="".join(ch if ch.isalnum() else "_" for ch in name)
    if not value or value[0].isdigit():
        value="_"+value
    return value


def python_match(machine: Machine) -> str:
    """Generate an explicit Python match/case state transition function."""
    lines=["from enum import Enum", "", "", "class State(Enum):"]
    for state in machine.states:
        lines.append(f'    {_ident(state).upper()} = "{state}"')
    lines += ["", "", "def step(state: State, event: str) -> State:", "    match (state, event):"]
    for t in machine.transitions:
        lines.append(
            f'        case (State.{_ident(t.source).upper()}, "{t.event}"):'
        )
        lines.append(f"            return State.{_ident(t.target).upper()}")
    lines += [
        "        case _:",
        '            raise ValueError(f"no transition for {state.value!r} / {event!r}")',
        "",
        f"state = State.{_ident(machine.initial).upper()}",
    ]
    return "\n".join(lines)+"\n"


def python_table(machine: Machine) -> str:
    """Generate a table-driven Python implementation."""
    lines=["TRANSITIONS = {"]
    for t in machine.transitions:
        lines.append(f'    ("{t.source}", "{t.event}"): "{t.target}",')
    lines += [
        "}",
        "",
        f'STATE = "{machine.initial}"',
        "",
        "def step(state: str, event: str) -> str:",
        "    try:",
        "        return TRANSITIONS[(state, event)]",
        "    except KeyError:",
        '        raise ValueError(f"no transition for {state!r} / {event!r}") from None',
    ]
    return "\n".join(lines)+"\n"


def c_switch(machine: Machine) -> str:
    """Generate a small C enum/switch implementation."""
    state_names={s:f"STATE_{_ident(s).upper()}" for s in machine.states}
    event_names={e:f"EVENT_{_ident(e).upper()}" for e in machine.alphabet}
    lines=[
        "#include <stdbool.h>",
        "",
        "typedef enum {",
        "    "+",\n    ".join(state_names.values()),
        "} state_t;",
        "",
        "typedef enum {",
        "    "+",\n    ".join(event_names.values()),
        "} event_t;",
        "",
        "bool fsm_step(state_t *state, event_t event)",
        "{",
        "    switch (*state) {",
    ]
    for state in machine.states:
        lines.append(f"    case {state_names[state]}:")
        outgoing=[t for t in machine.transitions if t.source==state]
        lines.append("        switch (event) {")
        for t in outgoing:
            lines.append(f"        case {event_names[t.event]}: *state = {state_names[t.target]}; return true;")
        lines += ["        default: return false;", "        }"]
    lines += ["    default: return false;", "    }", "}", "", f"state_t state = {state_names[machine.initial]};"]
    return "\n".join(lines)+"\n"


class EventDrivenFSM:
    """Small queue-driven runtime showing how FSMs fit event loops."""

    def __init__(self, machine: Machine):
        self.machine=machine
        self.state=machine.initial
        self._queue=[]

    def post(self, event: str) -> None:
        """Append an event without changing state immediately."""
        self._queue.append(event)

    @property
    def pending(self) -> tuple[str, ...]:
        return tuple(self._queue)

    def dispatch_one(self) -> tuple[str, str, str]:
        """Consume one queued event and execute its transition."""
        if not self._queue:
            raise ValueError("event queue is empty")
        event=self._queue.pop(0)
        source=self.state
        self.state=self.machine.next_state(self.state,event)
        return source,event,self.state

    def dispatch_all(self) -> tuple[tuple[str, str, str], ...]:
        """Drain the queue in FIFO order and return a deterministic trace."""
        trace=[]
        while self._queue:
            trace.append(self.dispatch_one())
        return tuple(trace)
