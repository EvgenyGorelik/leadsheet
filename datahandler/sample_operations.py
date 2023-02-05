from pydub import AudioSegment
from pydub.playback import play
import os
import numpy as np
import torchaudio
import torchaudio.functional as F

class Sampler:
    def __init__(self, augmentations=None, sample_rate=44100) -> None:
        self.sample_rate = sample_rate
        pass

    def load(self, file):
        waveform, sample_rate = torchaudio.load(file)
        waveform = waveform.cuda()
        if sample_rate != self.sample_rate:
            waveform = F.resample(waveform, sample_rate, self.sample_rate)
        return waveform


def read_pydub(f, normalized=False):
    a = AudioSegment.from_wav(f)
    #play(song)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y

if __name__=="__main__":

    sampler = Sampler()
    sampler.load("data\samples\sample_001.wav")
    # frame_rate, sample = read_pydub("data/tracks/All The Things You Are.wav")
    # print(sample.shape)
