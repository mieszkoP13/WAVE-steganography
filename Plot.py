import matplotlib.pyplot as plt
import numpy as np
from Wave import Wave

class Plot():

    def plot_compare_signals(self, wave1: Wave, wave2: Wave):

        # if file is not mono, take only first channel of the signal
        signal1 = wave1.audioData if len(wave1.audioData.shape) == 1 else wave1.audioData[:, 0]
        signal2 = wave2.audioData if len(wave2.audioData.shape) == 1 else wave2.audioData[:, 0]

        # calculate time linspaces in seconds
        signalDuration1 = wave1.audioData.shape[0]/wave1.rate
        time1 = np.linspace(0., signalDuration1, wave1.audioData.shape[0])
        signalDuration2 = wave2.audioData.shape[0]/wave2.rate
        time2 = np.linspace(0., signalDuration2, wave2.audioData.shape[0])

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
        plt.savefig("compareSignals.png")
        plt.close()

    def plot_compare_phase(self, wave1: Wave, wave2: Wave):

        spectre1 = np.fft.fft(wave1.audioData)
        freq1 = np.fft.fftfreq(wave1.audioData.size, 1/wave1.rate)
        mask1=freq1>0

        spectre2 = np.fft.fft(wave2.audioData)
        freq2 = np.fft.fftfreq(wave2.audioData.size, 1/wave2.rate)
        mask2=freq2>0

        phase1 = np.angle(spectre1[mask1])
        phase2 = np.angle(spectre2[mask2])
        phaseDiff = phase2[0:phase1.shape[0]] - phase1[0:phase1.shape[0]]

        #phaseDiffUnwrapped = np.unwrap(phaseDiff)

        plt.figure(figsize=(8, 9))
        plt.subplots_adjust(hspace=0.9)

        plt.subplot(311)

        plt.plot(freq1[mask1], phase1)
        plt.title('Wykres zależności fazy kontenera od częstotliwości')
        plt.ylabel("Faza")
        plt.xlabel("Częstotliwość [Hz]")

        plt.subplot(312)

        plt.plot(freq2[mask2], phase2)
        plt.title('Wykres zależności fazy stegokontenera od częstotliwości')
        plt.ylabel("Faza")
        plt.xlabel("Częstotliwość [Hz]")

        plt.subplot(313)

        plt.plot(freq1[mask1], phaseDiff)
        plt.title('Wykres zależności różnicy faz kontenera i stegokontenera od częstotliwości')
        plt.ylabel("Faza")
        plt.xlabel("Częstotliwość [Hz]")

        #plt.show()
        plt.savefig("comparePhase.png")
        plt.close()

    def plot_compare_time_size(self, sizeTimeDict: dict[float,int]):

        plt.figure(figsize=(8, 9))
        
        plt.plot( sizeTimeDict.keys(), sizeTimeDict.values() )
        plt.title('Wykres zależności czasu od wielkości pliku')
        plt.ylabel("Czas [s]")
        plt.xlabel("Wielkości pliku")

        #plt.show()
        plt.savefig("compareTimeSize.png")
        plt.close()