# Analysis, testing, and reproducibility

An FSM is small enough that we can often analyze the complete model rather than only testing a few examples. This makes state machines especially useful for learning systematic testing.

## Reachability

A state is **reachable** when some transition sequence leads from the initial state to it. A declared state that can never be reached is **unreachable**.

```sh
edufsm analyze examples/turnstile.fsm
```

Unreachable states often indicate a modeling mistake, although they may also occur temporarily during development.

## Dead-end and nonproductive states

EduFSM distinguishes two concepts:

- **dead-end state**: has no outgoing transitions;
- **nonproductive state**: in a machine with accepting states, no accepting state can be reached from it.

The distinction matters: a state can contain a loop and therefore not be a dead end while still being nonproductive.

## Completeness and determinism

A deterministic FSM must have at most one transition for each state/event pair. A complete DFA additionally has a transition for every alphabet symbol from every state.

EduFSM analyzes both properties. Missing transitions are not necessarily errors in a general control FSM, but they should be understood and handled deliberately.

## Transition coverage

Transition coverage measures how many of the model's transitions a test has actually visited.

A test with 100% transition coverage has visited every transition at least once. This does not prove the system is defect-free, but it provides a concrete measure of exercised FSM structure.

## Trace and replay

EduFSM can save an execution as a versioned machine-readable trace:

```sh
edufsm trace examples/turnstile.fsm coin push --output run.json
edufsm replay examples/turnstile.fsm run.json
```

The `edufsm-trace-v1` format stores source, event, and target for every step. Replay validates every step against the current model. A behavioral model change is therefore detected.

This makes traces useful as regression artifacts and for debugging.

## Model-based testing

```sh
edufsm model-test examples/turnstile.fsm --runs 10 --steps 100 --seed 42
```

The generator selects only valid transitions from the current state. The seed makes execution deterministic and reproducible. When a generated CI test fails, the exact event sequence can be reproduced.

## Invariants

An invariant is a property that must always hold. Examples include:

- the system is always in a declared state;
- a locked door opens only after the correct event;
- a protocol does not send a response before a request is complete.

FSM analysis, traces, and model-based testing provide a strong foundation for checking such properties.

## Exercises

1. Create an FSM with one unreachable state and find it with `analyze`.
2. Create a dead-end state.
3. Create an accepting machine with a nonproductive loop.
4. Save a trace, change a transition, and try replay.
5. Run model-based testing twice with the same seed.
6. Try to reach 100% transition coverage.
