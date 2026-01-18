# gD-algo

Welcome to gD-algo! I use this library for financial programming projects. Currently, I am exploring historical stock and crypto data, but I also have projects looking at option pricing and using the polymarket API. If you see any inconsistencies between a README and a file, or missing information, this is probably because this is an evolving project. I will try to keep the repository updated as I work. 

## Summary
Folders:
* Classes: Any new objects defined live in this folder.
* Historical Data: Contains Stock and Crypto historical data. More information can be found in the folder.
* Option Tests: Scripts looking at option pricing.
* PM: Scripts looking at using Polymarket via its API.

<br><br>
Files:
* `.gitignore`.
* `README.md`.
* `requirements.txt`.
* `test bench.py`.

## BTC Project
The objective of this project is to train a deep learning model to predict BTC price fluctuations on minute-by-minute resolutions. This is done on Kraken, using both the REST and Websocket APIs. The inputs to the model are:
* Past OHLC data for BTC (minute resolution).
* Past volumen for BTC (minute resolution).
* Past price data for BTC (second resolution).
* Past OHLC data for ETH (minute resolution).
* Past OHLC data for SOL (minute resolution).
* Moving Averages (E.g. MA(60) and MA(120)).

This is still the beginnning of the project, and so the inputs above may change as the project progresses.

## AMD ROCm
To improve the performance of the model training, ROCm 7.1.1 was used on Ubuntu 24.04.3 to leverage the use of my AMD Radeon RX 6900 XT. Information on the setup and use can be found in the folder ROCM Info. It is used to train the model in `Train_BTC_Model_ROCm.py`.

<br><br>
## Citation & Contact
If you would like to use any resources that are present in this repository please cite using
* Oscar Djuric. gD-algo. GitHub repository, 2025. https://github.com/bibi848/gD-algo

If you would like to contact me with any questions surrounding this repository please email oscar.djuric@gmail.com
