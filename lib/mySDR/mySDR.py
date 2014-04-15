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
    def read_samples(self, Q, n):
        Q.put(self.sdr.read_samples(n))
