import pandas as pd
import matplotlib.pyplot as plt
import os

availableColumns = ['Close', 'High', 'Low', 'Open', 'Volume']

class Visualiser:
    
    def __init__(self, assetType='Stocks', tickr=['AMD'], timeRes='1d'):

        self.assetType = assetType
        self.tickr = tickr
        self.timeRes = timeRes

        currentDirectory = os.getcwd()

        self.df = []
        for i in range(len(tickr)):
            filePath = currentDirectory + '//Historical Data//' + assetType + '//' + tickr[i] + '_' + timeRes + '_01012010_01012025.csv'
            self.df.append(pd.read_csv(filePath, header=0).iloc[2:])
            self.df[i]['Price'] = pd.to_datetime(self.df[i]['Price'], format="%Y-%m-%d")
        
            for col in self.df[i].columns:
                if col != 'Price':
                    self.df[i][col] = pd.to_numeric(self.df[i][col], errors='coerce')

    def plotPrice(self, priceType='Open', startDate=None, endDate=None):

        if priceType not in availableColumns:
            print('price type not available - yet!')

        data = self.df.copy()
        plt.figure(figsize=(10, 5))
        plt.xlabel("Date")
        plt.ylabel(f"{priceType}")

        for i in range(len(self.tickr)):
            if startDate:
                data[i] = data[i][data[i]['Price'] >= pd.to_datetime(startDate, dayfirst=True)]
            if endDate:
                data[i] = data[i][data[i]['Price'] <= pd.to_datetime(endDate, dayfirst=True)]
        
            plt.plot(data[i]['Price'], data[i][priceType], label=self.tickr[i])

        plt.title(priceType)
        plt.grid()
        plt.legend()
        plt.show()