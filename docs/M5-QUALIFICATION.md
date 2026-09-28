# M5 Qualification — FSMs in software

Status: **PASS**

## Qualified baseline

- Qualified commit: `eedb513dc2119aea79fbc67ec8e05e9b236c6f34`
- Software-generator CI run: `36411674490`
- Latest full baseline run: `36411711879`
- Result: **success**
- Python matrix: 3.10, 3.12 and 3.13

## Qualified capabilities

M5 demonstrates several direct software implementations of the same deterministic FSM model:

- Python `Enum` plus `match/case`,
- table-driven Python transitions,
- C `enum` plus nested `switch`,
- queued event-driven execution,
- FIFO event dispatch,
- deterministic event traces,
- CLI generation of Python and C examples,
- Norwegian and English lessons comparing the implementation patterns.

## CLI qualification

The CI matrix explicitly executes:

```sh
edufsm software examples/turnstile.fsm --target python-match
edufsm software examples/turnstile.fsm --target python-table
edufsm software examples/turnstile.fsm --target c-switch
```

All three commands pass on Python 3.10, 3.12 and 3.13.

## Event-driven model

`EventDrivenFSM` separates event arrival from event processing:

- `post()` appends to the queue,
- `dispatch_one()` consumes one event,
- `dispatch_all()` drains the queue in FIFO order,
- state changes only during dispatch.

Tests verify queue contents, ordering, transitions and the resulting deterministic trace.

## Educational result

M5 makes an important connection explicit: enum/switch code, transition tables and event loops are different implementations of the same transition function:

`next_state = F(state, event)`

This lets learners move from the formal FSM model to ordinary application and embedded software without changing the underlying reasoning.

M5 is therefore qualified as **PASS**.
