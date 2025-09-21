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
    
    def calcPercentageChange(self, oldValue, newValue):
        return ((newValue-oldValue)/oldValue)*100

    def percentData(self, data, priceType, startDate, tickr):
        firstValues = []
        for i in range(len(tickr)):
            df_filtered = data[i][priceType][data[i]['Price'] >= pd.to_datetime(startDate, dayfirst=True)]
            if not df_filtered.empty:
                FV = df_filtered.iloc[0]
                firstValues.append(FV)
        
        perData = []
        for i in range(len(tickr)):
            dt = data[i][priceType]
            grp = []
            for j in range(len(dt)):
                grp.append(self.calcPercentageChange(firstValues[i], dt.iloc[j]))
            perData.append(grp)

        return perData


    def plotPrice(self, priceType='Open', 
                        percentage=False,
                        MA=False,
                        startDate=None, 
                        endDate=None):

        if priceType not in availableColumns:
            print('price type not available - yet!')
            return

        data = self.df.copy()

        for i in range(len(self.tickr)):
            if startDate:
                data[i] = data[i][data[i]['Price'] >= pd.to_datetime(startDate, dayfirst=True)]
            if endDate:
                data[i] = data[i][data[i]['Price'] <= pd.to_datetime(endDate, dayfirst=True)]
        
        if percentage:
            perData = self.percentData(data, priceType, startDate, self.tickr)
        
        plt.figure(figsize=(10, 5))
        plt.xlabel("Date")
        if percentage:
            plt.ylabel("Percent Change")
            plt.title("Percent Change")
        else:
            plt.ylabel(f"{priceType}")
            plt.title(priceType)

        for i in range(len(self.tickr)):
            if percentage:
                plt.plot(data[i]['Price'], perData[i], label=self.tickr[i])
            else:
                plt.plot(data[i]['Price'], data[i][priceType], label=self.tickr[i])

        plt.grid()
        plt.legend()
        plt.show()