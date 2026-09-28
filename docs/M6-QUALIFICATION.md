# M6 Qualification — Protocols and parsers

Status: **PASS**

## Qualified baseline

- Qualified commit: `6869b27d7d22e9bc7b670d80b580f68cfa4bb384`
- GitHub Actions run: `36412389563`
- Result: **success**
- Python matrix: 3.10, 3.12 and 3.13

## Qualified examples

M6 applies FSMs to sequential input processing through four teaching examples:

- `examples/uart-receiver.fsm` — conceptual UART receive phases,
- `examples/command-parser.fsm` — line-oriented command structure,
- `examples/protocol-controller.fsm` — request/response lifecycle with error recovery,
- `examples/lexer-identifier.fsm` — simplified identifier recognizer using input classes.

## CI qualification

Every supported Python version executes the M6 examples directly:

```sh
edufsm run examples/uart-receiver.fsm low clock byte_complete high
edufsm run examples/command-parser.fsm letter letter space digit newline reset
edufsm run examples/protocol-controller.fsm request_start data request_end response_ready sent
edufsm run examples/protocol-controller.fsm request_start malformed reset
edufsm run examples/lexer-identifier.fsm letter digit letter
```

All commands pass on Python 3.10, 3.12 and 3.13.

## Educational result

M6 establishes the pipeline:

`raw input -> classification -> event -> FSM -> state/action`

It connects formal automata from M2, synchronous controllers from M4 and software execution from M5 to practical UART, parsing, protocol and lexer use cases.

The Norwegian and English lessons also cover happy paths, malformed input, invalid-state events, reset/recovery and the separation between input classification and FSM structure.

M6 is therefore qualified as **PASS**.
