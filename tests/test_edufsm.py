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
        self.assertTrue(nfa.accepts("1"))

if __name__ == "__main__": unittest.main()
