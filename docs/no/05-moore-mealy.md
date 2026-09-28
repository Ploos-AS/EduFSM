# Moore- og Mealy-maskiner

En vanlig FSM beskriver hvilken tilstand systemet går til. I praktiske systemer trenger vi også **utganger**: et trafikklys skal tenne en lampe, en lås skal åpne en dør, og en protokollmaskin skal sende et signal.

Moore- og Mealy-maskiner er to klassiske måter å knytte utganger til en tilstandsmaskin.

## Moore: utgangen hører til tilstanden

I en Moore-maskin bestemmes utgangen bare av gjeldende tilstand.

| Tilstand | Utgang |
| --- | --- |
| red | stop |
| green | go |

Et enkelt EduFSM-eksempel:

```text
STATE red
STATE green
INITIAL red
OUTPUT red stop
OUTPUT green go
red + timer -> green
green + timer -> red
```

Når maskinen går fra `red` til `green`, blir den nye utgangen `go`.

Dette er lett å tenke på i digital elektronikk: state-registeret bestemmer utgangen gjennom ren dekodingslogikk.

## Mealy: utgangen hører til overgangen

I en Mealy-maskin avhenger utgangen av både gjeldende tilstand og hendelsen som mottas.

```text
STATE locked
STATE unlocked
INITIAL locked
locked + coin -> unlocked / open
unlocked + push -> locked / close
```

Her betyr `/ open` at hendelsen `coin` både flytter maskinen til `unlocked` og produserer utgangen `open`.

## Den viktige forskjellen

For en Moore-maskin kan vi skrive:

`output = f(state)`

For en Mealy-maskin:

`output = f(state, input)`

Det betyr at en Mealy-maskin kan reagere med en utgang direkte på en input uten først å måtte representere reaksjonen som en egen state. En Moore-modell kan derfor noen ganger trenge flere states for samme observerbare oppførsel.

Moore-modeller har på sin side en nyttig egenskap i maskinvare: utgangene er direkte knyttet til registrert state og er derfor ofte enklere å resonnere om med hensyn til timing.

## Timing

Anta at systemet er i state `locked` og mottar `coin`.

En Mealy-maskin kan produsere `open` som en del av behandlingen av akkurat denne overgangen.

En Moore-maskin må uttrykke `open` som output fra en state. Outputen endres dermed når den registrerte staten endres.

Dette skillet blir spesielt viktig når vi senere implementerer FSM-er med klokker og flip-flopper.

## Når bruker vi hva?

Det finnes ingen universell regel om at én modell alltid er best.

Moore er ofte naturlig når:
- output beskriver en stabil systemmodus,
- outputs bør følge registrert state,
- enkel timinganalyse er viktig.

Mealy er ofte naturlig når:
- systemet skal reagere direkte på hendelser,
- outputs representerer handlinger på transitions,
- vi ønsker å unngå ekstra states bare for kortvarige reaksjoner.

## Øvelse

Design en automatisk dør på begge måter.

Input:
- `person`
- `timeout`

Outputs:
- `open`
- `close`

1. Lag først en Moore-maskin.
2. Lag deretter en Mealy-maskin.
3. Sammenlign antall states.
4. Marker nøyaktig når output endres.
5. Forklar hvilken modell du synes beskriver systemet tydeligst — og hvorfor.

I neste del kobler vi dette direkte til sekvensiell digital logikk: klokke, reset, flip-flopper, state-register og next-state-logikk.
