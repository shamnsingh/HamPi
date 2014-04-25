# Carries out database matching.
from ..utils.dbScrape import *
from ..utils.correlator import *
import numpy as np

class matcher:

    # Fetches all data from the database at construction.
    def __init__(self):
       scraper = dbScrape()
       scraper.scrape()
       scraper.normalize()

       self.corr = correlator()
       self.storage = scraper.storage()

    # Carries out the actual database matching.
    def match(self, signal):
        metric = {}

        for word in self.storage.keys():
            metric[np.max(abs(corr.correlate(self.storage[word], signal)))] = word
