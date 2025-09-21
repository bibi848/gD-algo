#%%
from Classes.Visualiser import Visualiser

tickrs = ['TSLA', 'META']
stock = Visualiser('Stocks', tickrs, '1d')
stock.plotPrice(priceType='Open',
                percentage=True,
                MA=False,
                startDate="01/01/2020",
                endDate="01/01/2024")
