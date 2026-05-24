#%%
# Setup
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

cwd = os.getcwd()
cwd = cwd[:len(cwd) - len('Strategy Test')]
cwd_data = cwd + 'Historical Data\\K_Data\\Kraken_Data_Refactored\\'

XBTUSD_1m_full = pd.read_csv(cwd_data + 'XBTUSD_1m.csv')

#%%
# Start in 2020
start_date = '2020-01-01'
data_points = 1_050

XBTUSD_1m = XBTUSD_1m_full[XBTUSD_1m_full['timestamp'] >= start_date].copy()
XBTUSD_1m['timestamp'] = pd.to_datetime(XBTUSD_1m['timestamp'])
XBTUSD_1m_crop = XBTUSD_1m[:data_points].copy()

#%%
# Plot
XBTUSD_1m_crop.set_index('timestamp')['close'].plot(figsize=(12, 6))
plt.title('XBTUSD Close Price')
plt.ylabel('Price')
plt.xlabel('Date')
plt.grid(True, alpha=0.8)
plt.show()

#%%
price_list = list(XBTUSD_1m_crop['close'])
money = 200 # USD
bet_size = 0.001 # BTC
position = 0

TAKER_FEE = 0.0040  # 0.40% - you're a taker when reacting to signals
total_fees_paid = 0  # track cumulative fees

buy_hold_val = (money / price_list[0]) * price_list[-1]

#%%

ma1_list = []
ma2_list = []

ma1_roll = []
ma2_roll = []

buy_long_list   = []
sell_long_list  = []
buy_short_list  = []
sell_short_list = []

MA1 = 4
MA2 = 20

for i in range(len(price_list)):
    spot = price_list[i]
    
    ma1_roll.append(spot)
    ma2_roll.append(spot)
    
    if len(ma1_roll) > MA1:
        ma1_roll.pop(0)
    if len(ma2_roll) > MA2:
        ma2_roll.pop(0)

    mean1 = np.mean(ma1_roll)
    mean2 = np.mean(ma2_roll)
    
    ma1_list.append(mean1)
    ma2_list.append(mean2)
    
    if i >= MA2:
        # buy long, sell short
        if ma1_list[-2] <= ma2_list[-2] and mean1 > mean2:

            if position < 0:
                sell_short_list.append(i)
                money += position * spot          # close short (position is negative)
                fee = abs(position * spot) * TAKER_FEE
                money -= fee
                total_fees_paid += fee
                position = 0
            
            if position == 0:
                buy_long_list.append(i)
                position += bet_size
                money -= bet_size * spot
                fee = bet_size * spot * TAKER_FEE
                money -= fee
                total_fees_paid += fee

        # sell long, buy short
        elif ma1_list[-2] >= ma2_list[-2] and mean1 < mean2:

            if position > 0:
                sell_long_list.append(i)
                money += position * spot
                fee = abs(position * spot) * TAKER_FEE
                money -= fee
                total_fees_paid += fee
                position = 0
            
            if position == 0:
                buy_short_list.append(i)
                position -= bet_size
                money += bet_size * spot
                fee = bet_size * spot * TAKER_FEE
                money -= fee
                total_fees_paid += fee

#%%
# Create x-axis indices for plotting
ma1_x = list(range(len(ma1_list)))
ma2_x = list(range(len(ma2_list)))

plt.figure(figsize=(12, 6))
plt.plot(price_list, color='orange', alpha=0.7, label='Price')

plt.plot(ma1_x, ma1_list, label=f'MA{MA1}', color='olive')
plt.plot(ma2_x, ma2_list, label=f'MA{MA2}', color='brown')

plt.scatter(buy_long_list, [ma1_list[i] for i in buy_long_list], 
            color='green', marker='.', s=100, label='Buy Long')
plt.scatter(sell_long_list, [ma1_list[i] for i in sell_long_list], 
            color='red', marker='.', s=100, label='Sell Long')

plt.scatter(buy_short_list, [ma1_list[i] for i in buy_short_list], 
            color='blue', marker='.', s=100, label='Buy Short')
plt.scatter(sell_short_list, [ma1_list[i] for i in sell_short_list], 
            color='grey', marker='.', s=100, label='Sell Short')

plt.legend()
plt.title('Moving Market Average Crossovers')
plt.xlabel('Time')
plt.ylabel('Price')
plt.grid(True, alpha=0.3)
plt.show()

print('Trade Results')
print(f"Cash:     {money:.4f}")
print(f"Position: {position}")
print(f"Total:    {money + position * spot:.4f}")
print(f"Fees paid: {total_fees_paid:.4f}")

print()
print('Buy and Hold')
print(f"{buy_hold_val:.4f}")