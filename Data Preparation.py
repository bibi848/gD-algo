#%%
# Modules
'''
This script prepares the data for model training. Different currencies have different 
start dates on Kraken, so they are cropped and checked for alignment and gaps. Small
gaps are filled with the previous price but with a volume of 0. 
'''

import pandas as pd
import os

USD_pairs = ['ETHUSD', 'XRPUSD', 'XBTUSD']

INPUT_DIR  = os.path.join("Historical Data", "Kraken_Data_Refactored")
OUTPUT_DIR = "Training Data"
START_DATE = pd.Timestamp("2018-01-01", tz="UTC")

#%%
# Full minute index
end_dates = []
for pair in USD_pairs:
    path = os.path.join(INPUT_DIR, f"{pair}_1m.csv")
    df = pd.read_csv(path, parse_dates=['timestamp'])
    df['timestamp'] = df['timestamp'].dt.tz_convert('UTC')
    end_dates.append(df['timestamp'].max())

END_DATE = min(end_dates)

print("Global end date:", END_DATE)

full_index = pd.date_range(
    start=START_DATE,
    end=END_DATE,
    freq="1min",
    tz="UTC"
)

#%%
# Reindexing and cropping 

for pair in USD_pairs:
    print("Processing:", pair)

    path = os.path.join(INPUT_DIR, f"{pair}_1m.csv")
    df = pd.read_csv(path, parse_dates=['timestamp'])
    df['timestamp'] = df['timestamp'].dt.tz_convert('UTC')
    df.set_index('timestamp', inplace=True)

    # Crop to start/end
    df = df.loc[(df.index >= START_DATE) & (df.index <= END_DATE)]

    original_len = len(df)
    df = df.reindex(full_index)

    # No trades = Zero volume
    df['volume'] = df['volume'].fillna(0)

    # Forward fill prices
    price_cols = ['open', 'high', 'low', 'close']
    df[price_cols] = df[price_cols].ffill()

    # Drop rows that have NaNs
    df = df.loc[df[price_cols].notna().all(axis=1)]

    print(
        f"Original minutes: {original_len} | "
        f"After reindex: {len(df)}"
    )

    diffs = df.index.to_series().diff().value_counts()
    print("Time deltas:")
    print(diffs.head(3).to_dict())

    print()

    out_path = os.path.join(OUTPUT_DIR, f"{pair}_1m_2018_aligned.csv")
    df.to_csv(out_path)

#%%