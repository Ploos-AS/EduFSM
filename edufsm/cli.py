import argparse
from pathlib import Path
from .parser import parse
from .render import table, dot

def main(argv=None) -> int:
    ap=argparse.ArgumentParser(prog="edufsm",description="Educational deterministic FSM toolkit")
    sub=ap.add_subparsers(dest="command")
    run=sub.add_parser("run",help="simulate a machine"); run.add_argument("file"); run.add_argument("events",nargs="*")
    tab=sub.add_parser("table",help="emit a Markdown transition table"); tab.add_argument("file")
    graph=sub.add_parser("graph",help="emit Graphviz DOT"); graph.add_argument("file")
    # M1 compatibility: edufsm FILE EVENT...
    args,extra=ap.parse_known_args(argv)
    if args.command is None:
        raw=list(argv or [])
        if not raw:
            ap.print_help(); return 2
        args=run.parse_args(raw)
        args.command="run"
    machine=parse(Path(args.file).read_text(encoding="utf-8"))
    if args.command=="table": print(table(machine),end=""); return 0
    if args.command=="graph": print(dot(machine),end=""); return 0
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
