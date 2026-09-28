# FSM-er i protokoller og parsere

State-maskiner er spesielt nyttige når input kommer **sekvensielt**. En enkelt bit, byte eller karakter forteller ofte ikke nok; betydningen avhenger av hva som kom tidligere.

Den generelle kjeden er:

```text
rå input -> klassifisering -> event -> FSM -> ny state / handling
```

Dette kapitlet viser den samme ideen på fire nivåer.

## 1. UART receiver

`examples/uart-receiver.fsm` er en bevisst forenklet UART-modell:

```text
idle -> start -> data -> stop -> idle
```

En ekte UART-mottaker må telle databits, sample på riktige tidspunkt og kontrollere stop-bit. Men FSM-strukturen er allerede synlig: betydningen av et signal avhenger av hvilken fase mottakeren er i.

Dette er forbindelsen mellom M4 og M6: clocked digital logikk kan implementere akkurat denne typen protokoll-FSM.

## 2. Command parser

En tekstkommando kan behandles som event-klasser i stedet for konkrete tegn:

- `letter`
- `digit`
- `space`
- `newline`

`examples/command-parser.fsm` skiller mellom `idle`, `command`, `argument` og `ready`.

For input som konseptuelt tilsvarer:

```text
RUN 2\n
```

kan et tidligere lag produsere:

```text
letter letter letter space digit newline
```

Parser-FSM-en trenger dermed ikke vite om bokstaven var R eller U. Den arbeider med de egenskapene som er relevante for grammatikken.

## 3. Protocol controller

`examples/protocol-controller.fsm` modellerer livssyklusen til en enkel request/response-protokoll:

```text
idle -> receiving -> processing -> sending -> idle
```

Feil under mottak eller behandling går til `error`, og `reset` bringer controlleren tilbake til en kjent tilstand.

Dette viser hvorfor eksplisitte states er nyttige: ugyldige hendelser blir synlige. `sent` gir for eksempel mening i `sending`, men ikke i `idle`.

## 4. Lexer som DFA

En lexer oversetter tegn til tokens. Før vi bygger en full lexer kan vi bruke en DFA til å gjenkjenne én tokenklasse.

`examples/lexer-identifier.fsm` gjenkjenner en forenklet identifier:

- første tegn: `letter` eller `underscore`
- senere tegn: `letter`, `digit` eller `underscore`

Dermed knytter M6 seg direkte tilbake til M2: en DFA er ikke bare matematikk; den kan være en kjørbar recognizer i en lexer.

## Klassifisering er et eget lag

Det er nyttig å skille:

```text
character 'A' -> class letter -> FSM event letter
character '7' -> class digit  -> FSM event digit
```

Da beskriver FSM-en **struktur**, mens klassifiseringslaget beskriver detaljene i input-alfabetet.

Samme mønster fungerer for:

- bytes og packet types,
- GPIO-signaler,
- tastetrykk,
- nettverksmeldinger,
- lexer-symboler.

## Test både happy path og feil

En protokoll-FSM bør ikke bare testes med den forventede sekvensen. Test også:

- malformed input,
- events i feil state,
- reset/recovery,
- tom eller avbrutt input,
- repeterte events.

FSM-modellen gjør slike tester presise fordi forventet state etter hvert event er eksplisitt.

## Øvelse

Utvid command-parseren med en `error`-state. Bestem hvilke event-sekvenser som skal føre dit, og hvordan parseren kan komme tilbake til `idle`.

Tegn deretter samme maskin som state-diagram og kjør eventsekvensen med `edufsm run`.
