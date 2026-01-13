# Historical Data

This folder contains the historical data used to visualise, backtest and explore, as well as serving as the training data for any models.

Folders:
* Crypto: This contains cryptocurrency data scraped from yfinance.
* Kraken_Data: This contains the historical data downloaded from Kraken. Not all data is shown in this repository as the file sizes are too large. This data can be accessed here: https://support.kraken.com/articles/360047543791-downloadable-historical-market-data-time-and-sales-.#
* Kraken_Data_Refactored: This contains the refactored data from Kraken in a usable format. The original data from Kraken contains time [s] - price - volume. The refactored data contains Timestamp - Open - High - Low - Close - Volume, at a minute-by-minute resolution.
* Stocks: This contains historical stock data scraped from yfinance.

<br><br>
Files:
* `Fine Resolution Scraper.py`: Attempts to scrape minute-by-minute resolution data for BTC from yfinance. However, this is not efficient, and so data was instead taken from Kraken.
* `Kraken Data Refactoring.py`: Processes the data in the folder Kraken_Data to convert the second-resolution data to minute-resolution data. The resulting data is stored in the Kraken_Data_Refactored folder.
* `Yahoo Finance Scraper`: This accesses the yfinance data for stocks and crypto and converts them into OHLC csv files. These are stored in the Crypto and Stocks folder above.
