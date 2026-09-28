import argparse
from pathlib import Path
from .parser import parse

def main(argv=None) -> int:
    ap=argparse.ArgumentParser(prog="edufsm",description="Run a deterministic EduFSM machine")
    ap.add_argument("file"); ap.add_argument("events",nargs="*"); args=ap.parse_args(argv)
    machine=parse(Path(args.file).read_text(encoding="utf-8")); state=machine.initial
    print(f"Initial state: {state}")
    if args.events:
        for event in args.events:
            new=machine.next_state(state,event); print(f"{event}: {state} -> {new}"); state=new
        return 0
    try:
        while True:
            event=input("> ").strip()
            if not event: continue
            new=machine.next_state(state,event); print(f"{state} -> {new}"); state=new
    except (EOFError,KeyboardInterrupt): print(); return 0

if __name__ == "__main__": raise SystemExit(main())
