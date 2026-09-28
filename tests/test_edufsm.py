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

if __name__ == "__main__": unittest.main()
