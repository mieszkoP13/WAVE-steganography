from SteganographicMethod import SteganographicMethod
from Wave import Wave
import numpy as np
from bitarray import bitarray
import os

class LSB(SteganographicMethod):
    def __init__(self):
        self.PAD_CHAR = '#'

    def create_outputFile_name(self, inputFilePath: str):
        inputFileName = os.path.splitext(inputFilePath)[0] # extract file name out of file path
        return f'{inputFileName}_LSB.wav' # create output file name

    def text_to_bitarray(self, string: str):
        _bitarray = bitarray(endian='big')
        _bitarray.frombytes(string.encode('utf-8'))
        return _bitarray.tolist()
    
    def init_wave(self, inputFilePath: str):
        self.inputWave: Wave = Wave(inputFilePath)
        self.outputWave: Wave = Wave(self.create_outputFile_name(inputFilePath))
        self.inputWave.read_wave()
        self.outputWave.rate = self.inputWave.rate

    def hide_data(self, inputFilePath: str, string: str):
        self.init_wave(inputFilePath)

        # append random data to fill rest of the file
        string = string.ljust(int((len(self.inputWave.frame_bytes)-(len(string)*8*8))/8), self.PAD_CHAR)
        
        # convert text to bitarray
        bits = self.text_to_bitarray(string)

        # replace LSB of each byte
        for i, bit in enumerate(bits):
            self.inputWave.frame_bytes[i] = (self.inputWave.frame_bytes[i] & 254) | bit

        # checks shape to change dtype
        if len(self.inputWave.audioData.shape) == 1:
            self.dtype=np.int16
        else:
            self.dtype=np.int32

        self.outputWave.write_wave(np.frombuffer(self.inputWave.frame_bytes, dtype=self.dtype))

    def extract_data(self, inputFilePath: str):
        self.init_wave(inputFilePath)

        # extract the LSB of each byte
        extracted = [self.inputWave.frame_bytes[i] & 1 for i in range(len(self.inputWave.frame_bytes))]

        # convert byte array to string
        string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))

        # extract the message
        extracted = string.split(4 * self.PAD_CHAR)[0]

        return extracted