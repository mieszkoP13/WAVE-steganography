import numpy as np
from scipy.io import wavfile
from bitarray import bitarray

class PhaseCoding():
    def __init__(self, inputFilePath: str, outputFilePath: str):
        self.inputFilePath = inputFilePath
        self.outputFilePath = outputFilePath
        self.PAD = 100
        self.PAD_CHAR = '#'

    # read wave audio file frames and convert to byte array
    # def read_wave(self):
    #     rate1,audioData1 = wavfile.read(self.inputFilePath)
    #     self.rate = rate1
    #     self.audioData = audioData1.copy()

    #     self.frame_bytes = bytearray(self.audioData)

    def text_to_bitarray(self, string):
        _bitarray = bitarray(endian='big')
        _bitarray.frombytes(string.encode('utf-8'))
        return _bitarray.tolist()

    def hide_data(self, stringToEncode):
        rate,audioData1 = wavfile.read(self.inputFilePath)
        stringToEncode = stringToEncode.ljust(self.PAD, self.PAD_CHAR)
        textLength = 8 * len(stringToEncode)

        blockLength = int(2 * 2 ** np.ceil(np.log2(2 * textLength)))
        blockNumber = int(np.ceil(audioData1.shape[0] / blockLength))
        audioData = audioData1.copy()

        # checks shape to change data to 1 axis
        if len(audioData1.shape) == 1:
            audioData.resize(blockNumber * blockLength, refcheck=False)
            audioData = audioData[np.newaxis]
        else:
            audioData.resize((blockNumber * blockLength, audioData.shape[1]), refcheck=False)
            audioData = audioData.T

        blocks = audioData[0].reshape((blockNumber, blockLength))

        # Calculate DFT using fft
        blocks = np.fft.fft(blocks)

        # calculate magnitudes
        magnitudes = np.abs(blocks)

        # create phase matrix
        phases = np.angle(blocks)

        # get phase differences
        phaseDiffs = np.diff(phases, axis=0)

        # convert string to bitarray, then to numpy.ndarray
        textInBinary = np.ravel(self.text_to_bitarray(stringToEncode))

        # Convert txt to phase differences
        textInPi = textInBinary.copy()
        textInPi[textInPi == 0] = -1
        textInPi = textInPi * -np.pi / 2

        blockMid = blockLength // 2

        # phase conversion
        phases[0, blockMid - textLength: blockMid] = textInPi
        phases[0, blockMid + 1: blockMid + 1 + textLength] = -textInPi[::-1]

        # re compute the ophase amtrix
        for i in range(1, len(phases)):
            phases[i] = phases[i - 1] + phaseDiffs[i - 1]

        # apply i-dft
        blocks = (magnitudes * np.exp(1j * phases))
        blocks = np.fft.ifft(blocks).real

        # combining all block of audio again
        audioData[0] = blocks.ravel().astype(np.int16)    

        wavfile.write(self.outputFilePath, rate, audioData.T)

    def extract_data(self):
        rate, audioData = wavfile.read(self.outputFilePath)
        textLength = self.PAD * 8
        blockLength = 2 * int(2 ** np.ceil(np.log2(2 * textLength)))
        blockMid = blockLength // 2

        # get header info
        if len(audioData.shape) == 1:
            secret = audioData[:blockLength]
        else:
            secret = audioData[:blockLength, 0]

        # get the phase and convert it to binary
        secretPhases = np.angle(np.fft.fft(secret))[blockMid - textLength:blockMid]
        secretInBinary = (secretPhases < 0).astype(np.int8)

        #  convert into characters
        secretInIntCode = secretInBinary.reshape((-1, 8)).dot(1 << np.arange(8 - 1, -1, -1))

        # combine characters to original text
        return "".join(np.char.mod("%c", secretInIntCode)).replace(self.PAD_CHAR, "")    

if(__name__ == "__main__"):
    phaseEnc1 = PhaseCoding("./sound-examples/ex1.wav","./sound-examples/ex1_PhaseCoding.wav")
    phaseEnc1.hide_data("123456111")
    print(phaseEnc1.extract_data())