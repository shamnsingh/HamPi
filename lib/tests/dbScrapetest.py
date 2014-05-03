from ..utils.spectrogram import *
from ..utils.dbScrape import *
import numpy as np
import matplotlib.pyplot as plt

from numpy import *
from matplotlib.pyplot import *

m = 512
fs = 256e3 

scraper = dbScrape()

# Drops 100 samples at the beginning and end.
scraper.scrape(100, 100)
#scraper.normalize()

storage = scraper.storage

figure(figsize=(15, 6))

for word in storage.keys():
    plt.plot(storage[word])

plt.legend(storage.keys())
plt.show()

for word in storage.keys():
    figure(figsize=(3, 6))
    myspectrogram_hann_ovlp(storage[word], m, fs * 1.0 / 5.0, 0,title=word)

plt.show(block=False)

raw_input('ENTER to exit...')
