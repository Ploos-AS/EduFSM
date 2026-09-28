# The same system as Moore and Mealy

A useful way to understand the distinction is to model the same turnstile with both approaches.

The machine has two states, `locked` and `unlocked`, and two events, `coin` and `push`.

## Moore version

See `examples/moore-turnstile.fsm`.

Its outputs describe stable modes: `locked -> closed` and `unlocked -> open`.

```sh
edufsm moore-run examples/moore-turnstile.fsm coin push
```

The machine has an output before the first input because output is a property of state.

## Mealy version

See `examples/mealy-turnstile.fsm`.

Its outputs describe reactions to events: `open`, `alarm`, `thanks`, and `close`.

```sh
edufsm mealy-run examples/mealy-turnstile.fsm coin push
```

There is no transition output before the first event.

## Key observation

The machines have the same states and inputs, but their outputs do not mean exactly the same thing.

Moore output describes **the mode the system is in**. Mealy output describes **the reaction to an event**.

So the design question is not merely “Moore or Mealy?” First decide what the output is intended to represent.

## Experiment

Run both machines with:

```text
coin coin push push
```

Compare the traces, especially events that leave the state unchanged. A Mealy transition can still produce a meaningful output even when no state change occurs.
