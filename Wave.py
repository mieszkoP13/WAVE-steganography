from scipy.io import wavfile

class Wave():
    def __init__(self, filePath: str):
        self.filePath = filePath

    # read wave audio file frames and convert to byte array
    def read_wave(self):
        rate1,audioData1 = wavfile.read(self.filePath)
        self.rate = rate1
        self.audioData = audioData1.copy()

        self.frame_bytes = bytearray(self.audioData)

    def write_wave(self, data):
        wavfile.write(self.filePath, self.rate, data)