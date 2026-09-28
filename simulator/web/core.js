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
    if (line.toLowerCase().startsWith("machine ")) continue;
    if ((m = line.match(/^STATE\s+(.+)$/i))) { states.push(m[1].trim()); continue; }
    if ((m = line.match(/^INITIAL\s+(.+)$/i))) { initial = m[1].trim(); continue; }
    if ((m = line.match(/^ACCEPT\s+(.+)$/i))) { accepting.push(m[1].trim()); continue; }
    if (line.toLowerCase().startsWith("transition ")) {
      const parts = line.split(/\\s+/);
      if (parts.length !== 4) throw new Error("Invalid transition line: " + line);
      transitions.push({source:parts[1], event:parts[2], target:parts[3]});
      continue;
    }
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


export function traceObject(machine, steps) {
  return {
    format: "edufsm-trace-v1",
    initial: machine.initial,
    steps: steps.map(s => ({source:s.source,event:s.event,target:s.target}))
  };
}

export function replayTrace(machine, trace) {
  if (trace.format !== "edufsm-trace-v1") throw new Error("Unsupported EduFSM trace format");
  if (trace.initial !== machine.initial) throw new Error("Trace initial state does not match machine initial state");
  let state=machine.initial;
  for (let i=0;i<trace.steps.length;i++) {
    const step=trace.steps[i];
    if(step.source!==state) throw new Error(`Trace step ${i} source mismatch`);
    const target=nextState(machine,state,step.event);
    if(target!==step.target) throw new Error(`Trace step ${i} target mismatch`);
    state=target;
  }
  return state;
}

export function transitionTable(machine) {
  return machine.transitions.map(t => ({source:t.source,event:t.event,target:t.target}));
}


export function diagramLayout(machine) {
  const n=Math.max(machine.states.length,1);
  const cx=300, cy=210, radius=Math.min(150,45*n);
  const nodes=machine.states.map((state,i)=>{
    const angle=-Math.PI/2 + 2*Math.PI*i/n;
    return {state,x:cx+radius*Math.cos(angle),y:cy+radius*Math.sin(angle)};
  });
  const positions=Object.fromEntries(nodes.map(n=>[n.state,n]));
  const edges=machine.transitions.map(t=>({
    ...t,
    x1:positions[t.source].x, y1:positions[t.source].y,
    x2:positions[t.target].x, y2:positions[t.target].y
  }));
  return {width:600,height:420,nodes,edges};
}
