# EduFSM

**Learn how computers make decisions over time.**

EduFSM is a beginner-friendly course about finite state machines (FSMs), automata, sequential logic, and practical state-machine design.

The course starts with everyday examples and builds toward software, digital logic, communication protocols, and FPGA/HDL implementations.

## Goals

After completing the course, a learner should be able to:

- explain states, events, transitions, inputs, and outputs;
- draw and read state diagrams;
- create transition tables;
- distinguish deterministic and nondeterministic finite automata;
- understand Moore and Mealy machines;
- translate a state machine into Boolean/sequential logic;
- implement FSMs in software;
- implement simple FSMs in HDL;
- use FSMs for parsers, protocols, controllers, and embedded systems;
- test and debug state machines systematically.

## Languages

Norwegian is the primary course language. English is maintained as a parallel language.

## Planned publishing formats

Course sources are intended to generate:

- HTML / web documentation
- EPUB
- Kindle-friendly output
- PDF

## M0 scope

M0 establishes the project foundation:

- course architecture;
- Norwegian and English source trees;
- first introductory lesson;
- example FSM descriptions;
- simulator design notes;
- publishing/build skeleton;
- licensing and contribution guidance.

## Course path

EduFSM fits naturally into the wider educational progression:

`EduNumbers -> EduBoolean -> EduFSM -> EduCPU`

EduNumbers covers representation, EduBoolean covers combinational logic, EduFSM introduces state and time, and EduCPU brings these ideas together into a processor.

## Repository layout

```text
course/
  no/               Norwegian course sources
  en/               English course sources
examples/            FSM examples
simulator/           simulator specification and future implementation
book/                publishing metadata
scripts/             build helpers
```

## Status

**M0 — Foundation**

The repository is intentionally small at this milestone. Later milestones will expand the course, simulator, exercises, diagrams, generated formats, and hardware/HDL material.

## License

Course/documentation material is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0), unless otherwise stated.

Software added to this repository is licensed under the MIT License, unless a file or directory states otherwise.
