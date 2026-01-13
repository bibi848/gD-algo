import torch.nn as nn

class CNN1D(nn.Module):
    def __init__(self, n_features):
        super().__init__()

        self.net = nn.Sequential(
            nn.Conv1d(n_features, 32, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.Conv1d(32, 64, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1),
        )

        self.fc = nn.Linear(64, 1)

    def forward(self, x):
        # x: (batch, time, features)
        x = x.transpose(1, 2)
        x = self.net(x)
        x = x.squeeze(-1)
        return self.fc(x).squeeze(-1)