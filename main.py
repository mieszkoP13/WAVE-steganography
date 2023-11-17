from LSB import LSB
from PhaseCoding import PhaseCoding

if(__name__ == "__main__"):
    lsb1 = LSB("./sound-examples/ex1.wav")
    lsb1.hide_data("data to hide lsb")
    print(lsb1.extract_data())

    phaseEnc1 = PhaseCoding("./sound-examples/ex1.wav")
    phaseEnc1.hide_data("data to hide phase coding")
    print(phaseEnc1.extract_data())