from ..mySDR import mySDR
import Queue
from myPass import *

# Run tests here.

# Initialization
sdr = mySDR.mySDR()

if (sdr != None):
    myPass('Found SDR.')
else:
    myFail('Found SDR.')
    exit(1)

# Reading
fs = 240e3
fc = 94.1e6
gain = 36

Q = Queue.Queue()
sdr.set_up(fs, fc, gain)

try:
    sdr.read_samples(Q, 256000 * 1)
except IOError:
    myFail('Error while reading.')
    exit(1)

if (not Q.empty()):
    myPass('Read samples.')
else:
    myFail('Read samples.')
    exit(1)
