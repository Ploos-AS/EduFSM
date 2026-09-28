# Clock, reset and output logic

A synchronous FSM can be divided into three blocks: the **state register**, **next-state combinational logic**, and **output logic**.

Between active clock edges, combinational logic computes D from current Q and inputs. At the active edge the state register captures D. For a D flip-flop, `Q(next) = D`.

EduFSM's `clocked_step()` models this register-level behaviour.

## Reset

Reset establishes a defined state. EduFSM maps `INITIAL` to the reset state, and `reset_value()` returns the encoded bit pattern that the state register must load.

## Moore output logic

For a Moore machine, output is a function only of registered state:

`Y = G(Q)`

State encoding can therefore be transformed directly into an output table.

The complete conceptual datapath is:

```text
input ---> next-state logic F(Q,X) ---> D
                    ^                   |
                    |                   v
                    Q <--- state register <--- clock/reset
                    |
                    +---> output logic G(Q) ---> output
```

## Link to EduBoolean

EduFSM now supplies truth tables and canonical SOP equations. Boolean algebra can then simplify those equations and map them to AND/OR/NOT gates. Later milestones express the same design in HDL.

This completes the conceptual path from state diagram to flip-flops and gates.
