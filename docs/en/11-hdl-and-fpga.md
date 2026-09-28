# HDL and FPGA

A hardware FSM can be divided into two main parts:

1. a **state register** that remembers the current state;
2. **combinational next-state logic** that computes the next state from the current state and input.

This is the same function used earlier:

`next_state = F(current_state, event)`

The difference is that state is now stored in flip-flops and updated on a clock edge.

## Generated SystemVerilog

EduFSM can generate synthesizable SystemVerilog:

```sh
edufsm hdl examples/turnstile.fsm --target systemverilog --module turnstile
```

The generator uses the binary state encoding introduced in M4. The generated module exposes `clk`, synchronous active-high `reset`, `event_i`, and `state`.

`always_ff` describes the state register. `always_comb` describes next-state logic. An event without a defined transition leaves the machine in its current state.

## Testbench and simulation

```sh
edufsm hdl examples/turnstile.fsm --target testbench --module turnstile
```

M7 uses Icarus Verilog to compile and simulate generated SystemVerilog. This catches HDL errors that ordinary Python tests of the text generator cannot detect.

## From FSM to FPGA

The qualification chain is:

```text
EduFSM
  -> SystemVerilog
  -> Icarus RTL simulation
  -> Yosys synthesis
  -> nextpnr-ice40 place and route
  -> IceStorm bitstream
```

EduFSM uses the shared `Ploos-AS/hardware-ci` workflow for this chain. The M7 fixture uses its UPduino v3.1 profile.

A successful CI run proves that the FSM can be simulated, synthesized, placed/routed, and built into an FPGA bitstream. It does **not** claim testing on a physical board; hardware-ci reports physical qualification separately.

## Why this matters for EduCPU

A CPU control unit is largely a sequential decision machine. The FSM knowledge from this course therefore transfers directly to control sequencing, bus control, instruction phases, and other control blocks in EduCPU.

## Exercises

1. Generate SystemVerilog for `turnstile.fsm`.
2. Identify the state register and next-state logic.
3. Generate the testbench and simulate it.
4. Change a transition and compare the generated HDL.
5. Generate HDL for the traffic-light machine and inspect the required state bits.
