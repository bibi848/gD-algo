from torch.utils.data import Dataset
import numpy as np
import torch

class CryptoWindowDataset(Dataset):
    def __init__(self, data, window, horizon):
        self.data = data.values.astype(np.float32)
        self.window = window
        self.horizon = horizon

    def __len__(self):
        return len(self.data) - self.window - self.horizon

    def __getitem__(self, idx):
        x = self.data[idx : idx + self.window]

        p_t  = self.data[idx + self.window - 1, 0]
        p_th = self.data[idx + self.window - 1 + self.horizon, 0]
        y = p_th - p_t

        return torch.tensor(x), torch.tensor(y)