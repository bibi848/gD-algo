'''
Uses the Visualiser class to visualise financial data from yfinance. 
'''
#%%
# Visualise Data

from Classes.Visualiser import Visualiser

tickrs = ['BTC-USD']
stock = Visualiser('Crypto', tickrs, '1d', startDate='01012015', endDate='01012026')
stock.plotPrice(priceType='Close',
                percentage=True,
                MA=[200, 50],
                startDate="2017-01-01",
                endDate="2026-01-01")
