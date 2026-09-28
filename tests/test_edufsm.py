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

if __name__ == "__main__": unittest.main()
