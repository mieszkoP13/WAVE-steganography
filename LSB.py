from Wave import Wave
import numpy as np
from bitarray import bitarray
import os

class LSB():
    def __init__(self, inputFilePath: str):
        self.PAD_CHAR = '#'
        self.inputWave = Wave(inputFilePath)

        inputFileName = os.path.splitext(inputFilePath)[0] # extract file name out of file path
        outputFilePath = f'{inputFileName}_LSB.wav' # create output file name

        self.outputWave = Wave(outputFilePath)

    def text_to_bitarray(self, string):
        _bitarray = bitarray(endian='big')
        _bitarray.frombytes(string.encode('utf-8'))
        return _bitarray.tolist()

    def hide_data(self, string: str):
        self.inputWave.read_wave()
        # Append dummy data to fill out rest of the bytes.
        string = string.ljust(int((len(self.inputWave.frame_bytes)-(len(string)*8*8))/8), self.PAD_CHAR)
        
        # Convert text to bitarray
        bits = self.text_to_bitarray(string)

        # Replace LSB of each byte of the audio data by one bit from the text bit array
        for i, bit in enumerate(bits):
            self.inputWave.frame_bytes[i] = (self.inputWave.frame_bytes[i] & 254) | bit

        self.outputWave.read_wave()
        self.outputWave.write_wave(np.frombuffer(self.inputWave.frame_bytes, dtype=np.int32))

    def extract_data(self):
        self.outputWave.read_wave()

        # Extract the LSB of each byte
        extracted = [self.outputWave.frame_bytes[i] & 1 for i in range(len(self.outputWave.frame_bytes))]
        # Convert byte array back to string
        string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
        # Cut off at the filler characters
        decoded = string.split(3 * self.PAD_CHAR)[0]

        return decoded