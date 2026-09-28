# 2. Tilstander, hendelser og overganger

En finite state machine beskriver et system ved hjelp av et begrenset antall **tilstander** og regler for hvordan systemet skifter mellom dem.

## Tilstand
En tilstand forteller hvilken situasjon systemet befinner seg i akkurat nå. En sperreport kan for eksempel være `locked` eller `unlocked`.

## Hendelse
En hendelse er noe maskinen reagerer på, for eksempel `coin` eller `push`.

## Overgang
En overgang kobler nåværende tilstand og hendelse til neste tilstand:

    locked + coin -> unlocked

Det betyr: Når maskinen er låst og mottar en mynt, blir den ulåst.

## Et enkelt minne
Samme hendelse kan bety forskjellige ting avhengig av nåværende tilstand. Tilstanden gir derfor FSM-en et enkelt minne og skiller sekvensiell oppførsel fra ren kombinatorisk logikk.

## Øvelse
Lag en maskin for en lampe med tilstandene `off` og `on` og hendelsen `button`. Tegn diagrammet, skriv overgangstabellen og uttrykk maskinen i EduFSM-formatet.
