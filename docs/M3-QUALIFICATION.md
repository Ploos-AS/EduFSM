# M3 Qualification

EduFSM M3 — Moore and Mealy machines is qualified on GitHub Actions.

## Qualified revision

- Commit: `55e54d2c9d8f7ad76f675a2b9bfa06ce5741a80a`
- Workflow run: `36409058106`
- Python: 3.10, 3.12, 3.13

## Qualification results

All supported Python jobs passed.

The qualification covers:

- existing M1 deterministic FSM behaviour
- existing M2 DFA/NFA/epsilon/subset-construction regressions
- Moore state-output semantics
- Mealy transition-output semantics
- Moore CLI traces
- Mealy CLI traces
- side-by-side turnstile examples
- Moore Graphviz rendering using `state / output`
- Mealy Graphviz rendering using `event / output`

## Educational scope

M3 includes parallel Norwegian and English material explaining:

- outputs attached to states versus transitions
- `output = f(state)` versus `output = f(state, input)`
- timing implications
- stable-mode outputs versus event reactions
- comparison of equivalent system descriptions
- practical controller examples

Status: **PASS**
