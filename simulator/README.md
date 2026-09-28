# EduFSM Simulator

The EduFSM simulator will be a small deterministic teaching tool for finite state machines.

## M0 contract

The simulator should eventually support:

- loading a simple text-based `.fsm` format;
- validating declared states and transitions;
- selecting an initial state;
- injecting events one at a time;
- printing every state transition;
- rejecting or clearly reporting invalid events;
- deterministic execution with no dependency on wall-clock time;
- non-interactive execution for tests and CI;
- interactive execution for learners.

A future implementation should keep the state-machine engine separate from its CLI/UI so the same core can later power web, terminal, visualization, and course tooling.

## Example session

```text
$ edufsm run examples/turnstile.fsm
machine: turnstile
state: locked

> coin
locked -> unlocked

> push
unlocked -> locked
```

## Planned later capabilities

- state-diagram generation;
- transition-table generation;
- unreachable-state analysis;
- missing/ambiguous-transition checks;
- trace recording and replay;
- test-vector execution;
- Moore and Mealy outputs;
- DFA/NFA support;
- export to C and Python;
- export to Verilog/SystemVerilog;
- visualization suitable for the web course.

M0 defines direction only; implementation belongs to a later milestone.
