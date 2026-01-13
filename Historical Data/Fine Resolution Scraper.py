'''
Unfortunately, yfinance does not allow minute-resolution data to be extracted 
with timeframes larger than 8 days. This script extracts minute-resolution data
every single year to form large, high resolution data sets. 
'''

import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

ticker = "BTC-USD"
dataType = "Crypto"
interval_limits = {
    "1m": 20,
    "2m": 20,
    "5m": 20
}
today = datetime(2026, 1, 7)

base_dir = os.path.join(os.getcwd(), "Historical Data", dataType)
os.makedirs(base_dir, exist_ok=True)

for interval, lookback_days in interval_limits.items():
    print('Downloading Interval', interval)

    start_day = today - timedelta(days=lookback_days)
    all_data = []

    current_day = start_day
    while current_day < today:
        next_day = current_day + timedelta(days=1)

        df = yf.download(
            ticker,
            start=current_day.strftime("%Y-%m-%d"),
            end=next_day.strftime("%Y-%m-%d"),
            interval=interval,
            progress=False,
            auto_adjust=True
        )

        all_data.append(df)

        current_day = next_day

    final_df = pd.concat(all_data)
    final_df = final_df[~final_df.index.duplicated(keep="first")]

    filename = f"{ticker}_{interval}_{lookback_days}d.csv"
    filepath = os.path.join(base_dir, filename)

    final_df.to_csv(filepath)
    print(f"Saved: {filepath}")
