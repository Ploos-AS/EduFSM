# 0. Introduksjon til finite state machines

En **finite state machine** (FSM), eller **endelig tilstandsmaskin**, beskriver et system som til enhver tid befinner seg i én av et begrenset antall tilstander.

Systemet kan skifte tilstand når noe skjer: en knapp trykkes, et tegn mottas, en timer utløper, et signal endres eller en annen hendelse oppstår.

## Et første eksempel: en låst port

Vi starter med en enkel adgangsport med to tilstander:

- `Låst`
- `Ulåst`

Porten reagerer på to hendelser:

- `mynt`
- `dytt`

Reglene kan beskrives slik:

| Nåværende tilstand | Hendelse | Neste tilstand |
|---|---|---|
| Låst | mynt | Ulåst |
| Låst | dytt | Låst |
| Ulåst | mynt | Ulåst |
| Ulåst | dytt | Låst |

Dette er allerede en komplett liten state machine.

## De viktigste begrepene

### Tilstand

En **tilstand** beskriver hvilken situasjon systemet er i akkurat nå.

### Hendelse eller input

En **hendelse** er noe som kan få systemet til å reagere.

### Overgang

En **overgang** beskriver hvordan systemet går fra én tilstand til en annen.

### Starttilstand

En state machine må vanligvis ha en definert tilstand den starter i.

### Output

Noen state machines produserer også output. En trafikklys-maskin kan for eksempel ha tilstanden `GRØNN`, mens outputen er at den grønne lampen er på.

## Hvor brukes FSM-er?

FSM-er finnes overalt i computing:

- digitale kretser;
- CPU-kontrollogikk;
- embedded-systemer;
- brukergrensesnitt;
- spill;
- protokoller;
- parsere og lexere;
- nettverksprogramvare;
- robotikk;
- automasjon.

## Hva skal vi lære?

I dette kurset går vi fra intuitive eksempler til formelle modeller, programvare, boolsk logikk og HDL.

Målet er ikke bare å kunne lese et state diagram. Du skal etter hvert kunne designe, analysere, implementere og teste state machines selv.

## Første øvelse

Tenk på en vanlig av/på-bryter.

1. Hvilke tilstander har den?
2. Hvilken hendelse får den til å bytte tilstand?
3. Hva er starttilstanden?
4. Kan du skrive overgangene som en tabell?

Dette er den enkleste formen for sekvensiell logikk: systemets neste oppførsel avhenger ikke bare av input, men også av hva som har skjedd tidligere.
