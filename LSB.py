from Wave import Wave
import numpy as np
from scipy.io import wavfile
from bitarray import bitarray

class LSB():
    def __init__(self, inputFilePath: str, outputFilePath: str):
        self.PAD_CHAR = '#'
        self.wave = Wave(inputFilePath, outputFilePath)

    def text_to_bitarray(self, string):
        _bitarray = bitarray(endian='big')
        _bitarray.frombytes(string.encode('utf-8'))
        return _bitarray.tolist()

    def hide_data(self, string: str):
        self.wave.read_wave(self.wave.inputFilePath)
        # Append dummy data to fill out rest of the bytes.
        string = string.ljust(int((len(self.wave.frame_bytes)-(len(string)*8*8))/8), self.PAD_CHAR)
        
        # Convert text to bitarray
        bits = self.text_to_bitarray(string)

        # Replace LSB of each byte of the audio data by one bit from the text bit array
        for i, bit in enumerate(bits):
            self.wave.frame_bytes[i] = (self.wave.frame_bytes[i] & 254) | bit

        self.wave.write_wave(np.frombuffer(self.wave.frame_bytes, dtype=np.int32))

    def extract_data(self):
        self.wave.read_wave(self.wave.outputFilePath)

        # Extract the LSB of each byte
        extracted = [self.wave.frame_bytes[i] & 1 for i in range(len(self.wave.frame_bytes))]
        # Convert byte array back to string
        string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
        # Cut off at the filler characters
        decoded = string.split(3 * self.PAD_CHAR)[0]

        return decoded