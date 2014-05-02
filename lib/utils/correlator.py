# Carries out necessary steps for signal correlation.
import numpy as np
from scipy import signal

class correlator:

    # Define and return a correlation metric.
    def correlate(self, signal1, signal2):
        conv = signal.fftconvolve(signal1, signal2[::-1])
        return conv

    # Define the frequency correlation metric.
    def correlate_1(self, signal1, signal2):
        (signal1, signal2) = self.zero_pad(signal1, signal2)
        spec1 = np.fft.fftshift(np.fft.fft(signal1))
        spec2 = np.fft.fftshift(np.fft.fft(signal2)[::-1])
        conv = signal.fftconvolve(spec1, spec2)
        return abs(conv)

    # Zero pad the signals.
    def zero_pad(self, signal1, signal2):
        diff = len(signal1) - len(signal2)

        if (diff > 0):
            signal2 = np.concatenate([signal2, np.zeros(diff)])
        else:
            signal1 = np.concatenate([signal1, np.zeros(-1 * diff)])

        return (signal1, signal2)
