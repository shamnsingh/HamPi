from ..mySDR.mySDR import *
from ..fmDemod.fmDemod import *
from ..myAudio.myAudio import *
from ..db.db import *
import Queue

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

words = ['email', 'text', 'call']

database = db(words, t, m, cutoff, sdr, Q, fm, player)
database.construct()
player.terminate()
