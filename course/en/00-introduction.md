# 0. Introduction to finite state machines

A **finite state machine** (FSM) describes a system that is always in one of a limited number of states.

The system may change state when something happens: a button is pressed, a character arrives, a timer expires, a signal changes, or another event occurs.

## A first example: a turnstile

We start with a simple turnstile with two states:

- `Locked`
- `Unlocked`

It reacts to two events:

- `coin`
- `push`

The rules can be written like this:

| Current state | Event | Next state |
|---|---|---|
| Locked | coin | Unlocked |
| Locked | push | Locked |
| Unlocked | coin | Unlocked |
| Unlocked | push | Locked |

This is already a complete small state machine.

## Core concepts

### State

A **state** describes the situation the system is currently in.

### Event or input

An **event** is something the machine can react to.

### Transition

A **transition** describes how the machine moves from one state to another.

### Initial state

A state machine normally has a defined state in which it starts.

### Output

Some state machines also produce outputs. A traffic-light machine may, for example, have the state `GREEN`, while its output turns on the green lamp.

## Where are FSMs used?

FSMs appear throughout computing:

- digital circuits;
- CPU control logic;
- embedded systems;
- user interfaces;
- games;
- protocols;
- parsers and lexers;
- network software;
- robotics;
- automation.

## What will we learn?

This course moves from intuitive examples to formal models, software, Boolean logic, and HDL.

The goal is not only to read state diagrams. You will learn to design, analyze, implement, and test state machines yourself.

## First exercise

Think about a normal on/off switch.

1. What states does it have?
2. Which event makes it change state?
3. What is the initial state?
4. Can you describe the transitions in a table?

This is the simplest form of sequential logic: the system's next behavior depends not only on the current input, but also on what happened before.
