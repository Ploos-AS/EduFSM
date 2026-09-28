# Samme system som Moore og Mealy

Den enkleste måten å forstå forskjellen på er å modellere samme system på begge måter.

Vi bruker en enkel inngangsport med to states:

- `locked`
- `unlocked`

og to hendelser:

- `coin`
- `push`

## Moore-versjonen

Se `examples/moore-turnstile.fsm`.

Her beskriver output den stabile tilstanden:

- `locked -> closed`
- `unlocked -> open`

Kjør:

```sh
edufsm moore-run examples/moore-turnstile.fsm coin push
```

Maskinen har output allerede før første input. Når state endres, endres output.

## Mealy-versjonen

Se `examples/mealy-turnstile.fsm`.

Her beskriver output hva som skjer på en overgang:

- coin i locked: `open`
- push i locked: `alarm`
- coin i unlocked: `thanks`
- push i unlocked: `close`

Kjør:

```sh
edufsm mealy-run examples/mealy-turnstile.fsm coin push
```

Før første hendelse finnes ingen transition-output å vise.

## Viktig observasjon

Disse to modellene har samme states og inputs, men outputene betyr ikke helt det samme.

Moore-outputen beskriver **hvilken modus systemet er i**.

Mealy-outputen beskriver **reaksjonen på en hendelse**.

Det er derfor ikke nok å spørre «Moore eller Mealy?». Først må vi spørre hva outputen faktisk skal representere.

## Eksperiment

Kjør begge maskinene med:

```text
coin coin push push
```

Sammenlign trace-linjene. Legg spesielt merke til gjentatte hendelser som ikke endrer state. En Mealy-maskin kan fortsatt produsere en meningsfull output på en slik overgang.
