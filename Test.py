import unittest
import time
import os

from CLI import CLI
from Plot import Plot

PLOT_COMPARE_SIGNALS = False
PLOT_COMPARE_PHASE = False
CLEAN_UP_DIRECTORY = True
TEST_SECRET_MSG = "secretmesssdfjsjfsdhsfhasjidjpia!@#!@$#@$*fsdh23423423"
TEST_DIRECTORY = "./wave-dataset/Korg-DS-8-Sci-Fi-Sound-Effects-Pack/"
TEST_FILE = "glitch14.wav"
TEST_PATH = TEST_DIRECTORY + TEST_FILE
 
class TestSteganographyMethods(unittest.TestCase):

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        self.endTime = time.time()
        self.elapsedTime = round(self.endTime - self.startTime, 4)

    def test_lsb(self, filePath: str = TEST_PATH):
        cli1 = CLI(["-hl",filePath,TEST_SECRET_MSG])
        cli2 = CLI(["-el",cli1.lsb.create_outputFile_name(filePath)])

        if PLOT_COMPARE_SIGNALS:
            with self.subTest():
                compareSignals = Plot()
                compareSignals.plot_compare_signals( cli1.lsb.inputWave, cli2.lsb.inputWave )

        if PLOT_COMPARE_PHASE:
            with self.subTest():
                phase = Plot()
                phase.plot_compare_phase( cli1.lsb.inputWave, cli2.lsb.inputWave )

        if CLEAN_UP_DIRECTORY:
            os.remove(cli1.lsb.create_outputFile_name(filePath))

        self.assertEqual(cli1.secretMessage, cli2.secretMessage, "lsb metod procedure went wrong")

    def test_phase_coding(self, filePath: str = TEST_PATH):
        cli1 = CLI(["-hp",filePath,TEST_SECRET_MSG])
        cli2 = CLI(["-ep",cli1.phaseCoding.create_outputFile_name(filePath)])

        if PLOT_COMPARE_SIGNALS:
            with self.subTest():
                compareSignals = Plot()
                compareSignals.plot_compare_signals( cli1.phaseCoding.inputWave, cli2.phaseCoding.inputWave )

        if PLOT_COMPARE_PHASE:
            with self.subTest():
                phase = Plot()
                phase.plot_compare_phase( cli1.phaseCoding.inputWave, cli2.phaseCoding.inputWave )

        if CLEAN_UP_DIRECTORY:
            os.remove(cli1.phaseCoding.create_outputFile_name(filePath))

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