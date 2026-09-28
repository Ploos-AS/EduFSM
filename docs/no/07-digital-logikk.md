# Fra FSM til digital logikk

En FSM er en abstrakt modell. For å bygge den i digital maskinvare må vi representere tilstanden med bits.

## State-registeret

Tilstanden lagres i et register bygget av flip-flopper. Hvis maskinen har tre states kan en kompakt binær encoding være:

| State | Q1 Q0 |
| --- | --- |
| idle | 00 |
| run | 01 |
| done | 10 |

To flip-flopper er nok fordi to bits kan representere fire kombinasjoner.

EduFSM kan generere denne encodingen med `binary_encoding()`.

## One-hot

Et alternativ er én bit per state:

| State | bits |
| --- | --- |
| idle | 100 |
| run | 010 |
| done | 001 |

Dette bruker flere flip-flopper, men next-state-logikken kan bli enklere. Denne strategien kalles **one-hot encoding**.

## Klokken

I en synkron FSM beregner kombinatorisk logikk neste state fra:

- nåværende state
- inputs

Ved den aktive klokkeflanken kopierer state-registeret neste state inn som den nye nåværende staten.

Vi kan skrive:

`next_state = F(state, input)`

og ved klokkeflanken:

`state <= next_state`

## Reset

Reset setter state-registeret til en kjent starttilstand. I EduFSM er dette `INITIAL`-staten.

En robust hardware-design må alltid definere hva som skjer ved reset.

## Sannhetstabellen

Når states har fått bitkoder kan hver transition omskrives:

`present-state bits + input -> next-state bits`

Eksempel:

`00 + start -> 01`

Denne tabellen er utgangspunktet for å utlede boolske uttrykk for D-inngangene til state-registerets flip-flopper.

Dette kobler EduFSM direkte til EduBoolean: FSM-en bestemmer **hvilken funksjon** vi trenger, mens boolsk algebra viser **hvordan funksjonen kan realiseres med logikkporter**.

## Neste steg

Vi skal senere utvide dette til output-logikk, komplette sannhetstabeller, boolsk minimering og HDL.
