# 3. Deterministic finite automata (DFA)

A **DFA** is a finite state machine used to decide whether a sequence of symbols belongs to a language.

It has five parts: a finite set of states, an alphabet, a transition function, one initial state, and a set of accepting states.

For a DFA, every state/symbol pair has exactly one next state. There is no choice or guessing.

## Example

A DFA recognizing binary strings ending in `1` can use states `ends0` and `ends1`, where `ends1` is accepting.

| State | 0 | 1 |
|---|---|---|
| ends0 | ends0 | ends1 |
| ends1 | ends0 | ends1 |

Trace `0`, `1`, `101`, `1100`, and the empty string by hand, then decide whether the final state is accepting.
