#pip install yfinance, pandas, quantstats, openpyxl, matplotlib, numpy

import yfinance as yf
import pandas as pd
import quantstats as qs

#qs.extend_pandas()

import numpy as np
import matplotlib.pyplot as plt
import monthly_returns_heatmap as mrh

tickers = pd.DataFrame()
comp_historica = pd.DataFrame()
retorno_mensal = pd.DataFrame()
retorno_modelo = pd.DataFrame()

comp_historica = pd.read_excel('seven_mean_factor_investing\composicao_ibov.xlsx')
tickers = pd.read_excel('seven_mean_factor_investing\composicao_ibov.xlsx', sheet_name = 'lista_acoes')

dados_cotacoes = yf.download(tickers = tickers['tickers'].to_list(), start = "2015-05-29", end = "2022-12-31")['Adj Close']

dados_cotacoes.index = pd.to_datetime(dados_cotacoes.index)
dados_cotacoes = dados_cotacoes.sort_index()

r7 = (dados_cotacoes.resample("M").last().pct_change().rolling(7).mean().dropna(axis = 0, how = "all").drop('2022-12-31'))

for data in r7.index:
    for empresa in r7.columns:

        if empresa.replace(".SA", "") not in comp_historica.loc[:, data].to_list():

            r7.loc[data, empresa] = pd.NA

carteiras = r7.rank(axis = 1, ascending = False)

for data in carteiras.index:
    for empresa in carteiras.columns:

        if carteiras.loc[data, empresa] < 9:

            carteiras.loc[data, empresa] = 1
            
        else:
            
            carteiras.loc[data, empresa] = 0

retorno_mensal = dados_cotacoes.resample("M").last().pct_change()
retorno_mensal = retorno_mensal.drop(retorno_mensal.index[:8], axis = 0)
carteiras.index = retorno_mensal.index

retorno_modelo = (carteiras * retorno_mensal).sum(axis = 1)/8

retorno_modelo.index = pd.to_datetime(retorno_modelo.index)
retorno_modelo = retorno_modelo.sort_index()

print(retorno_modelo.tail())

#qs.plots.monthly_heatmap(retorno_modelo,ylabel=True,savefig=None,figsize=8,show=True)

#retorno_modelo.plot_monthly_heatmap()

help(qs.plots.monthly_heatmap)
