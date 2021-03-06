from ..utils.spectrogram import *
from ..mySDR.mySDR import *
import Queue

t = 0.25

# Read samples and continuously plot the spectrogram.
sdr = mySDR()
fs = 240e3
offset = 20e3 
fc = 443.670e6 - offset
gain = 36

Q = Queue.Queue()
sdr.set_up(fs, fc, gain)


sdr.read_samples(Q, t)
y = Q.get()
m = 128
h = figure(figsize=(15, 6))
myspectrogram_hann_ovlp(y, m, fs, fc)
show(block=False)

while (True):
    print 'Reading...'
    sdr.read_samples(Q, t)
    print 'Done reading..'
    y = Q.get()

    h = figure(figsize=(15, 6))
    myspectrogram_hann_ovlp(y, m, fs, fc)
    show(block=False)
