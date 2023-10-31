import requests
import pandas as pd
import os
import urllib.request
from dotenv import load_dotenv

class fintz_data:

    def __init__(self, data_path):

        load_dotenv()

        self.api_key = os.getenv("API_FINTZ")

        self.headers = {'accept': 'application/json',
                        'X-API-Key': self.api_key}
        os.chdir(data_path)

    def cdi(self):

        response = requests.get('https://api.fintz.com.br/taxas/historico?codigo=12&dataInicio=2000-01-01&ordem=ASC',
                                headers=self.headers)

        #print(response)

        cdi = pd.DataFrame(response.json())

        cdi = cdi.drop(["dataFim", 'nome'], axis = 1)

        cdi.columns = ['data', 'retorno']

        cdi['retorno'] = cdi['retorno']/100

        #print(cdi[cdi['ticker'] == 'WEGE3'])

        cdi.to_parquet('cdi.parquet', index = False)

    def ibov(self):

        response = requests.get('https://api.fintz.com.br/indices/historico?indice=IBOV&dataInicio=2000-01-01',
                                headers=self.headers)

        df = pd.DataFrame(response.json())

        df = df.sort_values('data', ascending=True)

        df.columns = ['indice', 'data', 'fechamento']

        df = df.drop('indice', axis = 1)

        #print(df[df['ticker'] == 'WEGE3'])

        df.to_parquet('ibov.parquet', index = False)          

    def getting_quotations(self):
        
        
        response = requests.get(f'https://api.fintz.com.br/bolsa/b3/avista/cotacoes/historico/arquivos?classe=ACOES&preencher=true', 
                                headers=self.headers)

        download_link = (response.json())['link']

        urllib.request.urlretrieve(download_link, f"cotacoes.parquet")

        df = pd.read_parquet('cotacoes.parquet')

        columns_to_adjust = ['preco_abertura', 'preco_maximo', 'preco_medio', 'preco_minimo']

        for coluna in columns_to_adjust:

            df[f'{coluna}_ajustado'] = df[coluna] * df['fator_ajuste']

        df['preco_fechamento_ajustado'] = df.groupby('ticker')['preco_fechamento_ajustado'].transform('ffill')

        df = df.sort_values('data', ascending=True)

        #print(df[df['ticker'] == 'WEGE3'])

        df.to_parquet('cotacoes.parquet', index = False) 

    def getting_accounting_files(self, demonstration = False, indicators = False, data_name = ''):

        if demonstration:

            try:

                response = requests.get(f'https://api.fintz.com.br/bolsa/b3/tm/demonstracoes/arquivos?item={data_name}',  
                                        headers=self.headers)
            
            except:

                print("Demonstração não encontrada!")
                exit()

            download_link = (response.json())['link']
            urllib.request.urlretrieve(download_link, f"{data_name}.parquet")
            #indicator = pd.read_parquet(f"{data_name}.parquet")
            #print(indicator[indicator['ticker'] == 'WEGE3'])
            #print(indicator)

        elif indicators:

            try:

                response = requests.get(f'https://api.fintz.com.br/bolsa/b3/tm/indicadores/arquivos?indicador={data_name}',  
                                        headers=self.headers)
            
            except:

                print("Indicador não encontrado!")
                exit()

            download_link = (response.json())['link']
            urllib.request.urlretrieve(download_link, f"{data_name}.parquet")
            #indicator = pd.read_parquet(f"{data_name}.parquet")
            #print(indicator[indicator['ticker'] == 'WEGE3'])
            #print(indicator)

        else:

            print("Escolha uma demonstração ou indicador.")


if __name__ == "__main__":

    reading_data = fintz_data(data_path=r'./finapp/files')

    demonstration_list = ['AcoesEmCirculacao', 'TotalAcoes']
                        # 'AcoesEmCirculacao', 'TotalAcoes'
                        # 'PatrimonioLiquido',
                        # 'LucroLiquido12m', 'LucroLiquido',
                        # 'ReceitaLiquida', 'ReceitaLiquida12m', 
                        # 'DividaBruta', 'DividaLiquida',
                        # 'Disponibilidades', 
                        # 'Ebit', 'Ebit12m',
                        # 'Impostos', 'Impostos12m',
                        # 'LucroLiquidoSociosControladora',
                        # 'LucroLiquidoSociosControladora12mEbit12m'

    indicators_list = ['L_P', 'ROE', 'ROIC'] #'EV', 'LPA', 'P_L', 'EBIT_EV', 'L_P', 'ROE', 'ROIC', 'ValorDeMercado']

    #for demonstration in demonstration_list:

    #    print(demonstration)

    #    reading_data.getting_accounting_files(demonstration=True, data_name = demonstration)

    #for indicador in indicators_list:

    #    print(indicador)

    #    reading_data.getting_accounting_files(indicators=True, data_name = indicador)

    #reading_data.cdi()
    #reading_data.getting_quotations()
    #reading_data.ibov()