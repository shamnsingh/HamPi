# Implements the demodulation scheme.

import numpy as np
from scipy import signal

class fmDemod:

    # Demodulate the given signal.
    def demod(self, y):
        y_n = y[1:]
        y_n_minus_1 = y[0:len(y) - 1]

        prod = y_n * y_n_minus_1.conjugate()
        x = np.angle(prod)
        return x

    # Filter the signal using the cutoff.
    def filter(self, y, taps, cutoff, fs):
        h = signal.firwin(taps, cutoff, nyq=fs * 1.0 / 2)
        out = signal.convolve(y, h)
        return out

    # Downsample the signal by a given amount.
    def downSample(self, y, D):
        return y[::D]

    # Completely demodulate the signal.
    def completeDemod(self, y, taps, cutoff, fs, D):
        return self.downSample(self.filter(self.demod(y), taps, cutoff, fs), D)
