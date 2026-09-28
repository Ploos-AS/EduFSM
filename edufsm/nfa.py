from dataclasses import dataclass
from .model import Transition

EPSILON = "epsilon"

@dataclass(frozen=True)
class NFA:
    states: tuple[str, ...]
    initial: str
    transitions: tuple[Transition, ...]
    accepting: tuple[str, ...] = ()

    @property
    def alphabet(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(t.event for t in self.transitions if t.event != EPSILON))

    def epsilon_closure(self, states) -> frozenset[str]:
        closure=set(states); pending=list(states)
        while pending:
            state=pending.pop()
            for t in self.transitions:
                if t.source==state and t.event==EPSILON and t.target not in closure:
                    closure.add(t.target); pending.append(t.target)
        return frozenset(closure)

    def step(self, states, symbol: str) -> frozenset[str]:
        active=self.epsilon_closure(states)
        targets={t.target for t in self.transitions if t.source in active and t.event==symbol}
        return self.epsilon_closure(targets)

    def accepts(self, symbols) -> bool:
        active=self.epsilon_closure({self.initial})
        for symbol in symbols: active=self.step(active,symbol)
        return bool(active.intersection(self.accepting))

def parse_nfa(text: str) -> NFA:
    states=[]; initial=None; accepting=[]; transitions=[]
    for number,raw in enumerate(text.splitlines(),1):
        line=raw.split("#",1)[0].strip()
        if not line: continue
        lower=line.lower()
        keyword=line.split(None,1)[0].lower()
        if keyword in ("nfa","machine"): continue
        if keyword=="state":
            state=line.split(None,1)[1].strip()
            if state not in states: states.append(state)
            continue
        if keyword=="initial": initial=line.split(None,1)[1].strip(); continue
        if keyword=="accept": accepting.extend(line.split()[1:]); continue
        if keyword=="transition":
            parts=line.split()
            if len(parts)!=4: raise ValueError(f"line {number}: transition needs source event target")
            _,source,event,target=parts; transitions.append(Transition(source,event,target)); continue
        if "->" in line and "+" in line:
            left,target=(x.strip() for x in line.split("->",1)); source,event=(x.strip() for x in left.split("+",1)); transitions.append(Transition(source,event,target)); continue
        raise ValueError(f"line {number}: cannot parse {raw!r}")
    if not states: raise ValueError("NFA has no states")
    initial=initial or states[0]; known=set(states)
    if initial not in known: raise ValueError(f"unknown initial state {initial!r}")
    if set(accepting)-known: raise ValueError("unknown accepting state")
    for t in transitions:
        if t.source not in known or t.target not in known: raise ValueError(f"transition references unknown state: {t}")
    return NFA(tuple(states),initial,tuple(transitions),tuple(dict.fromkeys(accepting)))


def to_dfa(nfa: NFA):
    """Convert an NFA to an equivalent DFA using subset construction."""
    from .model import Machine

    start=nfa.epsilon_closure({nfa.initial})
    pending=[start]; discovered=[start]; edges=[]
    while pending:
        current=pending.pop(0)
        for symbol in nfa.alphabet:
            target=nfa.step(current,symbol)
            if target not in discovered:
                discovered.append(target); pending.append(target)
            edges.append((current,symbol,target))

    def name(states):
        if not states: return "{}"
        return "{" + ",".join(state for state in nfa.states if state in states) + "}"

    states=tuple(name(s) for s in discovered)
    transitions=tuple(Transition(name(src),symbol,name(dst)) for src,symbol,dst in edges)
    accepting=tuple(name(s) for s in discovered if set(s).intersection(nfa.accepting))
    return Machine(states,name(start),transitions,accepting)
