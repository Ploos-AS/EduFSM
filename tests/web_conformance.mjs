import fs from "node:fs";
import {parseFSM,nextState,reachableStates} from "../simulator/web/core.js";

const data=JSON.parse(fs.readFileSync("simulator/web/conformance.json","utf8"));
if(data.format!=="edufsm-web-conformance-v1") throw new Error("bad conformance format");

for(const fixture of data.cases){
  const machine=parseFSM(fixture.source);
  if(machine.initial!==fixture.initial) throw new Error(fixture.name+": initial mismatch");
  let state=machine.initial;
  const steps=[];
  for(const event of fixture.events){
    const source=state;
    state=nextState(machine,state,event);
    steps.push({source,event,target:state});
  }
  if(state!==fixture.final) throw new Error(fixture.name+": final mismatch");
  if(JSON.stringify(steps)!==JSON.stringify(fixture.steps)) throw new Error(fixture.name+": trace mismatch");
  if(JSON.stringify(reachableStates(machine))!==JSON.stringify(fixture.reachable)) throw new Error(fixture.name+": reachability mismatch");
  console.log("PASS",fixture.name);
}
