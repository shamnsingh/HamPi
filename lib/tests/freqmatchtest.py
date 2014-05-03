from ..utils.spectrogram import *
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

m = 512 
l_thres = 0.0
u_thres = 0.8
s_thres = 1
x = np.load('lib/db/words/one.npy')
x1 = np.load('lib/db/words/two.npy')
y = return_image(x, m)[200:253]
y1 = return_image(x1, m)[200:253]

y = y - y.max() / 2
y1 = y1 - y1.max() / 2

#y[y < y.max() * l_thres] = -2 * y.max()
#y1[y1 < y1.max() * l_thres] = -2 * y1.max()

y[y > y.max() * u_thres] = y.max() * s_thres
y1[y1 > y1.max() * u_thres] = y1.max() * s_thres

plt.imshow(y, cmap=plt.cm.gray)
figure()
plt.imshow(y1, cmap=plt.cm.gray)
plt.show(block=False)

# Image autocorrelation.
Y = signal.fftconvolve(y, y[:, ::-1])[::2]
Y1 = signal.fftconvolve(y, y1[:, ::-1])[::2]
figure()
plt.imshow(Y, cmap=plt.cm.gray)
figure()
plt.imshow(Y1, cmap=plt.cm.gray)

corrY = Y.max(axis=0)
corrY1 = Y1.max(axis=0)

figure()
plt.plot(corrY)

figure()
plt.plot(corrY1)

plt.show(block=False)
raw_input("ENTER to continue...")
