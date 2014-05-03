from ..mySDR.mySDR import *
from ..fmDemod.fmDemod import *
from ..myAudio.myAudio import *
from ..db.db import *
import Queue
from ..utils.dbScrape import *

# Initiate SDR.
t = 1
sdr = mySDR()
fs = 256e3
offset = 20e3
fc = 443.670e6 - offset
gain = 10
m = 512
cutoff = 6e3 

# Initiate Queue.
Q = Queue.Queue()
sdr.set_up(fs, fc, gain)

# Initiate fmDemod and Audio.
fm = fmDemod()
player = myAudio()

database = db([], t, m, cutoff, sdr, Q, fm, player)
query = database.recordQuery('')

# Initiate scraper:
scraper = dbScrape()
corr = correlator()

scraper.scrape(100, 100)
scraper.normalize()

storage = scraper.storage
query_trunc = scraper.truncateSig(query, 1000, 1000)
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

# Sort metric and print out results.
sorted_metric = sorted(corr_metric, reverse=True)
max_metric = corr_metric[sorted_metric[0]]
max_thres = 0.07

if (sorted_metric[0] > max_thres):
    print "You said " + max_metric
else:
    print "Nothing matched."

raw_input("\nPress ENTER to exit...")
