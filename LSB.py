from scipy.io import wavfile
import numpy as np

class LSB():
    def __init__(self, inputFilePath: str, outputFilePath: str):
        self.inputFilePath = inputFilePath
        self.outputFilePath = outputFilePath

    # read wave audio file frames and convert to byte array
    def read_wave(self):
        rate1,audioData1 = wavfile.read(self.inputFilePath)
        self.rate = rate1
        self.audioData = audioData1.copy()

        self.frame_bytes = bytearray(self.audioData)

    def hide_data(self, string):
        # Append dummy data to fill out rest of the bytes.
        string = string + int((len(self.frame_bytes)-(len(string)*8*8))/8) *'#'
        # Convert text to bit array
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
        #print(bits)

        # Replace LSB of each byte of the audio data by one bit from the text bit array
        for i, bit in enumerate(bits):
            self.frame_bytes[i] = (self.frame_bytes[i] & 254) | bit

        wavfile.write(self.outputFilePath, self.rate, np.frombuffer(self.frame_bytes, dtype=np.int32))

    def extract_data(self):
        rate1,audioData1 = wavfile.read(self.outputFilePath)
        self.rate = rate1
        self.audioData = audioData1.copy()

        self.frame_bytes = bytearray(self.audioData)

        # Extract the LSB of each byte
        extracted = [self.frame_bytes[i] & 1 for i in range(len(self.frame_bytes))]
        # Convert byte array back to string
        string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
        # Cut off at the filler characters
        decoded = string.split("###")[0]

        return decoded


if(__name__ == "__main__"):
    lsb1 = LSB("./sound-examples/ex1.wav","./sound-examples/ex1_secret.wav")
    lsb1.read_wave()
    lsb1.hide_data("data to hide in a file")
    print(lsb1.extract_data())