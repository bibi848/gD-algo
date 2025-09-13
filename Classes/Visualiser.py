import pandas as pd
import matplotlib.pyplot as plt
import os

class Visualiser:
    
    def __init__(self, assetType='Stocks', tickr='AMD', timeRes='1d'):

        self.assetType = assetType
        self.tickr = tickr
        self.timeRes = timeRes

        currentDirectory = os.getcwd()
        self.filePath = currentDirectory + '//Historical Data//' + assetType + '//' + tickr + '_' + timeRes + '_01012010_01012025.csv'

        self.df = pd.read_csv(self.filePath, header=0).iloc[2:]
        self.df['Price'] = pd.to_datetime(self.df['Price'], format="%Y-%m-%d")
        
        for col in self.df.columns:
            if col != 'Price':
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')



    def plotPrice(self, priceType='Open', startDate=None, endDate=None):
        if priceType not in self.df.columns:
            raise ValueError(f"Column '{priceType}' not found. Available: {list(self.df.columns)}")

        data = self.df.copy()
        if startDate:
            data = data[data['Price'] >= pd.to_datetime(startDate, dayfirst=True)]
        if endDate:
            data = data[data['Price'] <= pd.to_datetime(endDate, dayfirst=True)]

        title = self.tickr + ": " + priceType
        
        plt.figure(figsize=(10, 5))
        plt.plot(data['Price'], data[priceType])
        plt.xlabel("Date")
        plt.ylabel(f"{priceType}")
        plt.title(title)
        plt.grid()
        plt.show()