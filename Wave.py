from scipy.io import wavfile
import numpy as np

class Wave():
    def __init__(self, filePath: str):
        self.filePath = filePath

    # read wave audio file frames and convert to byte array
    def read_wave(self):
        rate1,audioData1 = wavfile.read(self.filePath)
        self.rate: int = rate1
        self.audioData:np.ndarray = audioData1.copy()

        self.frame_bytes = bytearray(self.audioData)

        self.nchannels = len(self.audioData.shape)

    def write_wave(self, data:np.ndarray):
        wavfile.write(self.filePath, self.rate, data)