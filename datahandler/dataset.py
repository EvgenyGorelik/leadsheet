from torch.utils.data import Dataset
import os
import json
from sys import path
path.append(os.getcwd())
from datahandler.parsers import *
from datahandler.sample_operations import Sampler
from torch import arange
import matplotlib.pyplot as plt

def plot_waveform(waveform, sample_rate):
    waveform = waveform.cpu().numpy()

    num_channels, num_frames = waveform.shape
    time_axis = arange(0, num_frames) / sample_rate

    figure, axes = plt.subplots(num_channels, 1)
    if num_channels == 1:
        axes = [axes]
    for c in range(num_channels):
        axes[c].plot(time_axis, waveform[c], linewidth=1)
        axes[c].grid(True)
        if num_channels > 1:
            axes[c].set_ylabel(f"Channel {c+1}")
    figure.suptitle("waveform")
    plt.show()

class AudioDataset(Dataset):
    def __init__(self, data_root, sample_rate=44100) -> None:
        super().__init__()
        meta_file = os.path.join(data_root,"meta.json")
        assert os.path.exists(meta_file), f"{meta_file} does not exist!"
        self.meta = json.load(open(meta_file))
        self.data_root = data_root
        self.sample_rate = sample_rate
        self.sampler = Sampler(sample_rate=self.sample_rate)

    def __getitem__(self, index):
        item = dict()
        sample = self.sampler.load(os.path.join(self.data_root, self.meta[index]["sample"]))
        item["sample"] = sample
        if "annotation" in self.meta[index]:
            annotations = parse(os.path.join(self.data_root,self.meta[index]["annotation"]))
            if len(annotations.tempo) == 0:
                assert "tempo" in self.meta[index], f"Tempo not available for {self.meta[index]['name']}"
                beat_length = self.sample_rate/(float(self.meta[index]["tempo"])/60.0)
            sample_pointer = 0
            ann_ind = {"from_ind": [], "to_ind": [], "chord": []}
            for chord in annotations.chords:
                sample_pointer += chord["subdivision"]*beat_length
                if sample_pointer > 0:
                    ann_ind["to_ind"].append(sample_pointer)
                    sample_pointer += 1
                ann_ind["from_ind"].append(sample_pointer)
                ann_ind["chord"].append(chord["chord"])
            ann_ind["to_ind"].append(sample.shape[1])
            # read as: from index a to index b, chord c is played
            item["annotation"] = ann_ind
        return item
    


if __name__=="__main__":
    dataset = AudioDataset("data")
    waveform = dataset.__getitem__(0)
    plot_waveform(waveform["sample"], dataset.sample_rate)
