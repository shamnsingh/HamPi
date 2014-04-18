# Defines a wrapper class for pyAudio.
# Functions used from EE 123 Lab -- Miki Lustig, Frank.
import pyaudio
import wave
import numpy as np

class myAudio:

    def __init__(self):
        self.p = pyaudio.PyAudio()

    def terminate(self):
        self.p.terminate()

    def read_wav( self, wavname ):

        wf = wave.open(wavname, 'rb')

        CHUNK = 1024
        frames = []
        data_str = wf.readframes(CHUNK) #read a chunk

        while data_str != '':
            data_int = np.fromstring( data_str, 'int16') # convert from string to int (assumes .wav in int16)
            data_flt = data_int.astype( np.float32 ) / 32767.0 # convert from int to float32
            frames.append( data_flt )  #append to list
            data_str = wf.readframes(CHUNK) #read a chunk

        return np.concatenate( frames )


    def play_audio( self, data, fs):
        # data - audio data array
        # p    - pyAudio object
        # fs    - sampling rate

        # open output stream
        ostream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=fs,output=True)
        # play audio
        ostream.write( data.astype(np.float32).tostring() )
