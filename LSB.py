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
        self.tempWave: Wave = Wave(inputFilePath)
        self.outputWave: Wave = Wave(self.create_outputFile_name(inputFilePath))
        
        self.inputWave.read_wave()
        self.tempWave.read_wave()
        self.outputWave.rate = self.inputWave.rate

    def hide_data(self, inputFilePath: str, string: str):
        self.init_wave(inputFilePath)

        # append random data to fill rest of the file
        string = string.ljust(int(np.floor(len(self.tempWave.frameBytes)/16))-len(string), self.PAD_CHAR)
        
        # convert text to bitarray
        bits = self.text_to_bitarray(string)

        if len(bits) > len(self.tempWave.frameBytes)*2:
            raise ValueError("Message is too large to hide in the audio file")

        id = 0
        # replace LSB of each byte
        for i, bit in enumerate(bits):
            self.tempWave.frameBytes[id] = (self.tempWave.frameBytes[id] & 254) | bit
            id = id + 2

        newAudioData = np.frombuffer(self.tempWave.frameBytes, dtype=np.int16)

        audioDataList = []
        for i in range(0, len(newAudioData), self.tempWave.nchannels):
            item = np.array(newAudioData[i:i+self.tempWave.nchannels])
            audioDataList.append( item )

        audioDataNumpyArray = np.array(audioDataList, np.int16)
        
        self.outputWave.write_wave(audioDataNumpyArray)

    def extract_data(self, inputFilePath: str):
        self.init_wave(inputFilePath)

        # extract the LSB of each byte
        extracted = [self.tempWave.frameBytes[i] & 1 for i in range(0,len(self.tempWave.frameBytes),2)]

        # convert byte array to string
        string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))

        # extract the message
        extracted = string.split(4 * self.PAD_CHAR)[0]

        return extracted