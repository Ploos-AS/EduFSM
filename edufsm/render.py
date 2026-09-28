from .model import Machine

def table(machine: Machine) -> str:
    rows=["| Current state | Event | Next state |","|---|---|---|"]
    rows += [f"| {t.source} | {t.event} | {t.target} |" for t in machine.transitions]
    return "\n".join(rows)+"\n"

def dot(machine: Machine) -> str:
    lines=["digraph FSM {","  rankdir=LR;","  __start [shape=point];",f'  __start -> "{machine.initial}";']
    for state in machine.states:
        lines.append(f'  "{state}" [shape=circle];')
    for t in machine.transitions:
        lines.append(f'  "{t.source}" -> "{t.target}" [label="{t.event}"];')
    lines.append("}")
    return "\n".join(lines)+"\n"


def moore_dot(machine) -> str:
    base=machine.machine
    lines=["digraph Moore {","  rankdir=LR;","  __start [shape=point];",f'  __start -> "{base.initial}";']
    for state in base.states:
        label=f"{state} / {machine.output(state)}"
        lines.append(f'  "{state}" [shape=circle,label="{label}"];')
    for t in base.transitions:
        lines.append(f'  "{t.source}" -> "{t.target}" [label="{t.event}"];')
    lines.append("}")
    return "\n".join(lines)+"\n"

def mealy_dot(machine) -> str:
    lines=["digraph Mealy {","  rankdir=LR;","  __start [shape=point];",f'  __start -> "{machine.initial}";']
    for state in machine.states:
        lines.append(f'  "{state}" [shape=circle];')
    for t in machine.transitions:
        lines.append(f'  "{t.source}" -> "{t.target}" [label="{t.event} / {t.output}"];')
    lines.append("}")
    return "\n".join(lines)+"\n"
