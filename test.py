import unittest
import os

from CLI import CLI

TEST_SECRET_MSG = "secret message"
TEST_DIRECTORY = "./sound-examples/"
TEST_FILE = "ex1.wav"
TEST_PATH = TEST_DIRECTORY + TEST_FILE
 
class TestSteganographyMethods(unittest.TestCase):

    def test_lsb(self, filePath: str = TEST_PATH):
        cli1 = CLI(["-hl",filePath,TEST_SECRET_MSG])
        cli2 = CLI(["-el",cli1.lsb.create_outputFile_name(filePath)])

        os.remove(cli1.lsb.create_outputFile_name(filePath)) # after test directory clean up   
        self.assertEqual(cli1.secretMessage, cli2.secretMessage, "lsb metod procedure went wrong")

    def test_phase_coding(self, filePath: str = TEST_PATH):
        cli1 = CLI(["-hp",filePath,TEST_SECRET_MSG])
        cli2 = CLI(["-ep",cli1.phaseEncoding.create_outputFile_name(filePath)])

        os.remove(cli1.phaseEncoding.create_outputFile_name(filePath)) # after test directory clean up
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