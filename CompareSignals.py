import matplotlib.pyplot as plt
import numpy as np
from Wave import Wave

class CompareSignals():
    def __init__(self, wave1: Wave, wave2: Wave):
        self.wave1 = wave1
        self.wave2 = wave2

    def plot_signal(self):

        # if file is not mono, take only first channel of the signal
        signal1 = self.wave1.audioData if len(self.wave1.audioData.shape) == 1 else self.wave1.audioData[:, 0]
        signal2 = self.wave2.audioData if len(self.wave2.audioData.shape) == 1 else self.wave2.audioData[:, 0]

        # calculate time linspaces in seconds
        signalDuration1 = self.wave1.audioData.shape[0]/self.wave1.rate
        time1 = np.linspace(0., signalDuration1, self.wave1.audioData.shape[0])
        signalDuration2 = self.wave2.audioData.shape[0]/self.wave2.rate
        time2 = np.linspace(0., signalDuration2, self.wave2.audioData.shape[0])

        plt.figure(figsize=(8, 9))
        plt.subplots_adjust(hspace=0.9)

        plt.subplot(411)

        plt.plot( time1, signal1 )
        plt.title('Sygnał kontenera')
        plt.ylabel("Amplituda")
        plt.xlabel("Czas [s]")

        plt.subplot(412)

        plt.plot( time2, signal2 )
        plt.title('Sygnał stegokontenera')
        plt.ylabel("Amplituda")
        plt.xlabel("Czas [s]")

        xlim = plt.xlim()
        ylim = plt.ylim()

        plt.subplot(413)

        signalDiff = signal1[0:signal1.shape[0]]-signal2[0:signal1.shape[0]]

        plt.plot( time1, signalDiff )
        plt.title('Różnica sygnałów kontenera i stegokontenara')
        plt.ylabel("Amplituda")
        plt.xlabel("Czas [s]")

        plt.xlim(xlim)
        plt.ylim(ylim)

        plt.subplot(414)

        plt.plot( time1, signalDiff )
        plt.title('Przeskalowana różnica sygnałów kontenera i stegokontenara')
        plt.ylabel("Amplituda")
        plt.xlabel("Czas [s]")

        plt.xlim(xlim)
        plt.ylim((min(signalDiff), max(signalDiff)))

        # plt.show()
        plt.savefig("mygraph2.png")
        plt.close()
