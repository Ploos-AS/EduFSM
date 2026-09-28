# M2 Qualification

EduFSM M2 — Automata is qualified on GitHub Actions.

## Qualified revision

- Commit: `5a07788e8aba7289a18176c35419589a193e04d5`
- Workflow run: `36408448868`
- Python: 3.10, 3.12, 3.13

## Qualification results

All three Python jobs passed the M2 qualification suite, including:

- unit tests
- deterministic FSM execution
- DFA acceptance
- DFA transition-table and Graphviz rendering
- DFA completeness checking
- NFA acceptance with nondeterministic transitions
- epsilon-transition acceptance
- NFA to DFA subset construction

The subset-construction unit test also checks language equivalence between the NFA and generated DFA for all binary words of length 0 through 5.

## M2 capabilities

M2 establishes the executable automata foundation for EduFSM:

- DFA accepting states and recognition
- inferred alphabets and completeness checks
- NFA execution as sets of active states
- epsilon closure
- subset construction from NFA to DFA
- deterministic CI qualification across supported Python versions

Status: **PASS**
