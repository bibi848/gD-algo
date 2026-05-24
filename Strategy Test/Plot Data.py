#%%
# Setup
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "K_Data")
df_1m  = pd.read_csv(os.path.join(DIR, "XBTUSD_1m.csv"),  index_col="timestamp", parse_dates=True)
df_5m  = pd.read_csv(os.path.join(DIR, "XBTUSD_5m.csv"),  index_col="timestamp", parse_dates=True)
df_15m = pd.read_csv(os.path.join(DIR, "XBTUSD_15m.csv"), index_col="timestamp", parse_dates=True)
df_1h  = pd.read_csv(os.path.join(DIR, "XBTUSD_1h.csv"),  index_col="timestamp", parse_dates=True)

# Time period
START_DATE = '2019-01-01'
END_DATE   = 'end'

HTF_MA = 20

# Higher timeframe trend signals
def htf_trend(df: pd.DataFrame, period: int = HTF_MA) -> pd.Series:
    ma = df["close"].rolling(period).mean()
    trend = np.where(df["close"] > ma, 1, -1)
    return pd.Series(trend, index=df.index)

trend_5m  = htf_trend(df_5m).reindex(df_1m.index, method="ffill")
trend_15m = htf_trend(df_15m).reindex(df_1m.index, method="ffill")
trend_1h  = htf_trend(df_1h).reindex(df_1m.index, method="ffill")

if END_DATE == 'end':
    df_1m     =    df_1m.loc[START_DATE :]
    trend_5m  = trend_5m.loc[START_DATE :]
    trend_15m = trend_15m.loc[START_DATE:]
    trend_1h  = trend_1h.loc[START_DATE :]
else:
    df_1m = df_1m.loc[START_DATE:END_DATE]
    trend_5m  = trend_5m.loc[START_DATE:END_DATE]
    trend_15m = trend_15m.loc[START_DATE:END_DATE]
    trend_1h  = trend_1h.loc[START_DATE:END_DATE]

#%%
# Plot
df_1m['close'].plot(figsize=(12, 6))
plt.title('XBTUSD Close Price')
plt.ylabel('Price')
plt.xlabel('Date')
plt.grid(True, alpha=0.8)
plt.show()