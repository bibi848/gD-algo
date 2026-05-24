#%%
import os
import pandas as pd

# Paths
CWD = os.path.dirname(os.path.abspath(__file__))
RAW_PATH = os.path.join(CWD, "..", "Historical Data", "K_Data",
                        "Kraken_Data_Refactored", "XBTUSD_1m.csv")
OUT_DIR   = os.path.join(CWD, "K_Data")
os.makedirs(OUT_DIR, exist_ok=True)

# Load and Crop
print("Loading raw data...")
df = pd.read_csv(RAW_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df[df["timestamp"] >= "2019-01-01"].copy()
df.sort_values("timestamp", inplace=True)
df.set_index("timestamp", inplace=True)

print(f"  Rows after crop: {len(df):,}  ({df.index[0]} → {df.index[-1]})")

# Resampling
OHLCV = {
    "open":   "first",
    "high":   "max",
    "low":    "min",
    "close":  "last",
    "volume": "sum",   # dropped silently if not present
}

def resample(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    agg = {k: v for k, v in OHLCV.items() if k in df.columns}
    return df.resample(rule).agg(agg).dropna()

files = {
    "XBTUSD_1m.csv":  df,
    "XBTUSD_5m.csv":  resample(df, "5min"),
    "XBTUSD_15m.csv": resample(df, "15min"),
    "XBTUSD_1h.csv":  resample(df, "1h"),
}

for fname, frame in files.items():
    path = os.path.join(OUT_DIR, fname)
    frame.to_csv(path)
    print(f"  Written: {fname}  ({len(frame):,} rows)")