# EduFSM text format v1

M1 defines a deliberately small deterministic teaching format.

~~~text
# comments start with #
STATE locked
STATE unlocked
INITIAL locked
locked + coin -> unlocked
unlocked + push -> locked
~~~

## Rules

- A machine has one or more declared states.
- `INITIAL` selects the initial state. If omitted, the first declared state is used.
- A transition is `source + event -> target`.
- Source and target states must be declared.
- For M1, one `(state, event)` pair may have only one target. Duplicate pairs are rejected as non-deterministic.
- Blank lines and comments are ignored.

The v1 core intentionally does not define outputs, clocks, guards, actions or epsilon transitions. Those are later milestones rather than implicit syntax.
