# FSMs in software

The same state machine previously mapped to digital logic can also be implemented directly in software. The model does not change: we still have **state**, **events**, and **transitions**. What changes is how the transition function is implemented.

Consider:

```text
STATE idle
STATE running
INITIAL idle
idle + start -> running
running + stop -> idle
```

## 1. Enum and match/switch

The most explicit style gives each state a name in an `Enum` and writes transitions as Python `match/case` or a C `switch`.

This makes control flow easy to inspect and debug. For small controllers it is often the clearest first implementation.

```sh
edufsm software machine.fsm --target python-match
edufsm software machine.fsm --target c-switch
```

Generated code is deliberately straightforward so learners can see the correspondence between the FSM and ordinary program code.

## 2. Table-driven FSM

Instead of encoding every transition as control flow, the transition function can be stored as data:

```text
(idle, start)   -> running
(running, stop) -> idle
```

The runtime looks up `(state, event)` in the table.

```sh
edufsm software machine.fsm --target python-table
```

This separates machine description from execution and works well when many machines share one runtime or transitions are generated from a model.

## 3. Event-driven FSM

Event-driven software commonly receives events through a queue:

```text
producer -> event queue -> FSM dispatcher -> new state
```

EduFSM's `EventDrivenFSM` makes the distinction explicit. `post(event)` queues an event without changing state. `dispatch_one()` processes one event. `dispatch_all()` drains the queue in FIFO order.

The important lesson is that **receiving an event does not necessarily mean processing it immediately**.

The same pattern appears in GUIs, embedded firmware, messaging systems, protocol stacks, and servers.

## One model, several implementations

All three styles implement the same mathematical function:

`next_state = F(state, event)`

That means they can be tested against the same FSM model. The implementation style can change while the required behaviour remains the same.

## Exercise

Implement a three-state traffic light using:

1. Python `match/case`
2. a transition table
3. an event queue

Compare where state and transitions live in each implementation. Which parts are **data**, and which parts are **control flow**?
