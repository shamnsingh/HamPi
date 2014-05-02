from ..utils.spectrogram import *
from ..mySDR.mySDR import *
from ..fmDemod.fmDemod import *
from ..myAudio.myAudio import *
from numpy.fft import *
import Queue

t = 2
sdr = mySDR()
fs = 256e3
offset = 20e3
fc = 443.670e6 - offset
gain = 10
m = 1024 

Q = Queue.Queue()
sdr.set_up(fs, fc, gain)

print("\nSDR is reading at fc: " + str(fc / 1e6) + " MHz.")
raw_input("Press ENTER and record sound for " + str(t) + " seconds. ")

sdr.read_samples(Q, t)
y = Q.get()

print 'Read ', str(len(y)), ' samples.'


figure(figsize=(15, 6))
myspectrogram_hann_ovlp(y, m, fs, fc)

fm = fmDemod()
data = fm.completeDemod(y, 128, 20e3, fs, 1)
data_ds = fm.completeDemod(y, 128, 20e3, fs, 5)

player = myAudio()

player.play_audio(data_ds, 48000)

player.terminate()

figure(figsize=(15, 6))
myspectrogram_hann_ovlp(data_ds, m, fs * 1.0 / 5, 0)

figure(figsize=(15, 6))
plt.plot(data_ds)

print "Computing DFT..."

omega = (fs * 1.0 / 2) * np.linspace(-1, 1, len(data))
figure(figsize=(15, 6))
plt.plot(omega, abs(fftshift(fft(data))))
show()

raw_input("Press ENTER...")
