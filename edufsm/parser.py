from .model import Machine, Transition

def parse(text: str) -> Machine:
    states=[]; initial=None; accepting=[]; transitions=[]
    for number,raw in enumerate(text.splitlines(),1):
        line=raw.split("#",1)[0].strip()
        if not line: continue
        lower=line.lower()
        if lower.startswith("machine "): continue
        if lower.startswith("state "):
            state=line.split(None,1)[1].strip()
            if state not in states: states.append(state)
        elif lower.startswith("initial "): initial=line.split(None,1)[1].strip()
        elif lower.startswith("accept "): accepting.extend(line.split()[1:])
        elif lower.startswith("transition "):
            parts=line.split()
            if len(parts)!=4: raise ValueError(f"line {number}: transition needs source event target")
            _,source,event,target=parts; transitions.append(Transition(source,event,target))
        elif "->" in line and "+" in line:
            left,target=(x.strip() for x in line.split("->",1)); source,event=(x.strip() for x in left.split("+",1)); transitions.append(Transition(source,event,target))
        else: raise ValueError(f"line {number}: cannot parse {raw!r}")
    if not states: raise ValueError("machine has no states")
    initial=initial or states[0]; known=set(states)
    if initial not in known: raise ValueError(f"unknown initial state {initial!r}")
    unknown_accept=set(accepting)-known
    if unknown_accept: raise ValueError(f"unknown accepting state(s): {', '.join(sorted(unknown_accept))}")
    seen=set()
    for t in transitions:
        if t.source not in known or t.target not in known: raise ValueError(f"transition references unknown state: {t}")
        key=(t.source,t.event)
        if key in seen: raise ValueError(f"non-deterministic transition: {t.source} + {t.event}")
        seen.add(key)
    return Machine(tuple(states),initial,tuple(transitions),tuple(dict.fromkeys(accepting)))


def parse_moore(text: str):
    from .model import MooreMachine
    base_lines=[]; outputs=[]
    for number,raw in enumerate(text.splitlines(),1):
        line=raw.split("#",1)[0].strip()
        if not line: continue
        parts=line.split()
        if parts[0].lower()=="output":
            if len(parts)!=3: raise ValueError(f"line {number}: OUTPUT needs state value")
            outputs.append((parts[1],parts[2])); continue
        base_lines.append(raw)
    machine=parse("\n".join(base_lines))
    values=dict(outputs)
    unknown=set(values)-set(machine.states)
    if unknown: raise ValueError(f"output references unknown state(s): {', '.join(sorted(unknown))}")
    missing=set(machine.states)-set(values)
    if missing: raise ValueError(f"missing Moore output for state(s): {', '.join(sorted(missing))}")
    return MooreMachine(machine,tuple(outputs))

def parse_mealy(text: str):
    from .model import MealyMachine, MealyTransition
    states=[]; initial=None; transitions=[]; seen=set()
    for number,raw in enumerate(text.splitlines(),1):
        line=raw.split("#",1)[0].strip()
        if not line: continue
        parts=line.split()
        keyword=parts[0].lower()
        if keyword=="machine": continue
        if keyword=="state":
            if len(parts)!=2: raise ValueError(f"line {number}: STATE needs a name")
            if parts[1] not in states: states.append(parts[1])
            continue
        if keyword=="initial":
            if len(parts)!=2: raise ValueError(f"line {number}: INITIAL needs a state")
            initial=parts[1]; continue
        if "->" in line and "+" in line and "/" in line:
            left,right=(x.strip() for x in line.split("->",1))
            source,event=(x.strip() for x in left.split("+",1))
            target,output=(x.strip() for x in right.split("/",1))
            key=(source,event)
            if key in seen: raise ValueError(f"non-deterministic transition: {source} + {event}")
            seen.add(key); transitions.append(MealyTransition(source,event,target,output)); continue
        raise ValueError(f"line {number}: cannot parse {raw!r}")
    if not states: raise ValueError("machine has no states")
    initial=initial or states[0]; known=set(states)
    if initial not in known: raise ValueError(f"unknown initial state {initial!r}")
    for t in transitions:
        if t.source not in known or t.target not in known: raise ValueError(f"transition references unknown state: {t}")
    return MealyMachine(tuple(states),initial,tuple(transitions))
