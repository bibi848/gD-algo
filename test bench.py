#%%
from Classes.Visualiser import Visualiser

tickrs = ['TSLA']
stock = Visualiser('Stocks', tickrs, '1d')
stock.plotPrice(priceType='Close',
                percentage=True,
                MA=[200],
                startDate="01/01/2020",
                endDate="01/01/2021")
