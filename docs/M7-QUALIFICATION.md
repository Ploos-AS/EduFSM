# M7 Qualification — HDL and FPGA

Status: **PASS**

## Qualified functionality

- synthesizable SystemVerilog generation from deterministic EduFSM machines;
- synchronous state register and combinational next-state logic;
- generated simulation testbench;
- Icarus Verilog compilation and RTL simulation;
- Yosys synthesis;
- nextpnr-ice40 place and route using the UPduino v3.1 profile;
- IceStorm bitstream generation;
- reusable FPGA qualification through `Ploos-AS/hardware-ci@v1`;
- bilingual HDL/FPGA course material and EduCPU progression link.

## Qualification evidence

Qualified implementation baseline:

`8956e501319cbd083a5f4414ff813c36ff71a799`

GitHub Actions:

- EduFSM CI run `36414675615`: **PASS**
- FPGA qualification run `36414676292`: **PASS**

The reusable FPGA job successfully completed:

1. board-profile validation;
2. UPduino v3.1 toolchain installation;
3. RTL test target;
4. canonical FPGA bitstream build;
5. bitstream verification;
6. qualification report generation;
7. bitstream artifact upload;
8. qualification report artifact upload.

The synthesis log reported no Yosys design-check problems.

## Scope

This qualification proves automated RTL simulation, synthesis, place-and-route, and bitstream generation. It does not claim physical testing on an UPduino board. The shared hardware-ci workflow deliberately records physical board qualification separately.
