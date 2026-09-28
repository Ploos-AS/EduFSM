# M4 Qualification — Sequential digital logic

Status: **PASS**

## Qualified baseline

- Qualified commit: `0910607ba72d8e9c7dc98d72602b296b49ec747b`
- GitHub Actions run: `36409568124`
- Result: **success**
- Python matrix: 3.10, 3.12 and 3.13

## Qualified capabilities

M4 establishes the complete educational path from a deterministic FSM to synchronous digital logic:

- compact binary state encoding,
- one-hot state encoding,
- encoded transition truth tables,
- encoded input symbols,
- canonical sum-of-products next-state equations for D flip-flop inputs,
- reset value derived from the `INITIAL` state,
- clocked state-register stepping,
- Moore output tables derived from encoded state,
- Norwegian and English lessons covering state registers, clock, reset, next-state logic and output logic.

## Architecture taught

A synchronous FSM is presented as three cooperating blocks:

1. **State register** — flip-flops storing the present-state bits `Q`.
2. **Next-state logic** — combinational logic implementing `D = F(Q, X)`.
3. **Output logic** — for a Moore machine, `Y = G(Q)`.

At the active clock edge the state register captures D. Reset loads the encoding of the declared initial state.

## EduBoolean bridge

EduFSM deliberately emits canonical Boolean expressions rather than hiding the derivation behind optimization. These expressions are suitable input for the Boolean-algebra material in EduBoolean, where learners can simplify them and map them to AND/OR/NOT gates.

This keeps the responsibilities clear:

- EduFSM: derive the required logic from machine behaviour.
- EduBoolean: understand and simplify the Boolean logic.
- EduCPU / later HDL work: implement the resulting synchronous circuit.

## Evidence

The qualified CI baseline exercises the complete repository test suite and command-line qualification commands. The M4 tests specifically cover state encoding, next-state equations, reset, clocked stepping and Moore output mapping.

M4 is therefore qualified as **PASS**.
