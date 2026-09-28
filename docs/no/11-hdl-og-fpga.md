# HDL og FPGA

En FSM i maskinvare kan deles i to hoveddeler:

1. et **tilstandsregister** som husker nåværende tilstand;
2. **kombinatorisk neste-tilstandslogikk** som beregner neste tilstand fra nåværende tilstand og inngangen.

Dette er den samme funksjonen vi tidligere har skrevet som:

`next_state = F(current_state, event)`

Forskjellen er at tilstanden nå lagres i flip-flopper og oppdateres på en klokkeedge.

## Generert SystemVerilog

EduFSM kan generere syntetiserbar SystemVerilog:

```sh
edufsm hdl examples/turnstile.fsm --target systemverilog --module turnstile
```

Generatoren bruker binær tilstandskoding fra M4. Den genererte modulen har `clk`, synkron aktiv-høy `reset`, `event_i` og `state`.

`always_ff` beskriver tilstandsregisteret. `always_comb` beskriver neste-tilstandslogikken. For en hendelse som ikke har en definert overgang, beholdes nåværende tilstand.

## Testbench og simulering

```sh
edufsm hdl examples/turnstile.fsm --target testbench --module turnstile
```

M7 bruker Icarus Verilog til å kompilere og simulere den genererte SystemVerilog-koden. Dette oppdager HDL-feil som vanlige Python-tester av tekstgeneratoren ikke kan oppdage.

## Fra FSM til FPGA

Kvalifiseringskjeden er:

```text
EduFSM
  -> SystemVerilog
  -> Icarus RTL simulation
  -> Yosys synthesis
  -> nextpnr-ice40 place and route
  -> IceStorm bitstream
```

EduFSM bruker den delte `Ploos-AS/hardware-ci` workflowen for denne kjeden. M7-fixturen bruker UPduino v3.1-profilen.

En vellykket CI-kjøring viser at FSM-en kan simuleres, syntetiseres, plasseres/rutes og bygges til en FPGA-bitstream. Det er **ikke** det samme som en fysisk test på et virkelig kort; hardware-ci rapporterer fysisk kvalifisering separat.

## Hvorfor dette er viktig for EduCPU

En CPU-kontrollenhet er i stor grad en sekvensiell beslutningsmaskin. FSM-kunnskapen her kan derfor brukes direkte til kontrollsekvenser, busstyring, instruksjonsfaser og andre kontrollblokker i EduCPU.

## Oppgaver

1. Generer SystemVerilog for `turnstile.fsm`.
2. Finn tilstandsregisteret og neste-tilstandslogikken.
3. Generer testbenchen og simuler den.
4. Endre en overgang og sammenlign generert HDL.
5. Generer HDL for trafikklyset og undersøk hvor mange tilstandsbiter som kreves.
