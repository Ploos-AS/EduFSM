import argparse
from pathlib import Path
from .parser import parse, parse_moore, parse_mealy
from .render import table, dot
from .nfa import parse_nfa, to_dfa

def main(argv=None) -> int:
    ap=argparse.ArgumentParser(prog="edufsm",description="Educational finite-state-machine toolkit")
    sub=ap.add_subparsers(dest="command",required=True)
    run=sub.add_parser("run",help="simulate a machine"); run.add_argument("file"); run.add_argument("events",nargs="*")
    acc=sub.add_parser("accept",help="test a string with a DFA"); acc.add_argument("file"); acc.add_argument("input",nargs="?",default="")
    tab=sub.add_parser("table",help="emit a Markdown transition table"); tab.add_argument("file")
    graph=sub.add_parser("graph",help="emit Graphviz DOT"); graph.add_argument("file")
    check=sub.add_parser("check",help="analyze DFA completeness"); check.add_argument("file")
    nfa=sub.add_parser("nfa-accept",help="test a string with an NFA"); nfa.add_argument("file"); nfa.add_argument("input",nargs="?",default="")
    conv=sub.add_parser("nfa-to-dfa",help="convert an NFA to DFA and emit DOT"); conv.add_argument("file")
    mr=sub.add_parser("moore-run",help="simulate a Moore machine"); mr.add_argument("file"); mr.add_argument("events",nargs="*")
    me=sub.add_parser("mealy-run",help="simulate a Mealy machine"); me.add_argument("file"); me.add_argument("events",nargs="*")
    args=ap.parse_args(argv)
    text=Path(args.file).read_text(encoding="utf-8")
    if args.command=="nfa-accept":
        machine=parse_nfa(text); accepted=machine.accepts(args.input)
        print("ACCEPT" if accepted else "REJECT"); return 0 if accepted else 1
    if args.command=="nfa-to-dfa":
        print(dot(to_dfa(parse_nfa(text))),end=""); return 0
    if args.command=="moore-run":
        machine=parse_moore(text); state=machine.machine.initial
        print(f"Initial state: {state} | output: {machine.output(state)}")
        for number,event in enumerate(args.events,1):
            new,output=machine.step(state,event)
            print(f"[{number:03}] {event}: {state} -> {new} | output: {output}"); state=new
        print(f"Final state: {state} | output: {machine.output(state)}"); return 0
    if args.command=="mealy-run":
        machine=parse_mealy(text); state=machine.initial
        print(f"Initial state: {state}")
        for number,event in enumerate(args.events,1):
            new,output=machine.step(state,event)
            print(f"[{number:03}] {event}: {state} -> {new} | output: {output}"); state=new
        print(f"Final state: {state}"); return 0
    machine=parse(text)
    if args.command=="table": print(table(machine),end=""); return 0
    if args.command=="graph": print(dot(machine),end=""); return 0
    if args.command=="check":
        print("Alphabet:", " ".join(machine.alphabet) or "(empty)")
        missing=machine.missing_transitions()
        if not missing: print("DFA: complete"); return 0
        print("DFA: incomplete")
        for state,symbol in missing: print(f"missing: {state} + {symbol}")
        return 1
    if args.command=="accept":
        try: accepted=machine.accepts(args.input)
        except ValueError as exc: print(f"ERROR: {exc}"); return 2
        print("ACCEPT" if accepted else "REJECT"); return 0 if accepted else 1
    state=machine.initial; print(f"Initial state: {state}")
    if args.events:
        for number,event in enumerate(args.events,1):
            new=machine.next_state(state,event); print(f"[{number:03}] {event}: {state} -> {new}"); state=new
        print(f"Final state: {state}"); return 0
    try:
        while True:
            event=input("> ").strip()
            if not event: continue
            new=machine.next_state(state,event); print(f"{state} -> {new}"); state=new
    except (EOFError,KeyboardInterrupt): print(); return 0

if __name__=="__main__": raise SystemExit(main())
