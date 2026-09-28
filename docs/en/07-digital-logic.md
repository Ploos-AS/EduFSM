# From FSM to digital logic

An FSM is abstract. Hardware must represent its state using bits stored in flip-flops.

## State register

For three states, compact binary encoding can use two bits:

| State | Q1 Q0 |
| --- | --- |
| idle | 00 |
| run | 01 |
| done | 10 |

EduFSM generates this with `binary_encoding()`.

## One-hot encoding

One-hot uses one flip-flop per state: `idle=100`, `run=010`, `done=001`. It costs more storage but can simplify next-state logic.

## Clock and next state

Combinational logic computes:

`next_state = F(state, input)`

At the active clock edge, the state register captures that result:

`state <= next_state`

## Reset

Reset establishes a known state. In EduFSM the `INITIAL` state is the natural reset state.

## Truth table

After encoding, a transition becomes:

`present-state bits + input -> next-state bits`

For example:

`00 + start -> 01`

These rows are the starting point for deriving Boolean equations for the D inputs of the state-register flip-flops.

This connects EduFSM directly to EduBoolean: the FSM defines **the required function**, while Boolean algebra explains **how to implement that function with logic gates**.

Later M4 work expands this into output logic, complete truth tables, Boolean minimization and HDL-oriented representations.
