# Interface to construct the database.
from ..utils.spectrogram import *
from word_class import *

class db:
    
    # Initiate the database construction.
    def __init__(self, words, t, m, cutoff, sdr, Q, fm, player):
        self.words = words
        self.t = t
        self.m = m
        self.cutoff = cutoff
        self.sdr = sdr
        self.Q = Q
        self.fm = fm
        self.player = player

    # Process to record and save a word database.
    def construct(self):
        fs = self.sdr.sdr.sample_rate
        fc = self.sdr.sdr.center_freq

        for word in self.words:
            raw_input('ENTER and speak "' + word + '" ...')
           
            # Fetch data.
            self.sdr.read_samples(self.Q, self.t)
            y = self.Q.get()
            
            figure(figsize=(15, 6))
            myspectrogram_hann_ovlp(y, self.m, fs, fc)

            show(block=False)

            # Clip the spectrogram for data.
            t_start = float(raw_input('Enter starting time: '))
            t_end = float(raw_input('Enter ending time: '))

            y_clip = y[round(fs * t_start) : round(fs * t_end)]

            figure(figsize=(15, 6))
            myspectrogram_hann_ovlp(y_clip, self.m, fs, fc)

            data_ds = self.fm.completeDemod(y_clip, self.m, self.cutoff, fs, 5)

            # Display clipped data.
            figure(figsize=(5, 6))
            myspectrogram_hann_ovlp(data_ds, self.m, fs * 1.0 / 5.0, 0)

            figure(figsize=(15, 6))
            plt.plot(data_ds)
            show()

            word_obj = word_class(word, data_ds)            

            raw_input('ENTER to play sound...')
            self.player.play_audio(data_ds, 48000)

            # Save the file or not.
            save_ans = raw_input('Save sound? [y]: ')
    
            if (save_ans == 'y'):
                word_obj.save()

            print '\n'
