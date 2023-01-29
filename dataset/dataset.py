from torch.utils.data import Dataset
import os
import json
from annotations import load_annotations
from sample_operations import read

class SampleDataset(Dataset):
    def __init__(self, data_root) -> None:
        super().__init__()
        meta_file = os.path.join(data_root,"meta.json")
        assert os.path.exists(meta_file), f"{meta_file} does not exist!"
        self.meta = json.load(open(meta_file))
        self.data_root = data_root

    def __getitem__(self, index):
        item = dict()
        frame_rate, sample = read(os.path.join(self.data_root,self.meta[index]["sample"]), normalized=True)
        if "annotation" in self.meta[index]:
            assert "tempo" in self.meta[index], f"Tempo not available for {self.meta[index]['name']}"
            beat_length = frame_rate/(float(self.meta[index]["tempo"])/60.0)
            annotations = load_annotations(os.path.join(self.data_root,self.meta[index]["annotation"]))
            if "repetitions" in self.meta[index]:
                chords = []
                for r in self.meta[index]["repetitions"]:
                    chords += annotations.chords
                annotations.chords = chords
            ann_ind = ["from_ind", "to_ind", "chord"]
            for chord in annotations.chords:
                ann_ind
        return item

if __name__=="__main__":
    dataset = SampleDataset("data")
    dataset.__getitem__(0)