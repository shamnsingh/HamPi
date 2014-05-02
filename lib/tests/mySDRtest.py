from ..mySDR.mySDR import * 
import Queue
from ..utils.myPass import *

# Run tests here.

# Initialization
try:
    sdr = mySDR()
except IOError:
    myFail('SDR not found.')
    exit(1)    

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
    sdr.read_samples(Q, 0.1)
except IOError:
    myFail('Error while reading.')
    exit(1)

if (not Q.empty()):
    myPass('Read samples.')
else:
    myFail('Read samples.')
    exit(1)

sdr.close()
