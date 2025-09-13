#%%
from Classes.Visualiser import Visualiser

tickrs = ['AMZN', 'NVDA', 'DIS']
stock = Visualiser('Stocks', tickrs, '1d')
stock.plotPrice(priceType='Close',
                startDate="01/01/2018",
                endDate="31/12/2024")
