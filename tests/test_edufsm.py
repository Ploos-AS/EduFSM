import unittest
from edufsm.parser import parse
from edufsm.render import table, dot

TEXT="""\nSTATE locked\nSTATE unlocked\nINITIAL locked\nlocked + coin -> unlocked\nunlocked + push -> locked\n"""

class EduFSMTests(unittest.TestCase):
    def test_parse_and_run(self):
        m=parse(TEXT); self.assertEqual(m.initial,"locked"); self.assertEqual(m.next_state("locked","coin"),"unlocked"); self.assertEqual(m.next_state("unlocked","push"),"locked")
    def test_missing_transition(self):
        with self.assertRaises(ValueError): parse(TEXT).next_state("locked","push")
    def test_rejects_nondeterminism(self):
        with self.assertRaises(ValueError): parse(TEXT+"locked + coin -> locked\n")

    def test_render_table(self):
        self.assertIn("| locked | coin | unlocked |", table(parse(TEXT)))

    def test_render_dot(self):
        graph=dot(parse(TEXT))
        self.assertIn('__start -> "locked"', graph)
        self.assertIn('"locked" -> "unlocked" [label="coin"]', graph)

    def test_dfa_acceptance(self):
        m=parse("""STATE ends0\nSTATE ends1\nINITIAL ends0\nACCEPT ends1\nends0 + 0 -> ends0\nends0 + 1 -> ends1\nends1 + 0 -> ends0\nends1 + 1 -> ends1\n""")
        self.assertEqual(m.alphabet, ("0","1"))
        self.assertFalse(m.accepts(""))
        self.assertTrue(m.accepts("1"))
        self.assertTrue(m.accepts("101"))
        self.assertFalse(m.accepts("1100"))

    def test_unknown_accepting_state(self):
        with self.assertRaises(ValueError):
            parse("STATE a\nACCEPT missing\n")

    def test_dfa_completeness(self):
        complete=parse("""STATE a\nSTATE b\na + 0 -> a\na + 1 -> b\nb + 0 -> a\nb + 1 -> b\n""")
        self.assertTrue(complete.is_complete)
        incomplete=parse("""STATE a\nSTATE b\na + 0 -> b\nb + 1 -> a\n""")
        self.assertFalse(incomplete.is_complete)
        self.assertEqual(incomplete.missing_transitions(), (("a","1"),("b","0")))

    def test_nfa_nondeterminism_and_epsilon(self):
        from edufsm.nfa import parse_nfa
        nfa=parse_nfa("""STATE s\nSTATE a\nSTATE yes\nINITIAL s\nACCEPT yes\ns + 0 -> s\ns + 0 -> a\na + 1 -> yes\n""")
        self.assertTrue(nfa.accepts("01"))
        self.assertTrue(nfa.accepts("001"))
        self.assertFalse(nfa.accepts("111"))
        eps=parse_nfa("""STATE s\nSTATE a\nSTATE yes\nINITIAL s\nACCEPT yes\ns + epsilon -> a\na + 1 -> yes\n""")
        self.assertEqual(eps.epsilon_closure({"s"}), frozenset({"s","a"}))
        self.assertTrue(eps.accepts("1"))

    def test_subset_construction_equivalence(self):
        from itertools import product
        from edufsm.nfa import parse_nfa, to_dfa
        nfa=parse_nfa("""STATE s\nSTATE a\nSTATE yes\nINITIAL s\nACCEPT yes\ns + 0 -> s\ns + 0 -> a\ns + 1 -> s\na + 1 -> yes\nyes + 0 -> yes\nyes + 1 -> yes\n""")
        dfa=to_dfa(nfa)
        self.assertTrue(dfa.is_complete)
        for length in range(6):
            for symbols in product("01", repeat=length):
                word="".join(symbols)
                self.assertEqual(nfa.accepts(word), dfa.accepts(word), word)

    def test_named_nfa_header_is_not_accept_directive(self):
        from edufsm.nfa import parse_nfa
        nfa=parse_nfa("""NFA contains01\nSTATE start\nSTATE accept\nINITIAL start\nACCEPT accept\nstart + 1 -> accept\n""")
        self.assertEqual(nfa.accepting, ("accept",))
        self.assertNotIn("ACCEPT", nfa.accepting)
        self.assertTrue(nfa.accepts("1"))


    def test_moore_outputs_follow_state(self):
        from edufsm.parser import parse_moore
        m=parse_moore("""STATE red
STATE green
INITIAL red
OUTPUT red stop
OUTPUT green go
red + timer -> green
green + timer -> red
""")
        self.assertEqual(m.output("red"),"stop")
        self.assertEqual(m.step("red","timer"),("green","go"))

    def test_mealy_outputs_follow_transition(self):
        from edufsm.parser import parse_mealy
        m=parse_mealy("""STATE locked
STATE unlocked
INITIAL locked
locked + coin -> unlocked / open
unlocked + push -> locked / close
""")
        self.assertEqual(m.step("locked","coin"),("unlocked","open"))
        self.assertEqual(m.step("unlocked","push"),("locked","close"))

    def test_moore_and_mealy_dot_semantics(self):
        from edufsm.parser import parse_moore, parse_mealy
        from edufsm.render import moore_dot, mealy_dot
        moore=parse_moore("STATE a\nSTATE b\nOUTPUT a off\nOUTPUT b on\na + go -> b\n")
        self.assertIn('label="a / off"',moore_dot(moore))
        mealy=parse_mealy("STATE a\nSTATE b\na + go -> b / pulse\n")
        self.assertIn('label="go / pulse"',mealy_dot(mealy))

    def test_binary_and_one_hot_state_encoding(self):
        from edufsm.digital import binary_encoding, one_hot_encoding, transition_truth_table
        m=parse("""STATE idle
STATE run
STATE done
INITIAL idle
idle + start -> run
run + finish -> done
done + reset -> idle
""")
        binary=binary_encoding(m)
        self.assertEqual(binary.bits,2)
        self.assertEqual(binary.codes,(("idle","00"),("run","01"),("done","10")))
        onehot=one_hot_encoding(m)
        self.assertEqual(onehot.bits,3)
        self.assertEqual(onehot.codes,(("idle","100"),("run","010"),("done","001")))
        self.assertEqual(transition_truth_table(m,binary)[0],("00","start","01"))

    def test_next_state_boolean_equations(self):
        from edufsm.digital import binary_encoding, input_codes, next_state_equations
        m=parse("""STATE a
STATE b
INITIAL a
a + stay -> a
a + go -> b
b + stay -> b
b + go -> a
""")
        enc=binary_encoding(m)
        self.assertEqual(input_codes(m),(("stay","0"),("go","1")))
        equations=dict(next_state_equations(m,enc))
        self.assertIn("!Q0 & X0",equations["D0"])
        self.assertIn("Q0 & !X0",equations["D0"])

    def test_clock_reset_and_moore_output_table(self):
        from edufsm.digital import binary_encoding, reset_value, clocked_step, moore_output_table
        from edufsm.parser import parse_moore
        m=parse("""STATE idle
STATE run
INITIAL idle
idle + start -> run
run + stop -> idle
""")
        enc=binary_encoding(m)
        self.assertEqual(reset_value(m,enc),"0")
        self.assertEqual(clocked_step(m,enc,"0","start"),"1")
        self.assertEqual(clocked_step(m,enc,"1","ignored",reset=True),"0")
        moore=parse_moore("""STATE off
STATE on
INITIAL off
OUTPUT off dark
OUTPUT on light
off + toggle -> on
on + toggle -> off
""")
        menc=binary_encoding(moore.machine)
        self.assertEqual(moore_output_table(moore,menc),(("0","dark"),("1","light")))


    def test_software_generators(self):
        from edufsm.software import python_match, python_table, c_switch
        m=parse("""STATE idle
STATE run
INITIAL idle
idle + start -> run
run + stop -> idle
""")
        explicit=python_match(m)
        self.assertIn("class State(Enum):",explicit)
        self.assertIn('case (State.IDLE, "start"):',explicit)
        tabled=python_table(m)
        self.assertIn('("idle", "start"): "run"',tabled)
        csrc=c_switch(m)
        self.assertIn("typedef enum {",csrc)
        self.assertIn("case EVENT_START: *state = STATE_RUN; return true;",csrc)


    def test_event_driven_runtime(self):
        from edufsm.software import EventDrivenFSM
        m=parse("""STATE idle
STATE running
INITIAL idle
idle + start -> running
running + stop -> idle
""")
        runtime=EventDrivenFSM(m)
        runtime.post("start")
        runtime.post("stop")
        self.assertEqual(runtime.state,"idle")
        self.assertEqual(runtime.pending,("start","stop"))
        self.assertEqual(runtime.dispatch_all(),(
            ("idle","start","running"),
            ("running","stop","idle"),
        ))
        self.assertEqual(runtime.state,"idle")
        self.assertEqual(runtime.pending,())


    def test_m6_command_parser_flow(self):
        m=parse("""STATE idle
STATE command
STATE argument
STATE ready
INITIAL idle
idle + letter -> command
command + letter -> command
command + space -> argument
command + newline -> ready
argument + letter -> argument
argument + digit -> argument
argument + newline -> ready
ready + reset -> idle
""")
        state=m.initial
        for event in ("letter","letter","space","letter","digit","newline"):
            state=m.next_state(state,event)
        self.assertEqual(state,"ready")
        self.assertEqual(m.next_state(state,"reset"),"idle")

    def test_m6_protocol_success_and_error_paths(self):
        m=parse("""STATE idle
STATE receiving
STATE processing
STATE sending
STATE error
INITIAL idle
idle + request_start -> receiving
receiving + data -> receiving
receiving + request_end -> processing
processing + response_ready -> sending
sending + sent -> idle
receiving + malformed -> error
error + reset -> idle
""")
        state=m.initial
        for event in ("request_start","data","request_end","response_ready","sent"):
            state=m.next_state(state,event)
        self.assertEqual(state,"idle")
        state=m.next_state("idle","request_start")
        state=m.next_state(state,"malformed")
        self.assertEqual(state,"error")
        self.assertEqual(m.next_state(state,"reset"),"idle")


    def test_m6_lexer_identifier_classes(self):
        m=parse("""STATE start
STATE identifier
STATE rejected
INITIAL start
ACCEPT identifier
start + letter -> identifier
start + underscore -> identifier
start + digit -> rejected
identifier + letter -> identifier
identifier + underscore -> identifier
identifier + digit -> identifier
rejected + letter -> rejected
rejected + underscore -> rejected
rejected + digit -> rejected
""")
        def accepts(events):
            state=m.initial
            for event in events:
                state=m.next_state(state,event)
            return state in m.accepting
        self.assertTrue(accepts(("letter","digit","letter")))
        self.assertTrue(accepts(("underscore","letter")))
        self.assertFalse(accepts(("digit","letter")))


    def test_m7_systemverilog_generator(self):
        from edufsm.hdl import systemverilog, systemverilog_testbench
        m=parse("""STATE idle
STATE running
INITIAL idle
idle + start -> running
running + stop -> idle
""")
        sv=systemverilog(m,"controller")
        self.assertIn("module controller (",sv)
        self.assertIn("always_ff @(posedge clk)",sv)
        self.assertIn("always_comb begin",sv)
        self.assertIn("if (reset) current_state <= STATE_IDLE;",sv)
        self.assertIn("EVENT_START: next_state = STATE_RUNNING;",sv)
        self.assertIn("default: next_state = STATE_IDLE;",sv)
        tb=systemverilog_testbench(m,"controller")
        self.assertIn("module controller_tb;",tb)
        self.assertIn("controller dut",tb)
        self.assertIn("$finish;",tb)

if __name__ == "__main__": unittest.main()
