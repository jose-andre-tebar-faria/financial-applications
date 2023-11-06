import pandas as pd
import os
import numpy as np
from statsmodels.regression.rolling import RollingOLS
import statsmodels.api as sm

#A COLUNA COM O INDICADOR TEM QUE SE CHAMAR "valor"

class MakeIndicator():

    def __init__(self, data_path):

        os.chdir(data_path)

    def making_momentum(self, months):

        output_df = pd.DataFrame()
        quotations = pd.read_parquet('cotacoes.parquet')
        quotations['data'] = pd.to_datetime(quotations['data']).dt.date
        quotations = quotations[['data', 'ticker', 'preco_fechamento_ajustado']]

        quotations['valor'] = quotations.groupby('ticker')['preco_fechamento_ajustado'].pct_change(periods = (months * 21))
        quotations.loc[quotations['valor'] == 0, 'valor'] = pd.NA
        quotations.loc[quotations['valor'] == np.inf, 'valor'] = pd.NA
        quotations = quotations.dropna()
        output_df = quotations[['data', 'ticker', 'valor']]

        #print(output_df[output_df['ticker'] == 'WEGE3'])

        output_df.to_parquet(f'momento_{months}_meses.parquet', index = False)

    def median_volume(self):

        output_df = pd.DataFrame()
        quotations = pd.read_parquet('cotacoes.parquet')
        quotations['data'] = pd.to_datetime(quotations['data']).dt.date

        quotations = quotations[['data', 'ticker', 'volume_negociado']]
        quotations['volume_negociado'] = quotations.groupby('ticker')['volume_negociado'].fillna(0)
        quotations['valor'] = quotations.groupby('ticker')['volume_negociado'].rolling(21).median().reset_index(0,drop=True)
        quotations = quotations.dropna()
        output_df = quotations[['data', 'ticker', 'valor']]

        #print(output_df[output_df['ticker'] == 'WEGE3'])

        output_df.to_parquet(f'volume_mediano.parquet', index = False)

    def ebit_divida_liquida(self):

        df_ebit = pd.read_parquet('Ebit12m.parquet')
        df_ebit = df_ebit.assign(id_dado = df_ebit['ticker'].astype(str) + "_" + df_ebit['data'].astype(str))
        df_ebit['valor'] = df_ebit['valor'].astype(float)
        df_ebit = df_ebit[['ticker', 'data', 'id_dado', 'valor']]
        df_ebit.columns = ['ticker', 'data', 'id_dado', 'ebit']

        df_divida_liquida = pd.read_parquet('DividaLiquida.parquet')
        df_divida_liquida = df_divida_liquida.assign(id_dado = df_divida_liquida['ticker'].astype(str) + "_" + df_divida_liquida['data'].astype(str))
        df_divida_liquida['valor'] = df_divida_liquida['valor'].astype(float)
        df_divida_liquida = df_divida_liquida[['id_dado', 'valor']]
        df_divida_liquida.columns = ['id_dado', 'divida']

        output_df = pd.DataFrame()
        output_df = pd.merge(df_ebit, df_divida_liquida, how = 'inner', on = 'id_dado')
        output_df['ebit_DL'] = pd.NA
        output_df.loc[output_df['divida'] <= 0, 'ebit_DL'] = 999
        output_df.loc[output_df['ebit'] <= 0, 'ebit_DL'] = -999
        output_df.loc[output_df['ebit_DL'].isna(), 'ebit_DL'] = (output_df[output_df['ebit_DL'].isna()]['ebit']/
                                                                output_df[output_df['ebit_DL'].isna()]['divida'])
        output_df = output_df[['data', 'ticker', 'ebit_DL']]
        output_df.columns = ['data', 'ticker', 'valor'] 

        #print(output_df[output_df['ticker'] == 'WEGE3'])

        output_df.to_parquet(f'ebit_dl.parquet', index = False)

    def pl_divida_bruta(self):

        df_pl = pd.read_parquet('PatrimonioLiquido.parquet')
        df_pl = df_pl.dropna()
        df_pl = df_pl.assign(id_dado = df_pl['ticker'].astype(str) + "_" + df_pl['data'].astype(str))
        df_pl['valor'] = df_pl['valor'].astype(float)
        df_pl = df_pl[['data', 'ticker', 'valor', 'id_dado']]
        df_pl.columns = ['data', 'ticker', 'patrimonio_liquido', 'id_dado']

        df_divida_bruta = pd.read_parquet('DividaBruta.parquet')
        df_divida_bruta[df_divida_bruta['valor'] == '0.0'] = pd.NA
        df_divida_bruta = df_divida_bruta.dropna()
        df_divida_bruta = df_divida_bruta.assign(id_dado = df_divida_bruta['ticker'].astype(str) + "_" + df_divida_bruta['data'].astype(str))
        df_divida_bruta['valor'] = df_divida_bruta['valor'].astype(float)
        df_divida_bruta = df_divida_bruta[['id_dado', 'valor']]
        df_divida_bruta.columns = ['id_dado', 'divida']

        output_df = pd.DataFrame()
        output_df = pd.merge(df_pl, df_divida_bruta, how = 'inner', on = 'id_dado')
        output_df['PL_DB'] = pd.NA
        output_df.loc[output_df['patrimonio_liquido'] <= 0, 'PL_DB'] = 0
        output_df.loc[output_df['PL_DB'].isna(), 'PL_DB'] = (output_df[output_df['PL_DB'].isna()]['patrimonio_liquido']/
                                                                output_df[output_df['PL_DB'].isna()]['divida'])
        output_df = output_df[['data', 'ticker', 'PL_DB']]
        output_df.columns = ['data', 'ticker', 'valor'] 

        #print(output_df[output_df['ticker'] == 'WEGE3'])

        output_df.to_parquet('pl_db.parquet', index = False)

    def volatility(self, years):

        output_df = pd.DataFrame()
        quotations = pd.read_parquet('cotacoes.parquet')
        quotations['data'] = pd.to_datetime(quotations['data']).dt.date
        quotations = quotations[['data', 'ticker', 'preco_fechamento_ajustado']]
        quotations['retorno'] = quotations.groupby('ticker')['preco_fechamento_ajustado'].pct_change()
        quotations.loc[quotations['retorno'] == 0, 'retorno'] = pd.NA
        quotations.loc[quotations['retorno'] == np.inf, 'retorno'] = pd.NA
        quotations['valor'] = quotations.groupby('ticker')['retorno'].rolling(window=int(252 * years), min_periods=int(252 * years * 0.8)).std().reset_index(0,drop=True)
        quotations = quotations.dropna()
        quotations['valor'] = quotations['valor'] * np.sqrt(252) 
        output_df = quotations[['data', 'ticker', 'valor']]

        #print(output_df[output_df['ticker'] == 'WEGE3'])

        output_df.to_parquet(f'vol_{int(252 * years)}.parquet', index = False)

    def beta(self, years):

        quotations = pd.read_parquet('cotacoes.parquet')
        cotaoces_ibov = pd.read_parquet('ibov.parquet')


        cotaoces_ibov.loc['5846'] = ['2023-08-10', 118349.60]

        cotaoces_ibov['retorno_ibov'] = cotaoces_ibov['fechamento'].pct_change()
        cotaoces_ibov = cotaoces_ibov[['data', 'retorno_ibov']]
        cotaoces_ibov['data'] = pd.to_datetime(cotaoces_ibov['data']).dt.date

        quotations['data'] = pd.to_datetime(quotations['data']).dt.date
        quotations = quotations[['data', 'ticker', 'preco_fechamento_ajustado']]
        quotations['retorno'] = quotations.groupby('ticker')['preco_fechamento_ajustado'].pct_change()
        quotations.loc[quotations['retorno'] == 0, 'retorno'] = pd.NA
        quotations.loc[quotations['retorno'] == np.inf, 'retorno'] = pd.NA

        dados_totais = pd.merge(quotations, cotaoces_ibov, on='data', how='inner')

        empresas = dados_totais['ticker'].unique()
        dados_totais = dados_totais.set_index('ticker')
        lista_df_betas = []

        for empresa in empresas:

            dado_empresa = dados_totais.loc[empresa]

            if dado_empresa.dropna().empty == False:

                if len(dado_empresa) > int(252 * years):

                    datas = dado_empresa.data.values
                    exog = sm.add_constant(dado_empresa.retorno_ibov)
                    model = RollingOLS(endog=dado_empresa.retorno.values, exog=exog, 
                                    window=int(252 * years), min_nobs = int(252 * years * 0.8))
                    betas = model.fit()
                    betas = betas.params
                    dado_empresa = betas.reset_index()
                    dado_empresa['data'] = datas
                    dado_empresa.columns = ['ticker', 'const', 'valor', 'data']
                    dado_empresa = dado_empresa[['data', 'ticker', 'valor']]
                    dado_empresa = dado_empresa.dropna()
                    lista_df_betas.append(dado_empresa)

        betas = pd.concat(lista_df_betas)
        
        #print(betas[betas['ticker'] == 'WEGE3'])

        betas.to_parquet(f'beta_{int(252 * years)}.parquet', index = False)

    def ratio_moving_mean(self, mm_curta, mm_longa):

        output_df = pd.DataFrame()
        quotations = pd.read_parquet('cotacoes.parquet')
        quotations['data'] = pd.to_datetime(quotations['data']).dt.date
        quotations = quotations[['data', 'ticker', 'preco_fechamento_ajustado']]
        quotations['media_curta'] = quotations.groupby('ticker')['preco_fechamento_ajustado'].rolling(window=mm_curta, min_periods=int(mm_curta * 0.8)).mean().reset_index(0,drop=True)
        quotations['media_longa'] = quotations.groupby('ticker')['preco_fechamento_ajustado'].rolling(window=mm_longa, min_periods=int(mm_longa * 0.8)).mean().reset_index(0,drop=True)
        quotations['valor'] = quotations['media_curta']/quotations['media_longa']
        output_df = quotations[['data', 'ticker', 'valor']]
        output_df = output_df.dropna()

        #print(output_df[output_df['ticker'] == 'WEGE3'])

        output_df.to_parquet(f'mm_{mm_curta}_{mm_longa}.parquet', index = False)


if __name__ == "__main__":


    indicator = MakeIndicator(data_path=r'./finapp/files')

    #indicator.making_momentum(months=12)
    #indicator.making_momentum(months=1)
    #indicator.making_momentum(months=6)
    #indicator.median_volume()
    #indicator.ratio_moving_mean(7, 40)
    #indicator.beta(1)
    indicator.volatility(1)
    indicator.pl_divida_bruta()
    indicator.ebit_divida_liquida()