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
    
    def cropTimeData(self, time, data, startDate, endDate):
        start = pd.to_datetime(startDate)
        end = pd.to_datetime(endDate)

        mask = (time >= start) & (time <= end)

        new_time = time[mask].reset_index(drop=True)

        new_data = []
        for i in range(len(data)):
            aligned = data[i].reindex(time.index)
            new_data.append(aligned[mask].reset_index(drop=True))

        return new_time, new_data

    
    def calcPercentageChange(self, oldValue, newValue):
        return ((newValue-oldValue)/oldValue)*100

    def percentData(self, data, tickr):
        firstValues = []
        for i in range(len(tickr)):
                firstValues.append(data[i].iloc[0])
        
        perData = []
        for i in range(len(tickr)):
            grp = []
            for j in range(len(data[i])):
                grp.append(self.calcPercentageChange(firstValues[i], data[i].iloc[j]))
            perData.append(grp)

        return perData
    
    def rollingAverage(self, data, window):
        result = []
        for i in range(len(data)):
            start = max(0, i - window + 1)   
            window_slice = data[start:i+1]   
            avg = sum(window_slice) / len(window_slice)
            result.append(avg)
        return result
    
    def movingAverage(self, data, windows, tickr):
        MAData = []
        for i in range(len(tickr)):
            grp = []
            for w in windows:
                ma = self.rollingAverage(data[i], w)
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

        dt = self.df.copy()
        time = dt[0]['Price']
        data = []
        for i in range(len(self.tickr)):
            data.append(dt[i][priceType])

        time, data = self.cropTimeData(time, data, startDate, endDate)

        if percentage:
            data = self.percentData(data, self.tickr)
        
        if MA:
            MAData = self.movingAverage(data, MA, self.tickr)
        
        plt.figure(figsize=(10, 5))
        plt.xlabel("Date")
        if percentage:
            plt.ylabel("Percent Change")
            plt.title("Percent Change")
        else:
            plt.ylabel(f"{priceType}")
            plt.title(priceType)

        for i in range(len(self.tickr)):
            plt.plot(time, data[i], label=self.tickr[i])
            
            if MA:
                for j in range(len(MA)):
                    plt.plot(time, MAData[i][j], label=f"{self.tickr[i]} MA{MA[j]}")

        plt.grid()
        plt.legend()
        plt.show()