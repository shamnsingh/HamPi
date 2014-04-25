from ..utils.dbScrape import *
import numpy as np
import matplotlib.pyplot as plt

from numpy import *
from matplotlib.pyplot import *

scraper = dbScrape()

# Drops 100 samples at the beginning and end.
scraper.scrape(100, 100)
scraper.normalize()

storage = scraper.storage

figure(figsize=(15, 6))

for word in storage.keys():
    plt.plot(storage[word])

plt.legend(storage.keys())
plt.show()
