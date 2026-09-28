from .model import Machine, Transition

def parse(text: str) -> Machine:
    states=[]; initial=None; transitions=[]
    for number, raw in enumerate(text.splitlines(), 1):
        line=raw.split("#",1)[0].strip()
        if not line: continue
        if line.startswith("STATE "): states.append(line[6:].strip())
        elif line.startswith("INITIAL "): initial=line[8:].strip()
        elif "->" in line and "+" in line:
            left,target=(p.strip() for p in line.split("->",1)); source,event=(p.strip() for p in left.split("+",1)); transitions.append(Transition(source,event,target))
        else: raise ValueError(f"line {number}: cannot parse {raw!r}")
    if not states: raise ValueError("machine has no states")
    initial=initial or states[0]; known=set(states)
    if initial not in known: raise ValueError(f"unknown initial state {initial!r}")
    seen=set()
    for t in transitions:
        if t.source not in known or t.target not in known: raise ValueError(f"transition references unknown state: {t}")
        key=(t.source,t.event)
        if key in seen: raise ValueError(f"non-deterministic transition: {t.source} + {t.event}")
        seen.add(key)
    return Machine(tuple(states),initial,tuple(transitions))
