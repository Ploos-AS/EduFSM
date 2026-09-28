"""Generate synthesizable SystemVerilog from deterministic EduFSM machines."""

from .digital import binary_encoding, input_codes
from .model import Machine

def _ident(name: str) -> str:
    value="".join(ch if ch.isalnum() else "_" for ch in name)
    if not value or value[0].isdigit():
        value="_"+value
    return value.upper()

def systemverilog(machine: Machine, module: str="edufsm_machine") -> str:
    """Generate a compact synchronous SystemVerilog FSM."""
    states=binary_encoding(machine)
    events=input_codes(machine)
    event_bits=max(1,len(events[0][1]) if events else 1)
    lines=[f"module {module} (","    input  logic clk,","    input  logic reset,",f"    input  logic [{event_bits-1}:0] event,",f"    output logic [{states.bits-1}:0] state",");","",f"  typedef enum logic [{states.bits-1}:0] {{"]
    lines.append(",\n".join(f"    STATE_{_ident(name)} = {states.bits}'b{code}" for name,code in states.codes))
    lines += ["  } state_t;","","  state_t current_state, next_state;",""]
    if events:
        lines += [f"  typedef enum logic [{event_bits-1}:0] {{",",\n".join(f"    EVENT_{_ident(name)} = {event_bits}'b{code}" for name,code in events),"  } event_t;",""]
    lines += ["  assign state = current_state;","","  always_ff @(posedge clk) begin",f"    if (reset) current_state <= STATE_{_ident(machine.initial)};","    else       current_state <= next_state;","  end","","  always_comb begin","    next_state = current_state;","    unique case (current_state)"]
    by_state={state:[] for state in machine.states}
    for t in machine.transitions: by_state[t.source].append(t)
    for state in machine.states:
        lines.append(f"      STATE_{_ident(state)}: begin")
        if by_state[state]:
            lines.append("        unique case (event)")
            for t in by_state[state]: lines.append(f"          EVENT_{_ident(t.event)}: next_state = STATE_{_ident(t.target)};")
            lines += ["          default: ;","        endcase"]
        lines.append("      end")
    lines += [f"      default: next_state = STATE_{_ident(machine.initial)};","    endcase","  end","","endmodule",""]
    return "\n".join(lines)

def systemverilog_testbench(machine: Machine, module: str="edufsm_machine") -> str:
    """Generate a minimal simulation bench that exercises every transition."""
    states=binary_encoding(machine)
    events=input_codes(machine)
    event_map=dict(events)
    event_bits=max(1,len(events[0][1]) if events else 1)
    lines=[f"module {module}_tb;","  logic clk = 0;","  logic reset = 1;",f"  logic [{event_bits-1}:0] event = '0;",f"  logic [{states.bits-1}:0] state;",f"  {module} dut (.clk(clk), .reset(reset), .event(event), .state(state));","  always #5 clk = ~clk;","  initial begin","    @(posedge clk);","    reset <= 0;"]
    for t in machine.transitions:
        lines += ["    reset <= 1; @(posedge clk); reset <= 0;",f"    force dut.current_state = dut.STATE_{_ident(t.source)};",f"    event <= {event_bits}'b{event_map[t.event]};","    @(posedge clk);","    release dut.current_state;"]
    lines += ["    $finish;","  end","endmodule",""]
    return "\n".join(lines)
