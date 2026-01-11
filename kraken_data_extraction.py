#%%
import pandas as pd

file_path = 'C://Users//oscar//Documents//Python//gD-algo//Historical Data//Kraken_Data_Refactored//'
file_name = 'XBTUSD_1m.csv'
path = file_path + file_name

df = pd.read_csv(path)

#%%
import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.join("Historical Data", "Kraken_Data_Refactored")

BTC_FILE = os.path.join(BASE_DIR, "XBTUSD_1m.csv")
ETH_FILE = os.path.join(BASE_DIR, "ETHUSD_1m.csv")

btc = pd.read_csv(BTC_FILE, parse_dates=['timestamp'])
eth = pd.read_csv(ETH_FILE, parse_dates=['timestamp'])

btc.set_index('timestamp', inplace=True)
eth.set_index('timestamp', inplace=True)

data = pd.concat(
    [
        btc['close'].rename('BTC_Close'),
        eth['close'].rename('ETH_Close')
    ],
    axis=1,
    join='inner'
)

print("First timestamp:", data.index[0])
print("Last timestamp:", data.index[-1])
print("Number of aligned minutes:", len(data))

#%%
fig, ax1 = plt.subplots(figsize=(12, 6))

# BTC
ax1.plot(data.index, data['BTC_Close'], c='b', label='BTC/USD Close')
ax1.set_xlabel("Time (UTC)")
ax1.set_ylabel("BTC Price")
ax1.tick_params(axis='y')
ax1.legend(loc='upper left')

# ETH
ax2 = ax1.twinx()
ax2.plot(data.index, data['ETH_Close'], c='r', label='ETH/USD Close')
ax2.set_ylabel("ETH Price")
ax2.tick_params(axis='y')
ax2.legend(loc='center left')

plt.title("BTC/USD vs ETH/USD Minute Close Price Alignment")
plt.tight_layout()
plt.show()

#%%
missing = data.index.to_series().diff().value_counts()
print(missing.head())

#%%
