import pandas as pd
import os

class market_premium():

    def __init__(self, caminho_salvar_arquivo = '.', caminho_dados='.'):
        
        self.caminho_salvar_arquivo = caminho_salvar_arquivo
        self.caminho_dados = caminho_dados

    def calculando_premio(self):

        cdi = pd.read_parquet(f'{self.caminho_dados}/cdi.parquet')
        cdi['cota'] = (1 + cdi['retorno']).cumprod() - 1
        ibov = pd.read_parquet(f'{self.caminho_dados}/ibov.parquet')

        ibov_datas = ibov.sort_values('data', ascending = True)
        ibov_datas = ibov_datas.assign(year = pd.DatetimeIndex(ibov_datas['data']).year)
        ibov_datas = ibov_datas.assign(month = pd.DatetimeIndex(ibov_datas['data']).month)
        datas_final_mes = ibov_datas.groupby(['year', 'month'])['data'].last()
        dias_final_de_mes = datas_final_mes.to_list()

        ibov = ibov[ibov['data'].isin(dias_final_de_mes)]
        cdi = cdi[cdi['data'].isin(dias_final_de_mes)]
        ibov['retorno_ibov'] = ibov['fechamento'].pct_change()
        cdi['retorno_cdi'] = cdi['cota'].pct_change()
        ibov['data'] = ibov['data'].astype(str)
        cdi['data'] = cdi['data'].astype(str)

        df_dados_mercado = pd.merge(ibov, cdi, how = 'inner', on = "data")
        df_dados_mercado['mkt_premium'] = (1 + df_dados_mercado['retorno_ibov'])/(1 + df_dados_mercado['retorno_cdi']) - 1
        df_dados_mercado = df_dados_mercado.dropna()
        df_dados_mercado = df_dados_mercado[['data', 'mkt_premium']]
        df_dados_mercado['data'] = pd.to_datetime(df_dados_mercado['data']).dt.date

        print(df_dados_mercado)

        # configurando diretório de depósito dos arquivos
        diretorio_atual = os.getcwd()
        self.ponto_de_partida = os.path.dirname(os.path.abspath(__file__))
        self.ponto_de_partida = os.path.abspath(os.path.join(diretorio_atual, os.pardir))
        self.caminho_relativo = os.path.join(self.ponto_de_partida, "files", "premios_risco")

        df_dados_mercado.to_parquet(f'{self.caminho_salvar_arquivo}/market_premium.parquet', index = False)


if __name__ == "__main__":

    beta = market_premium(caminho_salvar_arquivo=r'./finapp/files/premios_risco',
                          caminho_dados=r'./finapp/files')

    beta.calculando_premio() 


    