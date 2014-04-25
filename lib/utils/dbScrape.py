# Fetch all words stored and return dict representation.
from correlator import *
import os
import re
import numpy as np


class dbScrape:
    path = 'lib/db/words'
    p = re.compile('[a-z]+')
    storage = {}
    corr = correlator()

    def scrape(self, begin, end):
        for word in os.listdir(self.path):
            label = self.p.match(word).group()
            signal = np.load(self.path + "/" + word)

            self.storage[label] = signal[begin:-1 * end]

    # Makes the average of each speech signal to be 0.
    def normalize(self):
        for word in self.storage.keys():
            arr = self.storage[word] - np.mean(self.storage[word])
            arr = arr * 1.0 / np.sqrt(np.max(abs(self.corr.correlate(arr, arr))))
            self.storage[word] = arr

    # Truncates a given signal.
    def truncateSig(self, sig, begin, end):
        return sig[begin:-1 * end]

    # Normalizes a given signal.
    def normalizeSig(self, sig):
        arr = sig - np.mean(sig)
        return arr * 1.0 / np.sqrt(np.max(abs(self.corr.correlate(arr, arr))))
