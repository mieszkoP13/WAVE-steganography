from SteganographicMethod import SteganographicMethod
from Wave import Wave
import numpy as np
from bitarray import bitarray
import os

class PhaseCoding(SteganographicMethod):
    def __init__(self):
        self.PAD = 100
        self.PAD_CHAR = '#'

    def create_outputFile_name(self, inputFilePath: str):
        inputFileName = os.path.splitext(inputFilePath)[0] # extract file name out of file path
        return f'{inputFileName}_PhaseCoding.wav' # create output file name

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

        string = string.ljust(self.PAD, self.PAD_CHAR)

        textLength = 8 * len(string)
        blockLength = int(2 * 2 ** np.ceil(np.log2(2 * textLength)))
        blockNumber = int(np.ceil(self.tempWave.audioData.shape[0] / blockLength))

        # checks shape to change data to 1 axis
        if self.tempWave.nchannels == 1:
            self.tempWave.audioData.resize(blockNumber * blockLength, refcheck=False)
            self.tempWave.audioData = self.tempWave.audioData[np.newaxis]
        else:
            self.tempWave.audioData.resize((blockNumber * blockLength, self.tempWave.audioData.shape[1]), refcheck=False)
            self.tempWave.audioData = self.tempWave.audioData.T

        blocks = self.tempWave.audioData[0].reshape((blockNumber, blockLength))

        # calculate DFT
        blocks = np.fft.fft(blocks)

        # calculate magnitudes
        magnitudes = np.abs(blocks)

        # create phase matrix
        phases = np.angle(blocks)

        # get phase differences
        phaseDiffs = np.diff(phases, axis=0)

        # convert string to bitarray, then to numpy.ndarray
        textInBinary = np.ravel(self.text_to_bitarray(string))

        # convert txt to phase differences
        textInPi = textInBinary.copy()
        textInPi[textInPi == 0] = -1
        textInPi = textInPi * -np.pi / 2

        blockMid = blockLength // 2

        # convert phases
        phases[0, blockMid - textLength: blockMid] = textInPi
        phases[0, blockMid + 1: blockMid + 1 + textLength] = -textInPi[::-1]

        # calculate phase matrix
        for i in range(1, len(phases)):
            phases[i] = phases[i - 1] + phaseDiffs[i - 1]

        # calculate inverse DFT
        blocks = (magnitudes * np.exp(1j * phases))
        blocks = np.fft.ifft(blocks).real

        # combine all blocks of audio together
        self.tempWave.audioData[0] = blocks.ravel().astype(np.int16)    

        self.outputWave.write_wave(self.tempWave.audioData.T)

    def extract_data(self, inputFilePath: str):
        self.init_wave(inputFilePath)

        textLength = self.PAD * 8
        blockLength = 2 * int(2 ** np.ceil(np.log2(2 * textLength)))
        blockMid = blockLength // 2

        # checks shape
        if self.tempWave.nchannels == 1:
            secret = self.tempWave.audioData[:blockLength]
        else:
            secret = self.tempWave.audioData[:blockLength, 0]

        # get phase -> convert to binary -> convert into characters
        secretPhases = np.angle(np.fft.fft(secret))[blockMid - textLength:blockMid]
        secretInBinary = (secretPhases < 0).astype(np.int8)
        secretInIntCode = secretInBinary.reshape((-1, 8)).dot(1 << np.arange(8 - 1, -1, -1))

        # combine to original text
        extracted = "".join(np.char.mod("%c", secretInIntCode)).split(4 * self.PAD_CHAR)[0]
        return extracted