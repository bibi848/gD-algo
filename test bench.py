#%%
from Classes.Visualiser import Visualiser

tickrs = ['DIS']
stock = Visualiser('Stocks', tickrs, '1d')
stock.plotPrice(priceType='Close',
                percentage=True,
                MA=[200, 50, 20],
                startDate="2020-01-01",
                endDate="2021-01-01")
