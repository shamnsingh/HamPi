from ..utils.spectrogram import *
import numpy as np
import matplotlib.pyplot as plt

m = 512
x = np.load('lib/db/words/one.npy')
y = return_image(x, m)
plt.imshow(y, cmap=plt.cm.gray), plt.show()
