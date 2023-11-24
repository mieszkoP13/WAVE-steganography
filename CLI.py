from LSB import LSB
from PhaseCoding import PhaseCoding

import os
import argparse

INVALID_FILETYPE_MSG = "Error: Invalid file format. %s must be a .wav file."
INVALID_PATH_MSG = "Error: Invalid file path/name. Path %s does not exist."

class CLI():
    def __init__(self):
        pass

    def validate_file(self, file_name):
        if not self.valid_path(file_name):
            print(INVALID_PATH_MSG%(file_name))
            quit()
        elif not self.valid_filetype(file_name):
            print(INVALID_FILETYPE_MSG%(file_name))
            quit()
        return
        
    def valid_filetype(self, file_name):
        return file_name.endswith('.wav')
    
    def valid_path(self, path):
        return os.path.exists(path)

    def hide_lsb(self, args):
        self.lsb1 = LSB(args.file_path[0])
        self.lsb1.hide_data("data to hide lsb")
        
    def extract_lsb(self, args):
        self.lsb1 = LSB(args.file_path[0])
        print(self.lsb1.extract_data())
        
    def hide_phase_coding(self, args):
        self.phaseEnc1 = PhaseCoding(args.file_path[0])
        self.phaseEnc1.hide_data("data to hide phase coding")
        
    def extract_phase_coding(self, args):
        self.phaseEnc1 = PhaseCoding(args.file_path[0])
        print(self.phaseEnc1.extract_data())
        
    def show(self, args):
        dir_path = args.show[0]
        
        if not self.valid_path(dir_path):
            print("Error: No such directory found.")
            exit()
    
        # get wav files in directory
        files = [f for f in os.listdir(dir_path) if self.valid_filetype(f)]
        print("{} wav files found.".format(len(files)))
        print('\n'.join(f for f in files))
    
    def config(self):
        # create parser object
        parser = argparse.ArgumentParser(description = "Steganography methods manager")

        # defining arguments for parser object
        parser.add_argument("-hl", "--hide-lsb", action='store_true', default = None,
                            help = "If wave file is specified, hide data in it using LSB method.")
        
        parser.add_argument("-el", "--extract-lsb", action='store_true', default = None,
                            help = "If wave file is specified, extract data from it using LSB method.")
        
        parser.add_argument("-hp", "--hide-phase-coding", action='store_true', default = None,
                            help = "If wave file is specified, hide data in it using Phase Coding method.")
        
        parser.add_argument("-ep", "--extract-phase-coding", action='store_true', default = None,
                            help = "If wave file is specified, extract data from it using Phase Coding method.")
        
        parser.add_argument("-fp", "--file-path", type = str, nargs = 1,
                            metavar = "file_name", default = None,
                            help = "Specifies file path to use in hide/extract methods.")
        
        parser.add_argument("-s", "--show", type = str, nargs = 1,
                            metavar = "path", default = None,
                            help = "Shows all wav files in specified directory path.\
                            Type '.' for current directory.")

        args = parser.parse_args()
        
        if args.show != None:
            self.show(args)
        elif args.file_path != None:
            if args.hide_lsb != None:
                self.hide_lsb(args)
            elif args.extract_lsb != None:
                self.extract_lsb(args)
            elif args.hide_phase_coding != None:
                self.hide_phase_coding(args)
            elif args.extract_phase_coding != None:
                self.extract_phase_coding(args)


if __name__ == "__main__":
    cli = CLI()
    cli.config()
    