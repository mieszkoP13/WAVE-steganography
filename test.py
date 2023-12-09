import unittest
import os

from CLI import CLI
from CompareSignals import CompareSignals

TEST_SECRET_MSG = "secretmessage"
TEST_DIRECTORY = "./sound-examples/"
TEST_FILE = "ex5.wav"
TEST_PATH = TEST_DIRECTORY + TEST_FILE
 
class TestSteganographyMethods(unittest.TestCase):

    def test_lsb(self, filePath: str = TEST_PATH):
        cli1 = CLI(["-hl",filePath,TEST_SECRET_MSG])
        cli2 = CLI(["-el",cli1.lsb.create_outputFile_name(filePath)])

        with self.subTest():
            compareSignals = CompareSignals( cli1.lsb.inputWave, cli2.lsb.inputWave )
            compareSignals.plot_signal()

        #os.remove(cli1.lsb.create_outputFile_name(filePath)) # after test directory clean up   
        self.assertEqual(cli1.secretMessage, cli2.secretMessage, "lsb metod procedure went wrong")

    def test_phase_coding(self, filePath: str = TEST_PATH):
        cli1 = CLI(["-hp",filePath,TEST_SECRET_MSG])
        cli2 = CLI(["-ep",cli1.phaseEncoding.create_outputFile_name(filePath)])

        with self.subTest():
            compareSignals = CompareSignals( cli1.phaseEncoding.inputWave, cli2.phaseEncoding.inputWave )
            compareSignals.plot_signal()

        #os.remove(cli1.phaseEncoding.create_outputFile_name(filePath)) # after test directory clean up
        self.assertEqual(cli1.secretMessage, cli2.secretMessage, "phase coding metod procedure went wrong")

    def test_lsb_all(self):
        cli = CLI([])
        files = [f for f in os.listdir(TEST_DIRECTORY) if cli.valid_filetype(f)]
        
        for file in files:
            with self.subTest(file=file):
                self.test_lsb(TEST_DIRECTORY+file)

    def test_phase_coding_all(self):
        cli = CLI([])
        files = [f for f in os.listdir(TEST_DIRECTORY) if cli.valid_filetype(f)]
        
        for file in files:
            with self.subTest(file=file):
                self.test_phase_coding(TEST_DIRECTORY+file)

if __name__ == '__main__':
    unittest.main()