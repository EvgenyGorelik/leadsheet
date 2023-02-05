from torch import nn
from torch.nn import functional as F

class M5(nn.Module):
    def __init__(self, n_input=1, n_output=35, stride=16, n_channel=32, perceptive_field=80):
        super().__init__()
        
        self.backbone = nn.Sequential(
            nn.Conv1d(n_input, n_channel, kernel_size=perceptive_field, stride=stride),
            nn.ReLU(),
            nn.BatchNorm1d(n_channel),
            nn.MaxPool1d(4),
            nn.Conv1d(n_channel, n_channel, kernel_size=3),
            nn.ReLU(),
            nn.BatchNorm1d(n_channel),
            nn.MaxPool1d(4),
            nn.Conv1d(n_channel, 2 * n_channel, kernel_size=3),
            nn.ReLU(),
            nn.BatchNorm1d(2 * n_channel),
            nn.MaxPool1d(4),
            nn.Conv1d(2 * n_channel, 2 * n_channel, kernel_size=3),
            nn.BatchNorm1d(2 * n_channel),
            nn.MaxPool1d(4)
        )
        self.head = nn.Sequential(
            nn.Linear(2 * n_channel, n_output)
        )


    def forward(self, x):
        x = self.backbone(x)
        x = F.avg_pool1d(x, x.shape[-1])
        x = x.permute(0, 2, 1)
        x = self.head(x)
        return F.log_softmax(x, dim=2)

