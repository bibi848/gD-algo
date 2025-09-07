#%%
import matplotlib.pyplot as plt
import pandas as pd
import os

currentDirectory = os.getcwd()
filePath = currentDirectory + '//Historical Data//Stocks//AMD_1d_01012010_01012025.csv'

df = pd.read_csv(filePath, header=0).iloc[2:]

#%% 
df['Price'] = pd.to_datetime(df['Price'])

plt.figure(figsize=(10,5))
plt.plot(df['Price'], df['Open'])
plt.xlabel("Date")
plt.ylabel("Open Price")
plt.title("Stock Open Prices Over Time")
plt.grid(True)
plt.show()
