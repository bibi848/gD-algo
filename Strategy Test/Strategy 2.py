#%%
# Preparing Data
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "K_Data")

df_1m  = pd.read_csv(os.path.join(DIR, "XBTUSD_1m.csv"),  index_col="timestamp", parse_dates=True)
df_5m  = pd.read_csv(os.path.join(DIR, "XBTUSD_5m.csv"),  index_col="timestamp", parse_dates=True)
df_15m = pd.read_csv(os.path.join(DIR, "XBTUSD_15m.csv"), index_col="timestamp", parse_dates=True)
df_1h  = pd.read_csv(os.path.join(DIR, "XBTUSD_1h.csv"),  index_col="timestamp", parse_dates=True)

# Parameters
MA_FAST = 4
MA_SLOW = 20

HTF_MA = 20

ATR_PERIOD  = 14
ATR_MINIMUM = 10.0

TAKER_FEE       = 0.0040
MARGIN_OPEN_FEE = 0.0001
ROLLOVER_FEE    = 0.0001

INITIAL_MONEY = 200.0
BET = 0.001

START_DATE = '2020-01-01'
END_DATE   = '2025-01-01'

def htf_trend(df, period=HTF_MA):
    ma = df["close"].rolling(period).mean()
    trend = np.where(df["close"] > ma, 1, -1)
    s = pd.Series(trend, index=df.index)
    return s.shift(1)

trend_5m  = htf_trend(df_5m).reindex(df_1m.index, method="ffill")
trend_15m = htf_trend(df_15m).reindex(df_1m.index, method="ffill")
trend_1h  = htf_trend(df_1h).reindex(df_1m.index, method="ffill")

df_1m = df_1m.loc[START_DATE:END_DATE]

trend_5m  = trend_5m.loc[START_DATE:END_DATE]
trend_15m = trend_15m.loc[START_DATE:END_DATE]
trend_1h  = trend_1h.loc[START_DATE:END_DATE]

#%%
# Simulation Parameters
prices = df_1m["close"].values
highs  = df_1m["high"].values if "high" in df_1m.columns else prices
lows   = df_1m["low"].values  if "low"  in df_1m.columns else prices

money = INITIAL_MONEY
short_margin_called = False
position = 0.0
entry_price = 0.0
total_fees_paid = 0.0
margin_call_events = 0
candles_in_short = 0

fast_buf = []
slow_buf = []
atr_buf = []
prev_close = prices[0]

ma_fast_list = []
ma_slow_list = []
atr_list = []
equity_curve = []
trade_log = []

#%%
# Main Loop
for i in range(len(prices)):
    price = prices[i]
    high  = highs[i]
    low   = lows[i]

    fast_buf.append(price)
    slow_buf.append(price)

    if len(fast_buf) > MA_FAST:
        fast_buf.pop(0)

    if len(slow_buf) > MA_SLOW:
        slow_buf.pop(0)

    fast_ma = np.mean(fast_buf)
    slow_ma = np.mean(slow_buf)

    tr = max(
        high - low,
        abs(high - prev_close),
        abs(low  - prev_close)
    )
    atr_buf.append(tr)
    if len(atr_buf) > ATR_PERIOD:
        atr_buf.pop(0)
    atr = np.mean(atr_buf)

    prev_close = price

    ma_fast_list.append(fast_ma)
    ma_slow_list.append(slow_ma)
    atr_list.append(atr)

    if position > 0:
        equity = money + position * price
    elif position < 0:
        equity = money + (entry_price - price) * abs(position)
    else:
        equity = money

    equity_curve.append(equity)

    if position < 0:
        candles_in_short += 1

        if candles_in_short % 240 == 0:
            rollover_cost = abs(position) * price * ROLLOVER_FEE
            money -= rollover_cost
            total_fees_paid += rollover_cost

    if position < 0 and not short_margin_called:
        if equity < INITIAL_MONEY * 0.20:
            margin_call_events += 1
            short_margin_called = True

    if i < MA_SLOW or atr < ATR_MINIMUM:
        continue

    prev_fast = ma_fast_list[-2]
    prev_slow = ma_slow_list[-2]
    h1_trend = trend_1h.iloc[i]

    # Bullish crossover
    if prev_fast <= prev_slow and fast_ma > slow_ma:
        htf_votes = (
            trend_5m.iloc[i]
            + trend_15m.iloc[i]
            + trend_1h.iloc[i]
        )

        if htf_votes >= 1 and h1_trend == 1:

            if position < 0:
                trade_log.append((i, "close_short"))
                pnl = (entry_price - price) * abs(position)
                money += pnl
                fee = abs(position) * price * TAKER_FEE
                money -= fee
                total_fees_paid += fee
                position = 0.0
                entry_price = 0.0
                candles_in_short = 0
                short_margin_called = False

            if position == 0:
                trade_log.append((i, "open_long"))
                position = BET
                entry_price = price
                money -= BET * price
                fee = BET * price * TAKER_FEE
                money -= fee
                total_fees_paid += fee

    # Bearish crossover
    elif prev_fast >= prev_slow and fast_ma < slow_ma:

        htf_votes = (
            trend_5m.iloc[i]
            + trend_15m.iloc[i]
            + trend_1h.iloc[i]
        )

        if htf_votes <= -1 and h1_trend == -1:

            if position > 0:
                trade_log.append((i, "close_long"))
                money += position * price
                fee = position * price * TAKER_FEE
                money -= fee
                total_fees_paid += fee
                position = 0.0
                entry_price = 0.0

            if position == 0:
                trade_log.append((i, "open_short"))
                position = -BET
                entry_price = price
                fee = BET * price * TAKER_FEE
                fee2 = BET * price * MARGIN_OPEN_FEE
                money -= fee
                money -= fee2
                total_fees_paid += fee + fee2
                candles_in_short = 0
                short_margin_called = False

