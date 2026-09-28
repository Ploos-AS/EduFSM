"""Static analysis helpers for deterministic EduFSM machines."""

from .model import Machine, Transition


def reachable_states(machine: Machine) -> tuple[str, ...]:
    """Return states reachable from the initial state, preserving declaration order."""
    seen = {machine.initial}
    changed = True
    while changed:
        changed = False
        for transition in machine.transitions:
            if transition.source in seen and transition.target not in seen:
                seen.add(transition.target)
                changed = True
    return tuple(state for state in machine.states if state in seen)


def unreachable_states(machine: Machine) -> tuple[str, ...]:
    """Return declared states that cannot be reached from the initial state."""
    reachable = set(reachable_states(machine))
    return tuple(state for state in machine.states if state not in reachable)


def dead_end_states(machine: Machine) -> tuple[str, ...]:
    """Return states with no outgoing transitions."""
    sources = {transition.source for transition in machine.transitions}
    return tuple(state for state in machine.states if state not in sources)


def productive_states(machine: Machine) -> tuple[str, ...]:
    """Return states from which an accepting state can be reached.

    For machines without accepting states, productivity is undefined and the
    empty tuple is returned.
    """
    if not machine.accepting:
        return ()
    productive = set(machine.accepting)
    changed = True
    while changed:
        changed = False
        for transition in machine.transitions:
            if transition.target in productive and transition.source not in productive:
                productive.add(transition.source)
                changed = True
    return tuple(state for state in machine.states if state in productive)


def nonproductive_states(machine: Machine) -> tuple[str, ...]:
    """Return states that cannot reach acceptance.

    This concept only applies when the machine declares accepting states.
    """
    if not machine.accepting:
        return ()
    productive = set(productive_states(machine))
    return tuple(state for state in machine.states if state not in productive)


def nondeterministic_pairs(machine: Machine) -> tuple[tuple[str, str], ...]:
    """Return state/event pairs with more than one transition."""
    counts: dict[tuple[str, str], int] = {}
    for transition in machine.transitions:
        key = (transition.source, transition.event)
        counts[key] = counts.get(key, 0) + 1
    return tuple(key for key, count in counts.items() if count > 1)


def transition_coverage(machine: Machine, trace) -> tuple[int, int, float]:
    """Return covered transitions, total transitions, and coverage percentage."""
    covered: set[Transition] = set()
    state = machine.initial
    for event in trace:
        matches = [t for t in machine.transitions if t.source == state and t.event == event]
        if len(matches) != 1:
            machine.next_state(state, event)  # raise the model's canonical error
        transition = matches[0]
        covered.add(transition)
        state = transition.target
    total = len(machine.transitions)
    percent = 100.0 if total == 0 else 100.0 * len(covered) / total
    return len(covered), total, percent
