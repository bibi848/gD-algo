#%%
import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# Config
SAVE_DIR  = os.path.join("Training Data", "Models")
WINDOW = 150          # past minutes
HORIZON = 1           # h = 1 minute
BATCH_SIZE = 64
EPOCHS = 4
LR = 1e-3
TRAIN_SPLIT = 0.8
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Paths
BASE_DIR = os.path.join("Training Data", "Aligned Data")
BTC_FILE = os.path.join(BASE_DIR, "XBTUSD_1m_2018_aligned.csv")
ETH_FILE = os.path.join(BASE_DIR, "ETHUSD_1m_2018_aligned.csv")

# Load data
btc = pd.read_csv(BTC_FILE, parse_dates=["timestamp"])
eth = pd.read_csv(ETH_FILE, parse_dates=["timestamp"])
btc.set_index("timestamp", inplace=True)
eth.set_index("timestamp", inplace=True)

btc = btc[["close", "volume"]].rename(
    columns={"close": "BTC_close", "volume": "BTC_volume"}
)
eth = eth[["close", "volume"]].rename(
    columns={"close": "ETH_close", "volume": "ETH_volume"}
)

df = pd.concat([btc, eth], axis=1, join="inner")
df = df.sort_index()

print("Aligned rows:", len(df))
print("Start:", df.index[0])
print("End:", df.index[-1])

# Keep only numeric features
features = [
    "BTC_close", "BTC_volume",
    "ETH_close", "ETH_volume",
]

df = df[features]

# Log prices
df["BTC_close"] = np.log(df["BTC_close"])
df["ETH_close"] = np.log(df["ETH_close"])

#%%
# Dataset
class CryptoWindowDataset(Dataset):
    def __init__(self, data, window, horizon):
        self.data = data.values.astype(np.float32)
        self.window = window
        self.horizon = horizon

    def __len__(self):
        return len(self.data) - self.window - self.horizon

    def __getitem__(self, idx):
        x = self.data[idx : idx + self.window]

        p_t  = self.data[idx + self.window - 1, 0]  # BTC log price
        p_th = self.data[idx + self.window - 1 + self.horizon, 0]

        y = p_th - p_t

        return torch.tensor(x), torch.tensor(y)

# Train / Val split (time-based)
split_idx = int(len(df) * TRAIN_SPLIT)

train_df = df.iloc[:split_idx]
val_df   = df.iloc[split_idx - WINDOW - HORIZON :]

train_ds = CryptoWindowDataset(train_df, WINDOW, HORIZON)
val_ds   = CryptoWindowDataset(val_df, WINDOW, HORIZON)

train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
val_loader   = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)

# CNN model
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

model = CNN1D(n_features=len(features)).to(DEVICE)
optimizer = torch.optim.Adam(model.parameters(), lr=LR)
criterion = nn.MSELoss()

#%%
# Training loop
for epoch in range(EPOCHS):
    model.train()
    train_loss = 0.0

    for x, y in train_loader:
        x, y = x.to(DEVICE), y.to(DEVICE)

        optimizer.zero_grad()
        preds = model(x)
        loss = criterion(preds, y)
        loss.backward()
        optimizer.step()

        train_loss += loss.item()

    train_loss /= len(train_loader)

    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for x, y in val_loader:
            x, y = x.to(DEVICE), y.to(DEVICE)
            preds = model(x)
            val_loss += criterion(preds, y).item()

    val_loss /= len(val_loader)

    print(
        f"Epoch {epoch+1:02d} | "
        f"Train MSE: {train_loss:.6e} | "
        f"Val MSE: {val_loss:.6e}"
    )

#%%
checkpoint = {
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "epoch": epoch,
    "window": WINDOW,
    "horizon": HORIZON,
    "features": features,
}

torch.save(
    checkpoint,
    os.path.join(SAVE_DIR, "CNN_BTCUSD_1.pt")
)
