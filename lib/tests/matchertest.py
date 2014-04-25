from ..mySDR.mySDR import *
from ..fmDemod.fmDemod import *
from ..myAudio.myAudio import *
from ..db.db import *
import Queue
from ..utils.dbScrape import *

# Initiate SDR.
t = 2
sdr = mySDR()
fs = 240e3
offset = 20e3
fc = 443.670e6 - offset
gain = 30
m = 512
cutoff = 6e3 

# Initiate Queue.
Q = Queue.Queue()
sdr.set_up(fs, fc, gain)

# Initiate fmDemod and Audio.
fm = fmDemod()
player = myAudio()

database = db([], t, m, cutoff, sdr, Q, fm, player)
query = database.recordQuery()

# Initiate scraper:
scraper = dbScrape()
corr = correlator()

scraper.scrape(100, 100)
scraper.normalize()

storage = scraper.storage
query_trunc = scraper.truncateSig(query, 100, 100)
query_norm = scraper.normalizeSig(query_trunc)

corr_metric = {}

for word in storage.keys():
    figure(figsize=(15, 9))
    result = corr.correlate(query_norm, storage[word])
    plt.plot(result)
    plt.legend([word])
    ax = plt.gca()
    ax.grid(True)
    corr_metric[max(result)] = word

plt.show(block=False)
print corr_metric, '\n'
print "You said " + corr_metric[sorted(corr_metric, reverse=True)[0]]

raw_input("\nPress ENTER to exit...")
