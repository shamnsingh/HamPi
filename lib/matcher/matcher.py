# Carries out database matching.
from ..utils.dbScrape import *
from ..utils.correlator import *
from ..utils.spectrogram import *
import numpy as np
import multiprocessing

from numpy import *
from matplotlib.pyplot import *

class matcher:

    # Fetches all data from the database at construction.
    def __init__(self, match_thres, m, fs):
       self.scraper = dbScrape()
       self.scraper.scrape(100, 100)
       self.scraper.normalize()

       self.corr = correlator()
       self.storage = self.scraper.storage
       self.match_thres = match_thres
       self.m = m
       self.fs = fs
       self.f = figure(figsize=(5, 5))
       show(block=False)

    # Carries out the actual database matching.
    def match(self, query, counter):
        query_trunc = self.scraper.truncateSig(query, 100, 100)
        query_norm = self.scraper.normalizeSig(query_trunc)

        corr_metric = {}
        self.f.clear()
        myspectrogram_hann_ovlp(query_norm, self.m, self.fs * 1.0/5.0, 0, title=str(counter))
        self.f.canvas.draw()

        for word in self.storage.keys():
           result = self.corr.correlate(query_norm, self.storage[word])
           corr_metric[max(result)] = word

        sorted_metric = sorted(corr_metric, reverse=True)
        max_word = corr_metric[sorted_metric[0]]

        if (sorted_metric[0] > self.match_thres):
            return (max_word, corr_metric)
        else:
            return (None, corr_metric)

    # Carries out the Queue matching.
    def match_Queue(self, Q):
        counter = 0
        while (not Q.empty()):
            query = Q.get()

            (max_word, corr_metric) = self.match(query, counter)
            if (max_word):
                print max_word
            else:
                print "Nothing."

            print corr_metric
            counter = counter + 1
        print 'Done matching.'
