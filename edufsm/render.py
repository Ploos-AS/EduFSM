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
