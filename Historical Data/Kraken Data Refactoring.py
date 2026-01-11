#%%
'''
This code takes each of the coin-pairs downloaded from Kraken and refactors them to the
correct format. The original data has 3 columns: time [s] - price - amount. 
The new data has the format: Timestamp - Open - High - Low - Close - Volume in minute-by-minute
resolution. The new data is stored in the Kraken_Data_Refactored folder. 
'''

import os
import pandas as pd

coinPairs = ['ETHEUR', 'ETHGBP', 'ETHUSD',
             'SOLEUR', 'SOLGBP', 'SOLUSD',
             'XBTEUR', 'XBTGBP', 'XBTUSD',
             'XRPEUR', 'XRPGBP', 'XRPUSD']

INPUT_DIR  = "Kraken_Data"
OUTPUT_DIR = "Kraken_Data_Refactored"
TIMEFRAME  = "1min"

def load_and_resample(pair):
    path = os.path.join(INPUT_DIR, f"{pair}.csv")
    print(f"Processing: {pair}")

    df = pd.read_csv(path)
    df.columns = ['timestamp', 'price', 'volume']
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)

    df = df.sort_values('timestamp')
    df.set_index('timestamp', inplace=True)

    # Resample to 1-minute OHLC
    ohlc = df['price'].resample(TIMEFRAME).ohlc()
    vol = df['volume'].resample(TIMEFRAME).sum()

    ohlcv = ohlc.join(vol)
    ohlcv.columns = ['open', 'high', 'low', 'close', 'volume']

    ohlcv.dropna(inplace=True)

    return ohlcv

for pair in coinPairs:
    ohlcv = load_and_resample(pair)
    out_path = os.path.join(OUTPUT_DIR, f"{pair}_1m.csv")
    ohlcv.to_csv(out_path)

#%%
import pandas as pd
OUTPUT_DIR = "Kraken_Data_Refactored"
coinPairs = ['ETHEUR', 'ETHGBP', 'ETHUSD',
             'SOLEUR', 'SOLGBP', 'SOLUSD',
             'XBTEUR', 'XBTGBP', 'XBTUSD',
             'XRPEUR', 'XRPGBP', 'XRPUSD']

for pair in coinPairs:
    df = pd.read_csv(os.path.join(OUTPUT_DIR, f"{pair}_1m.csv"))

    print(pair)
    print('First Date:', df['timestamp'][0])
