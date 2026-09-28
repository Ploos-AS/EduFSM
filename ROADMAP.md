# EduFSM Roadmap

## M0 — Foundation

- [x] Establish course goals and repository structure
- [x] Norwegian as primary language
- [x] English parallel course tree
- [x] First introductory lesson
- [x] First machine-readable FSM example
- [x] Simulator architecture/contract
- [x] Publishing targets documented

## M1 — Core state-machine concepts — PASS

- [x] states, events, transitions and outputs
- [x] state diagrams and transition tables
- [x] initial/final states
- [x] deterministic execution
- [x] exercises and solutions
- [x] first runnable simulator

## M2 — Automata — PASS

- [x] DFA
- [x] NFA
- [x] epsilon transitions
- [x] NFA to DFA conversion
- [x] executable recognizers

Qualification: `docs/M2-QUALIFICATION.md`

Simple lexical examples continue in M6 together with parsers and lexer examples.

## M3 — Moore and Mealy machines — PASS

- [x] output semantics
- [x] comparative examples
- [x] practical controller designs
- [x] executable Moore and Mealy traces
- [x] Graphviz diagrams

Qualification: `docs/M3-QUALIFICATION.md`

## M4 — Sequential digital logic

- clocks and reset
- flip-flops and state registers
- next-state logic
- state encoding
- Boolean derivation
- links to EduBoolean

## M5 — FSMs in software

- enums and switch/match implementations
- table-driven machines
- event-driven systems
- C and Python implementations

## M6 — Protocols and parsers

- UART receiver
- command parser
- simple protocol controller
- lexer examples

## M7 — HDL and FPGA

- Verilog/SystemVerilog implementation
- simulation/testbench
- synthesis-oriented design
- links to EduCPU hardware progression

## M8 — Analysis and testing

- unreachable/dead states
- completeness and determinism checks
- transition coverage
- trace/replay
- model-based tests

## M9 — Publishing and interactive course

- HTML site
- EPUB
- Kindle-friendly output
- PDF
- interactive simulator integration
- generated diagrams and exercises
