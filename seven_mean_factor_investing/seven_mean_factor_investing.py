#pip install yfinance, pandas, quantstats, openpyxl, matplotlib, numpy, seaborn

#importing libraries
import os
import yfinance as yf
import pandas as pd
import quantstats as qs
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

#defining initian variables
hist_composition = pd.DataFrame()
tickers = pd.DataFrame()
price_data = []
sevem_mean_model = []
monthly_wallets = pd.DataFrame()
montlhy_returns = pd.DataFrame()
model_returns = pd.DataFrame()

#reading total and monthly ibov indices compose
hist_composition = pd.read_excel('seven_mean_factor_investing\composicao_ibov.xlsx')
tickers = pd.read_excel('seven_mean_factor_investing\composicao_ibov.xlsx', sheet_name = 'lista_acoes')

#downloading all needed data
price_data = yf.download(tickers = tickers['tickers'].to_list(), start = "2015-05-29", end = "2022-12-31")['Adj Close']
ibovespa = yf.download("^BVSP", start = "2015-12-30", end = "2022-12-31")['Adj Close']

#transforming price_data index to datetime format
price_data.index = pd.to_datetime(price_data.index)
price_data = price_data.sort_index()

#
##
### MODELING
##
#

#calculating monthly returns in percentage
montlhy_returns = price_data.resample("M").last().pct_change()


#MAGIC! - transforming montlhy_returns dataframe to monthly last seven mean return in percentage droping missing data
sevem_mean_model = (montlhy_returns.rolling(7).mean().dropna(axis = 0, how = "all").drop('2022-12-31'))

print(sevem_mean_model)

#locating companies that are present at ibov each month
for date in sevem_mean_model.index:
    for company in sevem_mean_model.columns:
        if company.replace(".SA", "") not in hist_composition.loc[:, date].to_list():

            sevem_mean_model.loc[date, company] = pd.NA

#ranking companies monthly
monthly_wallets = sevem_mean_model.rank(axis = 1, ascending = False)

#creating montlhy_wallet, a 0/1 dataframe representing the TOP8 companies  
for date in monthly_wallets.index:
    for company in monthly_wallets.columns:
        if monthly_wallets.loc[date, company] < 9:
            monthly_wallets.loc[date, company] = 1
        else:
            monthly_wallets.loc[date, company] = 0

#
##
### BACK TESTING
##
#

#preparing montlhy_returns dataframe to calculate returns from model
montlhy_returns = montlhy_returns.drop(montlhy_returns.index[:8], axis = 0)
monthly_wallets.index = montlhy_returns.index

#creating monthly returns dataframe
model_returns = (monthly_wallets * montlhy_returns).sum(axis = 1)/8

#creating returns heatmap plot for sns -> retorno_modelo_pivot
model_returns_dict = {'Retorno': model_returns}
model_returns_df = pd.DataFrame(model_returns_dict)
model_returns_df['Ano'] = model_returns_df.index.year
model_returns_df['Mês'] = model_returns_df.index.month
model_returns_pivot = model_returns_df.pivot(index='Ano', columns='Mês', values='Retorno')

#creating acum returns heatmap plot for sns -> retorno_acum_modelo_pivot
model_acum_returns = (1 + model_returns).cumprod() - 1 

model_acum_returns_dict = {'Retorno': model_acum_returns}
model_acum_returns_df = pd.DataFrame(model_acum_returns_dict)
model_acum_returns_df['Ano'] = model_acum_returns_df.index.year
model_acum_returns_df['Mês'] = model_acum_returns_df.index.month
acum_model_returns_pivot = model_acum_returns_df.pivot(index='Ano', columns='Mês', values='Retorno')

#creating ibov acum returns heatmap plot for sns -> retorno_acum_ibov_pivot
ibovespa_returns = ibovespa.resample("M").last().pct_change().dropna()
ibov_acum_returns = (1 + ibovespa_returns).cumprod() - 1 

ibov_acum_returns_dict = {'Retorno': ibov_acum_returns}
ibov_acum_returns_df = pd.DataFrame(ibov_acum_returns_dict)
ibov_acum_returns_df['Ano'] = ibov_acum_returns_df.index.year
ibov_acum_returns_df['Mês'] = ibov_acum_returns_df.index.month
ibov_acum_returns_pivot = ibov_acum_returns_df.pivot(index='Ano', columns='Mês', values='Retorno')

#comparing model & ibov monthly returns
compare_model_ibov = model_returns - ibovespa_returns

#creating compare ibov returns heatmap plot for sns -> compare_model_ibov
compare_model_ibov_dict = {'Retorno': compare_model_ibov}
compare_model_ibov_df = pd.DataFrame(compare_model_ibov_dict)
compare_model_ibov_df['Ano'] = compare_model_ibov_df.index.year
compare_model_ibov_df['Mês'] = compare_model_ibov_df.index.month
compare_model_ibov_pivot = compare_model_ibov_df.pivot(index='Ano', columns='Mês', values='Retorno')

#configuring heatmaps
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10,8))

sns.heatmap(model_returns_pivot, ax=axs[0,0], cmap='RdYlGn', cbar_kws={'format': mtick.PercentFormatter(xmax=1, decimals=0)}, center=0, annot=True, fmt='.1%', annot_kws={'fontsize':8}, robust=True)
axs[0,0].set_title('MODEL MONTHLY RETURNS')

sns.heatmap(acum_model_returns_pivot, ax=axs[1,0], cmap='RdYlGn', cbar_kws={'format': mtick.PercentFormatter(xmax=1, decimals=0)}, center=0, annot=True, fmt='.1%', annot_kws={'fontsize':7}, robust=True)
axs[1,0].set_title('MODEL ACUM MONTHLY RETURNS')

sns.heatmap(compare_model_ibov_pivot, ax=axs[0,1], cmap='RdYlGn', cbar_kws={'format': mtick.PercentFormatter(xmax=1, decimals=0)}, center=0, annot=True, fmt='.1%', annot_kws={'fontsize':8}, robust=True)
axs[0,1].set_title('MODEL VS IBOV MONTHLY RETURNS')

sns.heatmap(ibov_acum_returns_pivot, ax=axs[1,1], cmap='RdYlGn', cbar_kws={'format': mtick.PercentFormatter(xmax=1, decimals=0)}, center=0, annot=True, fmt='.1%', annot_kws={'fontsize':7}, robust=True)
axs[1,1].set_title('IBOV ACUM MONTHLY RETURNS')

#defining labels as percentage
plt.xticks(np.arange(0.5, 5.5, step=1), np.arange(1, 6, step=1))
plt.yticks(np.arange(0.5, 5.5, step=1), np.arange(1, 6, step=1))

#configuring & saving heatmap figure
fig.set_size_inches(15, 10)

output_dir = 'seven_mean_factor_investing/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
plt.savefig(os.path.join(output_dir, 'seven_mean_heatmaps.png'), dpi=300)

#plotting
plt.tight_layout()
plt.show()