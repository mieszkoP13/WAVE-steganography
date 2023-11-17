from scipy.io import wavfile

class Wave():
    def __init__(self, inputFilePath: str, outputFilePath: str):
        self.inputFilePath = inputFilePath
        self.outputFilePath = outputFilePath

    # read wave audio file frames and convert to byte array
    def read_wave(self, path: str):
        rate1,audioData1 = wavfile.read(path)
        self.rate = rate1
        self.audioData = audioData1.copy()

        self.frame_bytes = bytearray(self.audioData)

    def write_wave(self, data):
        wavfile.write(self.outputFilePath, self.rate, data)