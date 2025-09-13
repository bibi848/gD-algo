#%%
from Classes.Visualiser import Visualiser

stock = Visualiser('Stocks', 'NVDA', '1d')
stock.plotPrice(priceType='High',
                startDate="01/01/2024",
                endDate="31/12/2024")
