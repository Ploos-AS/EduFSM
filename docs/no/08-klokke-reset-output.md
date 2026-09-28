# Klokke, reset og output-logikk

En synkron FSM kan deles i tre hovedblokker:

1. **State-register** — flip-flopper som lagrer Q-bitene.
2. **Next-state-logikk** — kombinatorisk logikk som beregner D-bitene.
3. **Output-logikk** — logikk som beregner systemets outputs.

## En klokkeflanke

Mellom klokkeflankene kan den kombinatoriske logikken endre D-verdiene når Q eller input endres. State-registerets Q-verdi endres først på den aktive klokkeflanken.

For en D-flip-flopp:

`Q(next) = D`

EduFSM-funksjonen `clocked_step()` modellerer dette på FSM-nivå.

## Reset

Reset må bringe systemet til en definert state. EduFSM bruker `INITIAL` som reset-state og `reset_value()` viser bitmønsteret som state-registeret må lastes med.

Eksempel:

```text
STATE idle
STATE run
INITIAL idle
```

Hvis `idle=0`, er reset-verdien `0`.

## Moore-output

For en Moore-maskin er output bare en funksjon av registrert state:

`Y = G(Q)`

Derfor kan state-encoding brukes direkte til å lage en output-tabell.

Dette gir hele datapathen:

```text
             +------------------+
input ------>| next-state logic |---- D
Q ---------->|     F(Q, X)      |
             +------------------+
                       |
                       v
                 +-----------+
clock ---------->|  state    |---- Q ----> output logic G(Q) ----> output
reset ---------->| register  |
                 +-----------+
```

## Koblingen til EduBoolean

Truth table og de kanoniske SOP-uttrykkene fra EduFSM kan nå tas videre til boolsk algebra:

- forenkle uttrykk,
- identifisere felles deluttrykk,
- implementere med AND/OR/NOT,
- senere uttrykke samme logikk i HDL.

Dermed er forbindelsen komplett fra state-diagram til flip-flopper og porter.
