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

    def percentData(self, data, priceType, tickr):
        firstValues = []
        for i in range(len(tickr)):
                firstValues.append(data[i][priceType].iloc[0])
        
        perData = []
        for i in range(len(tickr)):
            grp = []
            for j in range(len(data[i][priceType])):
                grp.append(self.calcPercentageChange(firstValues[i], data[i][priceType].iloc[j]))
            perData.append(grp)

        return perData
    
    def movingAverage(self, data, priceType, windows, tickr):
        MAData = []
        for i in range(len(tickr)):
            grp = []
            for w in windows:
                ma = data[i][priceType].rolling(window=w, min_periods=1).mean()
                grp.append(ma)
            MAData.append(grp)
        return MAData

    def plotPrice(self, priceType='Open', 
                        percentage=False,
                        MA=False,
                        startDate=None, 
                        endDate=None):

        if priceType not in availableColumns:
            print('price type not available - yet!')
            return

        data = self.df.copy()

        time = []
        for i in range(len(self.tickr)):
            if startDate:
                data[i] = data[i][data[i]['Price'] >= pd.to_datetime(startDate, dayfirst=True)]
            if endDate:
                data[i] = data[i][data[i]['Price'] <= pd.to_datetime(endDate, dayfirst=True)]
            time.append(data[i]['Price'])

        if percentage:
            data = self.percentData(data, priceType, self.tickr)
        
        if MA:
            MAData = self.movingAverage(data, priceType, MA, self.tickr)
        
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
                plt.plot(time[i], data[i], label=self.tickr[i])
            else:
                plt.plot(time[i], data[i][priceType], label=self.tickr[i])
            
            if MA:
                for j in range(len(MA)):
                    plt.plot(data[i]['Price'], MAData[i][j], label=f"{self.tickr[i]} MA{MA[j]}")

        plt.grid()
        plt.legend()
        plt.show()