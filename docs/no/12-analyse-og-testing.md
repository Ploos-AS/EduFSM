# Analyse, testing og reproduksjon

En FSM er liten nok til at vi ofte kan analysere hele modellen, ikke bare teste noen få eksempler. Det gjør state machines spesielt nyttige for å lære systematisk testing.

## Reachability

En tilstand er **reachable** når det finnes en sekvens av overganger fra initialtilstanden til den. En deklarert tilstand som aldri kan nås er **unreachable**.

```sh
edufsm analyze examples/turnstile.fsm
```

Unreachable states er ofte tegn på en feil i modellen, men kan også være midlertidige under utvikling.

## Dead-end og nonproductive

EduFSM skiller mellom to begreper:

- **dead-end state**: har ingen utgående overganger;
- **nonproductive state**: i en maskin med accept-states kan ingen accept-state nås derfra.

Dette skillet er viktig: en tilstand kan ha en loop og dermed ikke være dead-end, men fortsatt være nonproductive.

## Completeness og determinisme

En deterministisk FSM skal ha høyst én overgang for hvert par av tilstand og hendelse. En komplett DFA har dessuten en overgang for hvert symbol i alfabetet fra hver tilstand.

EduFSM analyserer begge egenskapene. Manglende overganger trenger ikke alltid være feil i en generell kontroll-FSM, men de må forstås og håndteres bevisst.

## Transition coverage

Transition coverage måler hvor mange av modellens overganger en test faktisk har besøkt.

En test som når 100 % transition coverage har besøkt alle overganger minst én gang. Det betyr ikke automatisk at systemet er feilfritt, men det gir et konkret mål for hvor mye av FSM-strukturen testen har utført.

## Trace og replay

EduFSM kan lagre en kjøring som et versjonert, maskinlesbart spor:

```sh
edufsm trace examples/turnstile.fsm coin push --output run.json
edufsm replay examples/turnstile.fsm run.json
```

Formatet `edufsm-trace-v1` lagrer source, event og target for hvert steg. Replay validerer hvert steg mot dagens modell. Hvis modellen har endret oppførsel, blir forskjellen oppdaget.

Dette gjør traces nyttige som regresjonsartefakter og ved feilsøking.

## Model-based testing

```sh
edufsm model-test examples/turnstile.fsm --runs 10 --steps 100 --seed 42
```

Generatoren velger bare gyldige overganger fra gjeldende tilstand. Seed gjør kjøringen deterministisk og reproducerbar. Når en generert test feiler i CI, kan nøyaktig samme hendelsesforløp kjøres igjen.

## Invariants

En invariant er en egenskap som alltid skal være sann. Eksempler:

- systemet er alltid i en deklarert tilstand;
- en låst dør åpnes bare etter riktig hendelse;
- en protokoll sender ikke svar før forespørselen er komplett.

FSM-analyse, traces og model-based testing gir et godt fundament for å teste slike egenskaper.

## Oppgaver

1. Lag en FSM med én unreachable state og finn den med `analyze`.
2. Lag en dead-end state.
3. Lag en accept-maskin med en nonproductive loop.
4. Lagre en trace, endre en overgang og prøv replay.
5. Kjør model-based testing med samme seed to ganger.
6. Forsøk å oppnå 100 % transition coverage.
