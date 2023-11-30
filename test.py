import unittest

from CLI import CLI
 
class TestSteganographyMethods(unittest.TestCase):

    def test_lsb(self):
        cli1 = CLI(["-hl","./sound-examples/ex1.wav","secret message"])
        cli2 = CLI(["-el","./sound-examples/ex1_LSB.wav"])

        self.assertEqual(cli1.secretMessage, cli2.secretMessage, "lsb metod procedure went wrong")

    def test_phase_coding(self):
        cli1 = CLI(["-hp","./sound-examples/ex1.wav","secret message"])
        cli2 = CLI(["-ep","./sound-examples/ex1_PhaseCoding.wav"])

        self.assertEqual(cli1.secretMessage, cli2.secretMessage, "phase coding metod procedure went wrong")
        
unittest.main()