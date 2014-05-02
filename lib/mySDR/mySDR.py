from rtlsdr import RtlSdr

# Wrapper for the SDR.

class mySDR:

    def __init__(self):
        self.sdr = RtlSdr()

    def set_up(self, fs, fc, gain):
        self.sdr.sample_rate = fs
        self.sdr.gain = gain
        self.sdr.center_freq = fc

    # Read samples and write them into a queue.
    def read_samples(self, Q, t):
        Q.put(self.sdr.read_samples(256000 * t))

    # Read samples and return the samples.
    def read_samples_return(self, t):
        return self.sdr.read_samples(256000 * t)

    def close(self):
        self.sdr.close()
