from LSB import LSB
from PhaseCoding import PhaseCoding

if(__name__ == "__main__"):
    lsb1 = LSB("./sound-examples/ex1.wav","./sound-examples/ex1_LSB.wav")
    lsb1.hide_data("data to hide in a file")
    print(lsb1.extract_data())

    phaseEnc1 = PhaseCoding("./sound-examples/ex1.wav","./sound-examples/ex1_PhaseCoding.wav")
    phaseEnc1.hide_data("123456111")
    print(phaseEnc1.extract_data())