from pydub import AudioSegment
from pydub.playback import play
import os
import numpy as np



def read(f, normalized=False):
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
    frame_rate, sample = read("data/tracks/All The Things You Are.wav")
    print(sample.shape)
