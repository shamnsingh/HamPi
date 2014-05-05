import itertools
from ..utils.dbScrape import *
from ..utils.correlator import *

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

from numpy import *
from matplotlib.pyplot import *

# Control runtime display warning.
rcParams['figure.max_open_warning'] = 200

scraper = dbScrape()
corr = correlator()

scraper.scrape(100, 100)
scraper.normalize()

storage = scraper.storage


for word in storage.keys():
    figure(figsize=(15, 9))
    result = corr.correlate(storage[word], storage[word])
    plt.plot(result)
    leg = [word + " and " + word]
    plt.legend(leg)
    ax = plt.gca()
    ax.grid(True)
    print leg,",",max(result)

for pair in itertools.combinations(storage.keys(), 2):
    figure(figsize=(15,9))
    result = corr.correlate(storage[pair[0]], storage[pair[1]])
    plt.plot(result)
    leg = [pair[0] + " and " + pair[1]]
    plt.legend(leg)
    ax = plt.gca()
    ax.grid(True)
    print leg,",",max(result)

plt.show(block=False)
raw_input("\nPress ENTER to exit...")
