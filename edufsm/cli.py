import argparse
from pathlib import Path
from .parser import parse, parse_moore, parse_mealy
from .render import table, dot, moore_dot, mealy_dot
from .nfa import parse_nfa, to_dfa
from .digital import binary_encoding, one_hot_encoding, transition_truth_table, input_codes, next_state_equations
from .software import python_match, python_table, c_switch
from .hdl import systemverilog, systemverilog_testbench
from .trace import Trace, record_trace, replay_trace
from .analysis import unreachable_states, dead_end_states, nonproductive_states, nondeterministic_pairs
from .model_testing import generate_trace, generated_transition_coverage

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
    mg=sub.add_parser("moore-graph",help="emit Graphviz DOT for a Moore machine"); mg.add_argument("file")
    meg=sub.add_parser("mealy-graph",help="emit Graphviz DOT for a Mealy machine"); meg.add_argument("file")
    enc=sub.add_parser("encode",help="show digital state encoding"); enc.add_argument("file"); enc.add_argument("--style",choices=("binary","one-hot"),default="binary")
    truth=sub.add_parser("truth-table",help="show encoded transition truth table"); truth.add_argument("file"); truth.add_argument("--style",choices=("binary","one-hot"),default="binary")
    eq=sub.add_parser("equations",help="derive canonical next-state Boolean equations"); eq.add_argument("file"); eq.add_argument("--style",choices=("binary","one-hot"),default="binary")
    sw=sub.add_parser("software",help="generate a software implementation"); sw.add_argument("file"); sw.add_argument("--target",choices=("python-match","python-table","c-switch"),default="python-match")
    hd=sub.add_parser("hdl",help="generate a hardware implementation"); hd.add_argument("file"); hd.add_argument("--target",choices=("systemverilog","testbench"),default="systemverilog"); hd.add_argument("--module",default="edufsm_machine")
    tr=sub.add_parser("trace",help="record a deterministic execution trace"); tr.add_argument("file"); tr.add_argument("events",nargs="*"); tr.add_argument("--output")
    rp=sub.add_parser("replay",help="validate and replay a saved trace"); rp.add_argument("file"); rp.add_argument("trace_file")
    an=sub.add_parser("analyze",help="run structural FSM analysis"); an.add_argument("file")
    mt=sub.add_parser("model-test",help="generate reproducible model-based tests"); mt.add_argument("file"); mt.add_argument("--runs",type=int,default=10); mt.add_argument("--steps",type=int,default=100); mt.add_argument("--seed",type=int,default=0)
    args=ap.parse_args(argv)
    text=Path(args.file).read_text(encoding="utf-8")
    if args.command=="analyze":
        machine=parse(text)
        print("Unreachable:", " ".join(unreachable_states(machine)) or "(none)")
        print("Dead-end:", " ".join(dead_end_states(machine)) or "(none)")
        if machine.accepting: print("Nonproductive:", " ".join(nonproductive_states(machine)) or "(none)")
        print("Nondeterministic:", " ".join(f"{s}/{e}" for s,e in nondeterministic_pairs(machine)) or "(none)")
        print("Missing transitions:", len(machine.missing_transitions()))
        return 1 if unreachable_states(machine) or nondeterministic_pairs(machine) else 0
    if args.command=="model-test":
        machine=parse(text)
        covered,total,percent=generated_transition_coverage(machine,args.runs,args.steps,args.seed)
        print(f"Transition coverage: {covered}/{total} ({percent:.1f}%)")
        sample=generate_trace(machine,args.steps,args.seed)
        print(f"Sample final state: {sample.final}")
        return 0 if covered==total else 1
    if args.command=="trace":
        machine=parse(text); trace=record_trace(machine,args.events); payload=trace.to_json()
        if args.output: Path(args.output).write_text(payload,encoding="utf-8")
        else: print(payload,end="")
        return 0
    if args.command=="replay":
        machine=parse(text); trace=Trace.from_json(Path(args.trace_file).read_text(encoding="utf-8"))
        print(f"Final state: {replay_trace(machine,trace)}"); return 0
    if args.command=="hdl":
        machine=parse(text)
        generator=systemverilog if args.target=="systemverilog" else systemverilog_testbench
        print(generator(machine,args.module),end=""); return 0
    if args.command=="software":
        machine=parse(text)
        generators={"python-match":python_match,"python-table":python_table,"c-switch":c_switch}
        print(generators[args.target](machine),end=""); return 0
    if args.command=="nfa-accept":
        machine=parse_nfa(text); accepted=machine.accepts(args.input)
        print("ACCEPT" if accepted else "REJECT"); return 0 if accepted else 1
    if args.command=="nfa-to-dfa":
        print(dot(to_dfa(parse_nfa(text))),end=""); return 0
    if args.command in ("encode","truth-table","equations"):
        machine=parse(text)
        encoding=binary_encoding(machine) if args.style=="binary" else one_hot_encoding(machine)
        if args.command=="encode":
            print(f"Encoding: {args.style} ({encoding.bits} bit(s))")
            for state,code in encoding.codes: print(f"{state}: {code}")
            return 0
        if args.command=="equations":
            inputs=input_codes(machine)
            print("Inputs:", " ".join(f"{name}={code}" for name,code in inputs) or "(none)")
            for name,expression in next_state_equations(machine,encoding):
                print(f"{name} = {expression}")
            return 0
        print("| Present state | Input | Next state |")
        print("|---|---|---|")
        for present,event,nxt in transition_truth_table(machine,encoding):
            print(f"| {present} | {event} | {nxt} |")
        return 0
    if args.command=="moore-graph":
        print(moore_dot(parse_moore(text)),end=""); return 0
    if args.command=="mealy-graph":
        print(mealy_dot(parse_mealy(text)),end=""); return 0
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
