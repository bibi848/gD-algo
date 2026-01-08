'''
By choosing a ticker, you can download a csv of a stock between two dates.
Name should folow:         ticker_timeResolution_startDate_endDate.csv
Data Type variable can be: Stock, Crypto
interval:                  1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
Time Resolution:           daily, weekly, monthly
'''

import yfinance as yf
import os

currentDirectory = os.getcwd()
dataType = 'Crypto'
ticker = 'BTC-USD'
startDate = '2025-01-04'
endDate = '2026-01-07'
timeInterval = '5m'

fileName = ticker + '_' + timeInterval + '_' + startDate[8] + startDate[9] + startDate[5] + startDate[6] + startDate[0:4] + '_' + endDate[8] + endDate[9] + endDate[5] + endDate[6] + endDate[0:4] + '.csv'
filePath = currentDirectory + '\\Historical Data\\' + dataType + "\\" + fileName

df = yf.download(ticker, 
                 start=startDate, 
                 end=endDate,
                 interval = timeInterval, 
                 progress = False)
df.to_csv(filePath)

print(ticker, 'download done')


