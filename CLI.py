from LSB import LSB
from PhaseCoding import PhaseCoding

import os
import argparse
from typing import List

class CLI():
    def __init__(self, args: List[str] = None):
        self.args = args
        self.lsb: LSB = LSB()
        self.phaseEncoding: PhaseCoding = PhaseCoding()

        self.fileName: str = ""
        self.secretMessage: str = ""

        self.parser = argparse.ArgumentParser(description = "Steganography app manager")
        self.config()

    def validate_file(self, fileName: str):
        if not self.valid_path(fileName):
            print(f"Error: Invalid file path/name. Path {fileName} does not exist.")
            quit()
        elif not self.valid_filetype(fileName):
            print(f"Error: Invalid file format. {fileName} must be a .wav file.")
            quit()
        return
        
    def valid_filetype(self, fileName: str):
        return fileName.endswith('.wav')
    
    def valid_path(self, path: str):
        return os.path.exists(path)

    def hide_lsb(self):
        self.lsb.hide_data(self.fileName, self.secretMessage)
        
    def extract_lsb(self):
        print(self.lsb.extract_data(self.fileName))
        
    def hide_phase_coding(self):
        self.phaseEncoding.hide_data(self.fileName, self.secretMessage)
        
    def extract_phase_coding(self):
        print(self.phaseEncoding.extract_data(self.fileName))
        
    def show(self):
        path = self.args.show[0]
        
        if not self.valid_path(path):
            print("Error: No such directory.")
            exit()
    
        # get wav files in directory
        files = [f for f in os.listdir(path) if self.valid_filetype(f)]
        print(f"{len(files)} wav files found.")
        print('   '.join(f for f in files))
    
    def config(self):
        self.parser.add_argument("-hl", "--hide-lsb", type = str, nargs = 2,
                            metavar = ('fileName', 'secretMessage'), default = None,
                            help = "hide secret message using LSB method in specified file")
        
        self.parser.add_argument("-el", "--extract-lsb", type = str, nargs = 1,
                            metavar = "fileName", default = None,
                            help = "extract data using LSB method from specified file")
        
        self.parser.add_argument("-hp", "--hide-phase-coding", type = str, nargs = 2,
                            metavar = ('fileName', 'secretMessage'), default = None,
                            help = "hide data using Phase Coding method in specified file")
        
        self.parser.add_argument("-ep", "--extract-phase-coding", type = str, nargs = 1,
                            metavar = "fileName", default = None,
                            help = "extract data using Phase Coding method from specified file")
        
        self.parser.add_argument("-s", "--show", type = str, nargs = 1,
                            metavar = "path", default = None,
                            help = "show all wav files in specified directory path.\
                            Type '.' for current directory.")

        self.args: argparse.Namespace = self.parser.parse_args(self.args)
        
        if self.args.show != None:
            self.show()
        elif self.args.hide_lsb != None:
            self.fileName = self.args.hide_lsb[0]
            self.secretMessage = self.args.hide_lsb[1]
            self.validate_file(self.fileName)
            self.hide_lsb()
        elif self.args.extract_lsb != None:
            self.fileName = self.args.extract_lsb[0]
            self.validate_file(self.fileName)
            self.extract_lsb()
        elif self.args.hide_phase_coding != None:
            self.fileName = self.args.hide_phase_coding[0]
            self.secretMessage = self.args.hide_phase_coding[1]
            self.validate_file(self.fileName)
            self.hide_phase_coding()
        elif self.args.extract_phase_coding != None:
            self.fileName = self.args.extract_phase_coding[0]
            self.validate_file(self.fileName)
            self.extract_phase_coding()
