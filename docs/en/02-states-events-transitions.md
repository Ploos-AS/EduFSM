# 2. States, events and transitions

A finite state machine describes a system using a finite set of **states** and rules for moving between them.

A **state** describes the current situation. An **event** is something the machine reacts to. A **transition** connects the current state and event to the next state.

    locked + coin -> unlocked

The current state acts as a small amount of memory: the meaning of an event may depend on what happened before.

## Exercise
Design a lamp with states `off` and `on` and event `button`. Draw its diagram, create its transition table, then express it using the EduFSM format.
