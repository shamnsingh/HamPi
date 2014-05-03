# Carries out database matching.
from ..utils.dbScrape import *
from ..utils.correlator import *
from ..utils.spectrogram import *
import numpy as np
import multiprocessing
import threading

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
       self.f = figure(figsize=(6, 8))
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

        sorted_metric = corr_metric.items()
        sorted_metric.sort(reverse=True)
        max_word = corr_metric[sorted_metric[0][0]]

        
        if (sorted_metric[0][0] > self.match_thres):
            return (max_word, sorted_metric)
        else:
            return (None, sorted_metric)

    # Carries out the Queue matching.
    def match_Queue(self, Q, executor, match_N=2):
        # Match decides how much data to skip in vicinity.
        
        counter = 0
        match = 0
        while (1):
            query = Q.get()

            if (match == 0):
                (max_word, sorted_metric) = self.match(query, counter)
               
            else:
                (max_word, sorted_metric) = (None, None)

            if (max_word):
                print str(counter), ': ', max_word
                match = match_N
                 
                # Initiates the action of the command.
                t_action = threading.Thread(target = executor.action, args = (max_word,))
                t_action.start()
            else:
                print str(counter), ': ', 'Nothing.'

            match = match - 1 if (match != 0) else match
            print sorted_metric, '\n'
            counter = counter + 1
        print 'Done matching.'
