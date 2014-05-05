# Import functions and libraries
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import Queue
import threading,time
import sys

from numpy import pi
from numpy import sin
from numpy import zeros
from numpy import r_
from scipy import signal
from scipy import integrate

import threading,time
import multiprocessing

%matplotlib inline

def genPTT(plen,zlen,fs):
    Nz = floor(zlen*fs)
    Nt = floor(plen*fs)
    pttsig = zeros(Nz)
    t=r_[0.0:Nt]/fs
    pttsig[:Nt] = 0.5*sin(2*pi*t*2000)
    return pttsig

def genPulse(Npulse, f0, fs):
    #     Function generates an analytic function of a chirp pulse
    #     Inputs:
    #             Npulse - pulse length in samples
    #             f0     - frequency of pulse
    #             fs     - sampling frequency
    
    t1 = r_[0.0:Npulse]/fs
    Tpulse = float32(Npulse) / fs 
    f_of_t = f0
    phi_of_t = 2*pi*np.cumsum(f_of_t)/fs
    pulse = exp(1j* phi_of_t )
    return pulse


# Acknowledger class that sends an acknowledgement with:
#     a = acknowledger(fc)
#     a.run(command)
class acknowledger():
    def __init__(self, frequency):
        self.fc = frequency
        self.possible_tones = {'email':400, 'text':600, 'call':800, 'one':1000, 'two':1200} #update this with new commands:frequencies
        
#given a command and the audioDevNumbers, it sends an appropriate tone back in acknowledgement
#audioDevNumbers is the output from the audioDevNumbers function: din, dout, dusb. Only dusb is actually used here.
#t_ack is the length of the acknowledgement pulse
    def run(self, command, audioDevNumbers, t_ack = 0.5):
        tone_freq = self.possible_tones.setdefault(command, None)
        if(tone_freq):
            p = pyaudio.PyAudio()
            din, dout, dusb = audioDevNumbers #can be ommitted if only dusb is provided
            Q = Queue.Queue()
            fc = self.fc
            pttsig = genPTT(0.07,0.25,44100.0)
            pulse = real(genPulse(44100.0*t_ack, tone_freq, 44100.0))/2.0
            Q.put(pttsig)
            Q.put(pulse)
            t_play = threading.Thread(target = play_audio,   args = (Q,   p, 44100, dusb  ))
            t_play.start()
            p.terminate()
        else:
            return
