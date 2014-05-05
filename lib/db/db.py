# Interface to construct the database.
from ..utils.spectrogram import *
from word_class import *

class db:
    path = 'lib/db/words/'


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

        word_idx = 0

        while (word_idx < len(self.words)):
            word = self.words[word_idx]

            data_ds = self.recordQuery(word)
            word_obj = word_class(word, data_ds)            

            # Save the file or not.
            save_ans = raw_input('Save sound? [y]: ')
    
            if (save_ans == 'y'):
                word_obj.save(self.path)
                word_idx = word_idx + 1

            print '\n'

    def recordQuery(self, word):
        fs = self.sdr.sdr.sample_rate
        fc = self.sdr.sdr.center_freq

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
        myspectrogram_hann_ovlp(self.fm.demod(y_clip), self.m, fs, 0)

        data_ds = self.fm.completeDemod(y_clip, 512, self.cutoff, fs, 5)

        # Display clipped data.
        figure(figsize=(5, 6))
        myspectrogram_hann_ovlp(data_ds, self.m, fs * 1.0 / 5.0, 0)

        figure(figsize=(15, 6))
        plt.plot(data_ds)
        show(block=False)

        raw_input('ENTER to play sound...')
        self.player.play_audio(data_ds, 48000)

        return data_ds

    def recordContinously(self, progress):
        fs = self.sdr.sdr.sample_rate
        fc = self.sdr.sdr.center_freq
        # Fetch data.
        while (1):
            self.sdr.read_samples(self.Q, self.t)
#            progress.write('Q_record size: ' + str(self.Q.qsize()) + '\n')

    def processContinously(self, Qout, progress, N, taps):
        fs = self.sdr.sdr.sample_rate
        fc = self.sdr.sdr.center_freq

        # Accumulate data in a buffer and process.
        buff_first = np.array([])

        for i in range(int(N) / 2):
            buff_first = np.append(buff_first, self.Q.get())

        while (1):
            buff_second = np.array([])

            # Fetch the second N / 2 samples.
            for i in range(int(N) / 2):
                buff_second = np.append(buff_second, self.Q.get())

            buff = np.concatenate([buff_first, buff_second])
            buff_first = buff_second
            Qout.put(self.fm.completeDemod(buff, taps, self.cutoff, fs, 5))
            progress.write('Q_process size: ' + str(Qout.qsize()) + '\n')
