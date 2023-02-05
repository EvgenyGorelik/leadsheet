
from torch import optim
from sys import path
import os
path.append(os.getcwd())
from datahandler.dataset import AudioDataset
from model import M5


if __name__=="__main__":
    dataset = AudioDataset("testing")
    model = M5(n_input=2).cuda()
    optimizer = optim.Adam(model.parameters(),  lr=0.01, weight_decay=0.0001)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.1)  # reduce the learning after 20 epochs by a factor of 10
    for item in dataset:
        output = model(item["sample"].unsqueeze(0))
        print(output)