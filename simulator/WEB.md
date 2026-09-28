# EduFSM interactive simulator

M9 turns the existing deterministic EduFSM engine into an interactive teaching surface.

## Architecture

The simulator keeps the same project rule used by the CLI and HDL flows:

1. the FSM model is the source of truth;
2. simulation semantics live in the deterministic core;
3. UI is a replaceable frontend;
4. examples remain plain `.fsm` files;
5. headless CI can validate the same behavior shown interactively.

## Browser frontend contract

The first browser frontend should provide:

- editable FSM source;
- Parse/Reset controls;
- current-state display;
- event buttons derived from valid outgoing transitions;
- transition history;
- transition table;
- generated state diagram;
- analysis panel for unreachable/dead/nonproductive states;
- import/export of `edufsm-trace-v1` traces;
- deterministic replay;
- no server requirement for normal course use.

The browser implementation must not silently invent different FSM semantics. A shared conformance corpus will compare browser behavior with the Python reference implementation.

## Progressive enhancement

The published HTML course remains readable without JavaScript. Interactive elements enhance examples when scripting is available; they are not required to read the lessons.

## Next qualification step

M9 will add a small browser implementation and conformance fixtures generated from the Python core before the interactive simulator is considered qualified.
