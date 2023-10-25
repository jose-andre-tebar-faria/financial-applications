import requests
import pandas as pd
import os
import urllib.request
from dotenv import load_dotenv

class dados_fintz:

    def __init__(self, caminho_dados):

        load_dotenv()

        self.chave_api = os.getenv("API_FINTZ")

        self.headers = {'accept': 'application/json',
                        'X-API-Key': self.chave_api}
        os.chdir(caminho_dados)

    def cdi(self):

        response = requests.get('https://api.fintz.com.br/taxas/historico?codigo=12&dataInicio=2000-01-01&ordem=ASC',
                                headers=self.headers)

        print(response)

        cdi = pd.DataFrame(response.json())

        cdi = cdi.drop(["dataFim", 'nome'], axis = 1)

        cdi.columns = ['data', 'retorno']

        cdi['retorno'] = cdi['retorno']/100

        print(cdi)

        cdi.to_parquet('cdi.parquet', index = False)

    def ibov(self):

        response = requests.get('https://api.fintz.com.br/indices/historico?indice=IBOV&dataInicio=2000-01-01',
                                headers=self.headers)

        df = pd.DataFrame(response.json())

        df = df.sort_values('data', ascending=True)

        df.columns = ['indice', 'data', 'fechamento']

        df = df.drop('indice', axis = 1)

        print(df)

        df.to_parquet('ibov.parquet', index = False)          

    def pegar_cotacoes(self):
        
        
        response = requests.get(f'https://api.fintz.com.br/bolsa/b3/avista/cotacoes/historico/arquivos?classe=ACOES&preencher=true', 
                                headers=self.headers)

        link_download = (response.json())['link']

        urllib.request.urlretrieve(link_download, f"cotacoes.parquet")

        df = pd.read_parquet('cotacoes.parquet')

        colunas_pra_ajustar = ['preco_abertura', 'preco_maximo', 'preco_medio', 'preco_minimo']

        for coluna in colunas_pra_ajustar:

            df[f'{coluna}_ajustado'] = df[coluna] * df['fator_ajuste']

        df['preco_fechamento_ajustado'] = df.groupby('ticker')['preco_fechamento_ajustado'].transform('ffill')

        df = df.sort_values('data', ascending=True)

        print(df)

        df.to_parquet('cotacoes.parquet', index = False) 

    def pegando_arquivo_contabil(self, demonstracao = False, indicadores = False, nome_dado = ''):

        if demonstracao:

            try:

                response = requests.get(f'https://api.fintz.com.br/bolsa/b3/tm/demonstracoes/arquivos?item={nome_dado}',  
                                        headers=self.headers)
            
            except:

                print("Demonstração não encontrada!")
                exit()

            link_download = (response.json())['link']
            urllib.request.urlretrieve(link_download, f"{nome_dado}.parquet")

        elif indicadores:

            try:

                response = requests.get(f'https://api.fintz.com.br/bolsa/b3/tm/indicadores/arquivos?indicador={nome_dado}',  
                                        headers=self.headers)
            
            except:

                print("Indicador não encontrado!")
                exit()

            link_download = (response.json())['link']
            urllib.request.urlretrieve(link_download, f"{nome_dado}.parquet")

        else:

            print("Escolha uma demonstração ou indicador.")


if __name__ == "__main__":

    lendo_dados = dados_fintz(caminho_dados=r'.\finapp\files')

    lista_demonstracoes = ['Ebit12m', 'DividaBruta', 'DividaLiquida', 'Ebit12m', 'LucroLiquido12m', 'PatrimonioLiquido', 'ReceitaLiquida12m']
    lista_indicadores = ['EBIT_EV', 'L_P', 'ROE', 'ROIC', 'ValorDeMercado']

    #for demonstracao in lista_demonstracoes:

    #    print(demonstracao)

    #    lendo_dados.pegando_arquivo_contabil(demonstracao=True, nome_dado = demonstracao)

    #for indicador in lista_indicadores:

    #    print(indicador)

    #    lendo_dados.pegando_arquivo_contabil(indicadores=True, nome_dado = indicador)

    #lendo_dados.cdi()
    #lendo_dados.pegar_cotacoes()
    #lendo_dados.ibov()