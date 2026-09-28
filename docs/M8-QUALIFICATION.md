# M8 Qualification — Analysis and testing

Status: **PASS**

## Qualified functionality

- reachable and unreachable state analysis;
- dead-end state detection;
- productive and nonproductive state analysis for accepting machines;
- determinism analysis;
- completeness analysis through the existing DFA checks;
- transition coverage measurement;
- deterministic execution trace recording;
- versioned `edufsm-trace-v1` JSON serialization;
- replay with behavioral model-drift detection;
- seed-reproducible model-based test generation;
- generated transition-coverage measurement;
- `analyze`, `trace`, `replay`, and `model-test` CLI workflows;
- bilingual analysis/testing course material.

## Qualification evidence

Qualified implementation baseline:

`dd1c446a8e33ab29357c76217a7ccc5b8b7ede92`

GitHub Actions:

- EduFSM CI run `36416260914`: **PASS**
- FPGA regression qualification run `36416261528`: **PASS**

The FPGA regression is retained because M8 changes share the same package and CLI as the M7 HDL generator. Its success confirms that the previously qualified HDL/FPGA path remains operational.

## Definitions

EduFSM uses explicit terminology:

- **dead-end**: no outgoing transitions;
- **nonproductive**: cannot reach an accepting state;
- **unreachable**: cannot be reached from the initial state.

These properties are related but intentionally not treated as synonyms.

## Reproducibility

Model-based walks use an explicit seed. Saved traces record each source/event/target step and replay validates those steps against the current machine. This makes generated failures and regression traces reproducible in CI.
