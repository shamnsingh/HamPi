from ..utils.spectrogram import *
from ..mySDR.mySDR import *
from ..fmDemod.fmDemod import *
from ..myAudio.myAudio import *
from numpy.fft import *
import Queue

t = 2
sdr = mySDR()
fs = 240e3
offset = 20e3
fc = 443.670e6 - offset
gain = 10
m = 128

Q = Queue.Queue()
sdr.set_up(fs, fc, gain)

raw_input("Press ENTER and record sound for " + str(t) + " seconds. ")

sdr.read_samples(Q, t)
y = Q.get()

figure(figsize=(15, 6))
myspectrogram_hann_ovlp(y, m, fs, fc)

fm = fmDemod()
data = fm.completeDemod(y, 128, 20e3, fs, 1)
data_ds = fm.completeDemod(y, 128, 20e3, fs, 5)

show()

player = myAudio()

player.play_audio(data_ds, 48000)

player.terminate()

print "Computing DFT..."

omega = (fs * 1.0 / 2) * np.linspace(-1, 1, len(data))
figure(figsize=(15, 6))
plt.plot(omega, abs(fftshift(fft(data))))
show()

raw_input("Press ENTER...")
