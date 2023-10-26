import pandas as pd
import os
import numpy as np
from statsmodels.regression.rolling import RollingOLS
import statsmodels.api as sm

#A COLUNA COM O INDICADOR TEM QUE SE CHAMAR "valor"

class MakeIndicator():

    def __init__(self, caminho_dados):

        os.chdir(caminho_dados)

    def fazer_indicador_momento(self, meses):

        cotacoes = pd.read_parquet('cotacoes.parquet')
        cotacoes['data'] = pd.to_datetime(cotacoes['data']).dt.date
        cotacoes = cotacoes[['data', 'ticker', 'preco_fechamento_ajustado']]

        cotacoes['valor'] = cotacoes.groupby('ticker')['preco_fechamento_ajustado'].pct_change(periods = (meses * 21))
        cotacoes.loc[cotacoes['valor'] == 0, 'valor'] = pd.NA
        cotacoes.loc[cotacoes['valor'] == np.inf, 'valor'] = pd.NA
        cotacoes = cotacoes.dropna()
        valor = cotacoes[['data', 'ticker', 'valor']]

        print(valor)

        valor.to_parquet(f'momento_{meses}_meses.parquet', index = False)

    def volume_mediano(self):

        cotacoes = pd.read_parquet('cotacoes.parquet')
        cotacoes['data'] = pd.to_datetime(cotacoes['data']).dt.date

        cotacoes = cotacoes[['data', 'ticker', 'volume_negociado']]
        cotacoes['volume_negociado'] = cotacoes.groupby('ticker')['volume_negociado'].fillna(0)
        cotacoes['valor'] = cotacoes.groupby('ticker')['volume_negociado'].rolling(21).median().reset_index(0,drop=True)
        cotacoes = cotacoes.dropna()
        valor = cotacoes[['data', 'ticker', 'valor']]

        print(valor)

        valor.to_parquet(f'volume_mediano.parquet', index = False)

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

        df_indicadores = pd.merge(df_ebit, df_divida_liquida, how = 'inner', on = 'id_dado')
        df_indicadores['ebit_DL'] = pd.NA
        df_indicadores.loc[df_indicadores['divida'] <= 0, 'ebit_DL'] = 999
        df_indicadores.loc[df_indicadores['ebit'] <= 0, 'ebit_DL'] = -999
        df_indicadores.loc[df_indicadores['ebit_DL'].isna(), 'ebit_DL'] = (df_indicadores[df_indicadores['ebit_DL'].isna()]['ebit']/
                                                                df_indicadores[df_indicadores['ebit_DL'].isna()]['divida'])
        df_indicadores = df_indicadores[['data', 'ticker', 'ebit_DL']]
        df_indicadores.columns = ['data', 'ticker', 'valor'] 

        df_indicadores.to_parquet(f'ebit_dl.parquet', index = False)

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

        df_indicadores = pd.merge(df_pl, df_divida_bruta, how = 'inner', on = 'id_dado')
        df_indicadores['PL_DB'] = pd.NA
        df_indicadores.loc[df_indicadores['patrimonio_liquido'] <= 0, 'PL_DB'] = 0
        df_indicadores.loc[df_indicadores['PL_DB'].isna(), 'PL_DB'] = (df_indicadores[df_indicadores['PL_DB'].isna()]['patrimonio_liquido']/
                                                                df_indicadores[df_indicadores['PL_DB'].isna()]['divida'])
        df_indicadores = df_indicadores[['data', 'ticker', 'PL_DB']]
        df_indicadores.columns = ['data', 'ticker', 'valor'] 

        df_indicadores.to_parquet('pl_db.parquet', index = False)

    def volatilidade(self, anos):

        cotacoes = pd.read_parquet('cotacoes.parquet')
        cotacoes['data'] = pd.to_datetime(cotacoes['data']).dt.date
        cotacoes = cotacoes[['data', 'ticker', 'preco_fechamento_ajustado']]
        cotacoes['retorno'] = cotacoes.groupby('ticker')['preco_fechamento_ajustado'].pct_change()
        cotacoes.loc[cotacoes['retorno'] == 0, 'retorno'] = pd.NA
        cotacoes.loc[cotacoes['retorno'] == np.inf, 'retorno'] = pd.NA
        cotacoes['valor'] = cotacoes.groupby('ticker')['retorno'].rolling(window=int(252 * anos), min_periods=int(252 * anos * 0.8)).std().reset_index(0,drop=True)
        cotacoes = cotacoes.dropna()
        cotacoes['valor'] = cotacoes['valor'] * np.sqrt(252) 
        valor = cotacoes[['data', 'ticker', 'valor']]

        print(valor)

        valor.to_parquet(f'vol_{int(252 * anos)}.parquet', index = False)

    def beta(self, anos):

        cotacoes = pd.read_parquet('cotacoes.parquet')
        cotaoces_ibov = pd.read_parquet('ibov.parquet')


        cotaoces_ibov.loc['5846'] = ['2023-08-10', 118349.60]

        cotaoces_ibov['retorno_ibov'] = cotaoces_ibov['fechamento'].pct_change()
        cotaoces_ibov = cotaoces_ibov[['data', 'retorno_ibov']]
        cotaoces_ibov['data'] = pd.to_datetime(cotaoces_ibov['data']).dt.date

        cotacoes['data'] = pd.to_datetime(cotacoes['data']).dt.date
        cotacoes = cotacoes[['data', 'ticker', 'preco_fechamento_ajustado']]
        cotacoes['retorno'] = cotacoes.groupby('ticker')['preco_fechamento_ajustado'].pct_change()
        cotacoes.loc[cotacoes['retorno'] == 0, 'retorno'] = pd.NA
        cotacoes.loc[cotacoes['retorno'] == np.inf, 'retorno'] = pd.NA

        dados_totais = pd.merge(cotacoes, cotaoces_ibov, on='data', how='inner')

        empresas = dados_totais['ticker'].unique()
        dados_totais = dados_totais.set_index('ticker')
        lista_df_betas = []

        for empresa in empresas:

            dado_empresa = dados_totais.loc[empresa]

            if dado_empresa.dropna().empty == False:

                if len(dado_empresa) > int(252 * anos):

                    datas = dado_empresa.data.values
                    exog = sm.add_constant(dado_empresa.retorno_ibov)
                    model = RollingOLS(endog=dado_empresa.retorno.values, exog=exog, 
                                    window=int(252 * anos), min_nobs = int(252 * anos * 0.8))
                    betas = model.fit()
                    betas = betas.params
                    dado_empresa = betas.reset_index()
                    dado_empresa['data'] = datas
                    dado_empresa.columns = ['ticker', 'const', 'valor', 'data']
                    dado_empresa = dado_empresa[['data', 'ticker', 'valor']]
                    dado_empresa = dado_empresa.dropna()
                    lista_df_betas.append(dado_empresa)

        betas = pd.concat(lista_df_betas)
        betas.to_parquet(f'beta_{int(252 * anos)}.parquet', index = False)

    def media_movel_proporcao(self, mm_curta, mm_longa):

        cotacoes = pd.read_parquet('cotacoes.parquet')
        cotacoes['data'] = pd.to_datetime(cotacoes['data']).dt.date
        cotacoes = cotacoes[['data', 'ticker', 'preco_fechamento_ajustado']]
        cotacoes['media_curta'] = cotacoes.groupby('ticker')['preco_fechamento_ajustado'].rolling(window=mm_curta, min_periods=int(mm_curta * 0.8)).mean().reset_index(0,drop=True)
        cotacoes['media_longa'] = cotacoes.groupby('ticker')['preco_fechamento_ajustado'].rolling(window=mm_longa, min_periods=int(mm_longa * 0.8)).mean().reset_index(0,drop=True)
        cotacoes['valor'] = cotacoes['media_curta']/cotacoes['media_longa']
        valor = cotacoes[['data', 'ticker', 'valor']]
        valor = valor.dropna()

        valor.to_parquet(f'mm_{mm_curta}_{mm_longa}.parquet', index = False)


if __name__ == "__main__":


    indicador = MakeIndicator(caminho_dados=r'./finapp/files')

    #indicador.fazer_indicador_momento(meses=12)
    #indicador.fazer_indicador_momento(meses=1)
    #indicador.fazer_indicador_momento(meses=6)
    #indicador.volume_mediano()
    #indicador.media_movel_proporcao(7, 40)
    #indicador.beta(1)
    #indicador.volatilidade(1)
    #indicador.pl_divida_bruta()