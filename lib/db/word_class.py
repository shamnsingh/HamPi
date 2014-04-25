# Represents the word class.
import numpy as np

class word_class:

    def __init__(self, text, signal):
        self.word = text
        self.signal = signal

    # Save word locally.

    def save(self, path):
        np.save(path + self.word + '.npy', self.signal)
