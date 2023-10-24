<h1 align="center">
    <img src=".\files\colored_eye.svg" width="155" />
    <p>🙇🏽‍♂️ financial-applications 🙇🏽 </p>
</h1>

## 🚨 ABOUT

### This **Project** have a lot of python code for download and analisys of stock market.

## ⚓ seven_mean_factor_investing

This folder contains a static code that have a end-to-end work flow. The code itself can download all needed data for applying the 7 mean model using a factor investing methodology with backtest.

Basically this code are creating a dataframe that contains in the lines - last business day of each month - the mean of the profitability of last 7 months, considering only price! after that, for each month, the program rank all the companies and choose the first 8 (TOP8) to be in our wallet. Each month the program calibrate the TOP8 stocks to compose our wallet! In the end are create a .png image to show the mapheat with profitability.

#### **CODE FLOW**:
    1) read total and monthly ibov indices compose
    2) download all needed data throught yahoo_finance

    ### MODELING
    3) calculate monthly returns in percentage
    4) 🚩transform montlhy_returns dataframe to monthly last seven mean return in percentage droping missing data
    5) rank companies monthly
    6) create montlhy_wallet

    ### BACK TESTING
    7) create monthly returns dataframe
    8) create returns heatmap plot for sns
    9) create acum returns heatmap plot for sns
    10) create ibov acum returns heatmap plot for sns 
    11) compare model & ibov monthly returns
    12) create compare ibov returns heatmap plot for sns
    13) configure heatmaps

Below a example of how a code will be presented here.

```bash
#example of bash
print('Hello World!')
```