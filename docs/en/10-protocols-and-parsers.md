# FSMs in protocols and parsers

State machines are especially useful when input arrives **sequentially**. A single bit, byte, or character is often not enough; its meaning depends on what came before.

The general pipeline is:

```text
raw input -> classification -> event -> FSM -> new state / action
```

This chapter applies the same idea at four levels.

## 1. UART receiver

`examples/uart-receiver.fsm` is a deliberately simplified UART model:

```text
idle -> start -> data -> stop -> idle
```

A real UART receiver must count data bits, sample at the correct times, and validate the stop bit. The FSM structure is already visible, however: a signal means different things depending on the current receive phase.

This connects M4 and M6 because clocked digital logic can implement exactly this kind of protocol FSM.

## 2. Command parser

A textual command can be presented as event classes instead of literal characters:

- `letter`
- `digit`
- `space`
- `newline`

`examples/command-parser.fsm` distinguishes `idle`, `command`, `argument`, and `ready`.

Input conceptually corresponding to:

```text
RUN 2\n
```

may first be classified as:

```text
letter letter letter space digit newline
```

The parser FSM does not need to know whether a letter was R or U. It receives only the properties relevant to the grammar.

## 3. Protocol controller

`examples/protocol-controller.fsm` models a simple request/response lifecycle:

```text
idle -> receiving -> processing -> sending -> idle
```

Receive or processing failures enter `error`; `reset` returns the controller to a known state.

Explicit states make invalid events visible. For example, `sent` is meaningful while `sending`, but not while `idle`.

## 4. Lexer as a DFA

A lexer converts characters into tokens. Before building a complete lexer, a DFA can recognize one token class.

`examples/lexer-identifier.fsm` recognizes a simplified identifier:

- first character: `letter` or `underscore`
- later characters: `letter`, `digit`, or `underscore`

M6 therefore connects directly back to M2: a DFA is not merely mathematical theory; it can be an executable recognizer inside a lexer.

## Classification as a separate layer

It is useful to separate:

```text
character 'A' -> class letter -> FSM event letter
character '7' -> class digit  -> FSM event digit
```

The FSM describes **structure**, while the classifier handles details of the input alphabet.

The same pattern works for bytes and packet types, GPIO signals, key presses, network messages, and lexer symbols.

## Test happy paths and failures

A protocol FSM should be tested with more than the expected sequence. Also test malformed input, events in the wrong state, reset/recovery, interrupted input, and repeated events.

The FSM makes these tests precise because the expected state after each event is explicit.

## Exercise

Extend the command parser with an `error` state. Decide which event sequences enter it and how the parser returns to `idle`.

Then draw the same machine as a state diagram and execute an event sequence with `edufsm run`.
