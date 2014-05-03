# Carries out necessary steps for signal correlation.
import numpy as np
from scipy import signal
from spectrogram import *

class correlator:

    # Define and return a correlation metric.
    def correlate(self, signal1, signal2):
        conv = signal.fftconvolve(signal1, signal2[::-1])
        return conv

    # Defines the image correlation metric.
    def correlate1(self, signal1, signal2, m=512):
        y1 = return_image(signal1, m)[200:253]
        y2 = return_image(signal2, m)[200:253]

        y1[y1 < y1.max() * 0.2] = 1j
        y2[y2 < y2.max() * 0.2] = 1j

        y1[y1 > y1.max() * 0.7] = y1.max() * 20
        y2[y2 > y2.max() * 0.7] = y2.max() * 20

        # Image autocorrelation.
        Y = signal.fftconvolve(y1, y2[:, ::-1])[::2]

        corrY = Y.max(axis=0)

        return corrY.real
