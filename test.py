import unittest

from LSB import LSB
from PhaseCoding import PhaseCoding
 
class TestGetAreaRectangle(unittest.TestCase):
    def setUp(self):
        self.lsb: LSB = LSB()
        self.phaseEncoding: PhaseCoding = PhaseCoding()

    def test_hide_lsb(self):
        self.lsb.hide_data("./sound-examples/ex1.wav", "data to hide lsb")

        self.assertEqual(self.lsb.extract_data("./sound-examples/ex1_LSB.wav"), "data to hide lsb", "lsb metod procedure went wrong")
        
    def test_phase_coding(self):
        self.phaseEncoding.hide_data("./sound-examples/ex1.wav", "data to hide phase coding")

        self.assertEqual(self.phaseEncoding.extract_data("./sound-examples/ex1_PhaseCoding.wav"), "data to hide phase coding", "phase coding metod procedure went wrong")
 
unittest.main()