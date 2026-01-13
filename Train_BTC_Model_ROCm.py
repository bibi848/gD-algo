import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from Classes.CryptoWindowDataset import CryptoWindowDataset
from Classes.CNN_Model import CNN1D

def main():
    print("Initialising")
    GPU_available = torch.cuda.is_available()
    print("GPU Available:", GPU_available)
    if GPU_available:
        print("GPU Detected:", torch.cuda.get_device_name(0))
    else:
        print("CPU Detected:", torch.cuda.get_device_name(0))
    print()

    # Config
    SAVE_DIR  = os.path.join("Training Data", "Models")
    WINDOW = 150    # past minutes
    HORIZON = 1     # h = 1 minute
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
    print("Reading CSVs")
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

    # Numeric features
    features = [
        "BTC_close", "BTC_volume",
        "ETH_close", "ETH_volume",
    ]

    df = df[features]

    # Log prices
    df["BTC_close"] = np.log(df["BTC_close"])
    df["ETH_close"] = np.log(df["ETH_close"])

    # Train / Val split
    split_idx = int(len(df) * TRAIN_SPLIT)

    train_df = df.iloc[:split_idx]
    val_df   = df.iloc[split_idx - WINDOW - HORIZON :]

    train_ds = CryptoWindowDataset(train_df, WINDOW, HORIZON)
    val_ds   = CryptoWindowDataset(val_df, WINDOW, HORIZON)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader   = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)

    # CNN model
    model = CNN1D(
        channels    = [4,16],
        kernels     = [7]
    ).to(DEVICE)

    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    criterion = nn.MSELoss()

    print()
    print('Training Starting')
    print()
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

if __name__ == "__main__":
    main()