final_price = prices[-1]

if position > 0:
    money += position * final_price
    fee = position * final_price * TAKER_FEE
    money -= fee
    total_fees_paid += fee
    position = 0.0

elif position < 0:
    pnl = (entry_price - final_price) * abs(position)
    money += pnl
    fee = abs(position) * final_price * TAKER_FEE
    money -= fee
    total_fees_paid += fee
    position = 0.0
    short_margin_called = False

final_value = money

bh_value = (INITIAL_MONEY / prices[0]) * prices[-1]

#%%
# Results
print("Strategy Results")
print(f"Final portfolio value: ${final_value:.2f}")
print(f"Buy & hold value:      ${bh_value:.2f}")
print(f"Total fees paid:       ${total_fees_paid:.2f}")
print(f"Total trades:          {len(trade_log)}")
print(f"Margin call warnings:  {margin_call_events}")

n_longs  = sum(1 for _, t in trade_log if t == "open_long")
n_shorts = sum(1 for _, t in trade_log if t == "open_short")

print(f"Longs opened:          {n_longs}")
print(f"Shorts opened:         {n_shorts}")

open_longs   = [i for i, t in trade_log if t == "open_long"]
close_longs  = [i for i, t in trade_log if t == "close_long"]
open_shorts  = [i for i, t in trade_log if t == "open_short"]
close_shorts = [i for i, t in trade_log if t == "close_short"]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

ax1.plot(prices, color="orange", alpha=0.7, linewidth=0.8, label="Price")
ax1.plot(ma_fast_list, color="olive", linewidth=0.8,
         label=f"MA{MA_FAST}")
ax1.plot(ma_slow_list, color="brown", linewidth=0.8,
         label=f"MA{MA_SLOW}")
ax1.scatter(open_longs, [prices[i] for i in open_longs], color="green", marker="^",
            s=60, zorder=5, label="Open Long")
ax1.scatter(close_longs, [prices[i] for i in close_longs], color="red", marker="v", s=60,
            zorder=5, label="Close Long")
ax1.scatter(open_shorts, [prices[i] for i in open_shorts], color="blue", marker="v",
            s=60, zorder=5, label="Open Short")
ax1.scatter(close_shorts, [prices[i] for i in close_shorts], color="purple", marker="^",
            s=60, zorder=5, label="Close Short")
ax1.set_ylabel("Price (USD)")
ax1.legend(fontsize=7)
ax1.grid(True, alpha=0.3)

ax2.plot(atr_list, color="steelblue", linewidth=0.8, label="ATR")
ax2.axhline(ATR_MINIMUM, color="red", linestyle="--", linewidth=0.8, 
            label=f"ATR min ({ATR_MINIMUM})")

ax2.set_ylabel("ATR")
ax2.set_xlabel("Index")

ax2.legend(fontsize=7)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()