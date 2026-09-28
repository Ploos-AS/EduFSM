# 3. Deterministiske endelige automater (DFA)

En **DFA** er en finite state machine brukt til å avgjøre om en sekvens av symboler hører til et bestemt språk.

Vi trenger fem deler: et endelig sett tilstander, et alfabet, en overgangsfunksjon, én starttilstand og et sett aksepterende tilstander.

Tenk på en maskin som skal godta binære strenger som slutter på `1`. Alfabetet er `{0, 1}`. Etter at hele strengen er lest, avgjør maskinens siste tilstand om strengen aksepteres.

## Deterministisk

For hver kombinasjon av tilstand og symbol finnes nøyaktig én neste tilstand. Maskinen trenger derfor aldri å gjette hvilken vei den skal gå.

## Eksempel

For språket «binære strenger som slutter på 1» kan vi bruke to tilstander: `ends0` og `ends1`. `ends1` er aksepterende.

| Tilstand | 0 | 1 |
|---|---|---|
| ends0 | ends0 | ends1 |
| ends1 | ends0 | ends1 |

Prøv strengene `0`, `1`, `101`, `1100` og den tomme strengen. For hver streng: følg overgangene for hånd og avgjør om slutt-tilstanden er aksepterende.

## Fra NFA til DFA

En NFA kan konverteres til en DFA med **subset construction**. Én DFA-tilstand representerer da et helt sett av NFA-tilstander. Starttilstanden er epsilon-closure av NFA-starttilstanden. For hvert symbol finner vi alle mulige måltilstander, tar epsilon-closure igjen, og dette settet blir én ny DFA-tilstand. En slik DFA-tilstand er aksepterende dersom settet inneholder minst én aksepterende NFA-tilstand.

EduFSM viser settene direkte som navn, for eksempel `{start,saw0}`. Prøv `edufsm nfa-to-dfa examples/nfa-contains-01.fsm` for å generere Graphviz DOT.
