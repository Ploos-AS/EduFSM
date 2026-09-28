# FSM-er i programvare

Den samme state-maskinen vi tidligere bygget som digital logikk kan også implementeres direkte i programvare. Forskjellen er ikke selve modellen: vi har fortsatt **state**, **events** og **transitions**. Forskjellen er hvordan transition-funksjonen realiseres.

Vi bruker denne enkle maskinen:

```text
STATE idle
STATE running
INITIAL idle
idle + start -> running
running + stop -> idle
```

## 1. Enum og match/switch

Den mest eksplisitte varianten gir hver state et navn i en `Enum` og skriver transitions som `match/case` i Python eller `switch` i C.

Fordelen er at kontrollflyten er lett å lese og debugge. For små kontrollere er dette ofte den beste første implementasjonen.

EduFSM kan vise Python-versjonen:

```sh
edufsm software machine.fsm --target python-match
```

og C-versjonen:

```sh
edufsm software machine.fsm --target c-switch
```

Legg merke til at generert kode er bevisst enkel. Målet er å vise forbindelsen mellom FSM-diagrammet og vanlig programkode.

## 2. Table-driven FSM

I stedet for å kode hver transition som kontrollflyt kan vi lagre transition-funksjonen som data:

```text
(idle, start)   -> running
(running, stop) -> idle
```

Programmet slår opp `(state, event)` i tabellen. Dette skiller maskinens struktur fra motoren som utfører den.

```sh
edufsm software machine.fsm --target python-table
```

Dette mønsteret passer særlig godt når mange maskiner skal bruke samme runtime, eller når transitions genereres fra en modell.

## 3. Event-driven FSM

I et eventdrevet program kommer events ofte fra en kø:

```text
producer -> event queue -> FSM dispatcher -> new state
```

`EventDrivenFSM` i EduFSM viser dette eksplisitt. `post(event)` legger et event i køen uten å endre state. `dispatch_one()` behandler ett event. `dispatch_all()` tømmer køen i FIFO-rekkefølge.

Dette skillet er viktig: **å motta et event er ikke nødvendigvis det samme som å behandle det med én gang**.

Samme idé brukes i GUI-programmer, embedded firmware, meldingssystemer, protokollstakker og servere.

## Hva er likt?

Alle tre implementasjonene realiserer samme matematiske funksjon:

`next_state = F(state, event)`

Derfor kan vi teste dem mot den samme FSM-modellen. Implementasjonsmønsteret kan endres uten at den ønskede oppførselen endres.

## Øvelse

Implementer en trafikklys-FSM på tre måter:

1. Python `match/case`
2. transition-tabell
3. event-kø

Sammenlign hvor state og transitions befinner seg i hver implementasjon. Hvilken del er **data**, og hvilken del er **kontrollflyt**?
