'''
Convolutional Neural Network Classes. 
'''

import torch.nn as nn

class CNN1D(nn.Module):
    def __init__(
        self,
        channels,
        kernels,
        activation=nn.ReLU,
        pool="avg"
    ):
        super().__init__()

        assert len(channels) >= 2
        assert len(kernels) == len(channels) - 1

        layers = []

        for i in range(len(channels) - 1):
            layers.append(
                nn.Conv1d(
                    in_channels=channels[i],
                    out_channels=channels[i + 1],
                    kernel_size=kernels[i],
                    padding=kernels[i] // 2
                )
            )
            layers.append(activation())

        if pool == "avg":
            layers.append(nn.AdaptiveAvgPool1d(1))
        elif pool == "max":
            layers.append(nn.AdaptiveMaxPool1d(1))
        else:
            raise ValueError("pool must be 'avg' or 'max'")

        self.net = nn.Sequential(*layers)
        self.fc = nn.Linear(channels[-1], 1)

    def forward(self, x):
        x = x.transpose(1, 2)
        x = self.net(x)              
        x = x.squeeze(-1)            
        return self.fc(x).squeeze(-1)
