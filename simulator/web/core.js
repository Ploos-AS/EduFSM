"use strict";

export function parseFSM(text) {
  const states = [];
  const transitions = [];
  let initial = null;
  const accepting = [];
  for (const raw of text.split(/\r?\n/)) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) continue;
    let m;
    if ((m = line.match(/^STATE\s+(.+)$/i))) { states.push(m[1].trim()); continue; }
    if ((m = line.match(/^INITIAL\s+(.+)$/i))) { initial = m[1].trim(); continue; }
    if ((m = line.match(/^ACCEPT\s+(.+)$/i))) { accepting.push(m[1].trim()); continue; }
    if ((m = line.match(/^(.+?)\s*\+\s*(.+?)\s*->\s*(.+)$/))) {
      transitions.push({source:m[1].trim(), event:m[2].trim(), target:m[3].trim()});
      continue;
    }
    throw new Error("Unknown FSM line: " + line);
  }
  if (!initial) throw new Error("Missing INITIAL");
  if (!states.includes(initial)) throw new Error("Unknown initial state: " + initial);
  for (const t of transitions) {
    if (!states.includes(t.source) || !states.includes(t.target)) throw new Error("Transition references unknown state");
  }
  return {states, initial, accepting, transitions};
}

export function nextState(machine, state, event) {
  const matches = machine.transitions.filter(t => t.source === state && t.event === event);
  if (matches.length === 0) throw new Error(`No transition from '${state}' for event '${event}'`);
  if (matches.length !== 1) throw new Error(`Machine is not deterministic at '${state}' / '${event}'`);
  return matches[0].target;
}

export function outgoingEvents(machine, state) {
  return [...new Set(machine.transitions.filter(t => t.source === state).map(t => t.event))];
}

export function reachableStates(machine) {
  const seen = new Set([machine.initial]);
  let changed = true;
  while (changed) {
    changed = false;
    for (const t of machine.transitions) {
      if (seen.has(t.source) && !seen.has(t.target)) { seen.add(t.target); changed = true; }
    }
  }
  return machine.states.filter(s => seen.has(s));
}
