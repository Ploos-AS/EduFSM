# Moore and Mealy machines

A finite state machine often needs **outputs** as well as state transitions. This chapter introduces the two classic output models: Moore outputs attached to states and Mealy outputs attached to transitions. The executable examples and semantics are defined by the EduFSM M3 model.

## Moore: output belongs to the state

A Moore machine computes output from the current state: `output = f(state)`.

```text
STATE red
STATE green
INITIAL red
OUTPUT red stop
OUTPUT green go
red + timer -> green
green + timer -> red
```

Entering `green` makes the output `go`. This maps naturally to digital hardware where registered state feeds output decoding logic.

## Mealy: output belongs to the transition

A Mealy machine computes output from current state and input: `output = f(state, input)`.

```text
STATE locked
STATE unlocked
INITIAL locked
locked + coin -> unlocked / open
unlocked + push -> locked / close
```

The `coin` event changes state and produces `open` on that transition.

## Why the distinction matters

A Mealy design can react directly to an input and may need fewer states. A Moore design ties outputs to registered state, which is often easier to reason about for hardware timing.

Neither model is universally better. Choose the representation that makes the intended behaviour and timing clearest.

## Exercise

Design an automatic door using both models. Inputs are `person` and `timeout`; outputs are `open` and `close`. Compare the number of states and identify exactly when each output changes.

The next milestone connects these ideas to clocks, reset, flip-flops, state registers and next-state logic.
