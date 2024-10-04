import update_asset_profile as uap

import re
import requests
import pandas as pd
import os
import urllib.request
from dotenv import load_dotenv

import matplotlib.pyplot as plt

class FintzData:

    def __init__(self):

        print("Inicializing Downloader by Fintz!")

        load_dotenv()

        self.api_key = os.getenv("API_FINTZ")

        self.headers = {'accept': 'application/json',
                        'X-API-Key': self.api_key}
        
        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.databse_folder = os.getenv("DATABASE_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.databse_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)
        
        print("OK.")

    def download_cdi(self, initial_date):

        print("Downloading CDI!")

        cdi_download_link = os.getenv("CDI_DOWNLOAD_LINK")
        cdi_file_name = os.getenv("CDI_FILE_NAME")

        part_of_link_1 = '&dataInicio='
        part_of_link_2 = '&ordem=ASC'
        full_link = cdi_download_link + part_of_link_1 + initial_date + part_of_link_2

        response = requests.get(full_link, headers=self.headers)

        cdi = pd.DataFrame(response.json())

        cdi = cdi.drop(["dataFim", 'nome'], axis = 1)

        cdi.columns = ['data', 'retorno']

        cdi['retorno'] = cdi['retorno']/100

        #print(cdi[cdi['ticker'] == 'WEGE3'])

        cdi.to_parquet(cdi_file_name, index = False)
        
        print("OK.")

    def download_ibov(self, initial_date):

        print("Downloading IBOV!")
        
        ibov_download_link = os.getenv("IBOV_DOWNLOAD_LINK")
        ibov_file_name = os.getenv("IBOV_FILE_NAME")

        full_link = ibov_download_link + initial_date

        response = requests.get(full_link, headers=self.headers)

        ibov = pd.DataFrame(response.json())

        ibov = ibov.sort_values('data', ascending=True)

        ibov.columns = ['indice', 'data', 'fechamento']

        ibov = ibov.drop('indice', axis = 1)

        #print(df[df['ticker'] == 'WEGE3'])

        ibov.to_parquet(ibov_file_name, index = False)      
        
        print("OK.")    

    def download_quotations(self):
        
        print("Downloading Daily Quotations!")

        quotations_download_link = os.getenv("QUOTATIONS_DOWNLOAD_LINK")
        quotations_file_name = os.getenv("QUOTATIONS_FILE_NAME")

        response = requests.get(quotations_download_link, headers=self.headers)
        print(response)

        download_link = (response.json())['link']

        urllib.request.urlretrieve(download_link, f"cotacoes.parquet")

        quotations = pd.read_parquet('cotacoes.parquet')

        columns_to_adjust = ['preco_abertura', 'preco_maximo', 'preco_medio', 'preco_minimo']

        for coluna in columns_to_adjust:

            quotations[f'{coluna}_ajustado'] = quotations[coluna] * quotations['fator_ajuste']

        quotations['preco_fechamento_ajustado'] = quotations.groupby('ticker')['preco_fechamento_ajustado'].transform('ffill')

        quotations = quotations.sort_values('data', ascending=True)

        print(quotations)

        quotations.to_parquet(quotations_file_name, index = False)
        
        print("OK.")

    def download_accounting_files(self, demonstration = False, indicator = False, data_name = ''):

        if demonstration:

            print("Downloading demonstration: ", data_name)

            demonstrations_download_link = os.getenv("DEMONSTRATIONS_DOWNLOAD_LINK")
            full_link = demonstrations_download_link + data_name

            try:
                response = requests.get(full_link, headers=self.headers)
                print("OK.")
            
            except:
                print("Demonstração não encontrada!")
                exit()

            # print(response.json())
            download_link = (response.json())['link']

            urllib.request.urlretrieve(download_link, f"{data_name}.parquet")
            
            #indicator = pd.read_parquet(f"{data_name}.parquet")
            #print(indicator[indicator['ticker'] == 'WEGE3'])
            #print(indicator)

        elif indicator:

            print("Downloading indicator: ", data_name)
            
            indicators_download_link = os.getenv("INDICATORS_DOWNLOAD_LINK")
            full_link = indicators_download_link + data_name

            try:
                response = requests.get(full_link, headers=self.headers)
                print("OK.")
            except:
                print("Indicador não encontrado!")
                exit()

            # print(response.json())
            download_link = (response.json())['link']
            urllib.request.urlretrieve(download_link, f"{data_name}.parquet")
            
            #indicator = pd.read_parquet(f"{data_name}.parquet")
            #print(indicator[indicator['ticker'] == 'WEGE3'])
            #print(indicator)

        else:
            print("Escolha uma demonstração ou indicador.")

    def download_dividendyield(self):

        print("Downloading Dividend Yield")
        
        indicators_download_link = os.getenv("DIVIDENDYIELD_DOWNLOAD_LINK")
        full_link = indicators_download_link
        print(full_link)

        dividendyield_df = pd.DataFrame()

        # profile_updater = uap.UpdateAssetProfile()

        # assets_database_df = profile_updater.read_profile_database()

        # ticker_list = list(assets_database_df['ticker'])

        # ticker_list = [ticker for ticker in ticker_list if ticker is not None]

        URL_BASE = 'https://api.fintz.com.br'
        endpoint = URL_BASE + '/bolsa/b3/avista/busca'
        res = requests.get(endpoint, headers=self.headers)
        
        fintz_asset_list = res.json()

        print(fintz_asset_list)

        ticker_list = re.compile(r'^[A-Z]{4}(3|4|11)$')

        # Filtrar os tickers que seguem o padrão brasileiro
        ticker_list = [empresa['ticker'] for empresa in fintz_asset_list if ticker_list.match(empresa['ticker'])]

        print('ticker_list: \n',ticker_list)

        for ticker in ticker_list:

            print('ticker: ', ticker)

            params = { 'indicador': 'DividendYield', 'ticker': ticker }

            try:
                # response = requests.get(full_link, headers=self.headers)
                response = requests.get(full_link, headers=self.headers, params=params)
                print("OK.")
            except:
                print("Indicador não encontrado!")
                exit()

            # print(response.json())

            response_df = pd.DataFrame(response.json())
            # print ('response_df: \n', response_df)

            # dividendyield_df.append(response_df)
            # Concatenação vertical
            dividendyield_df = pd.concat([dividendyield_df, response_df], ignore_index=True)
            
            print ('dividendyield_df: \n', dividendyield_df)

        dividendyield_df.to_parquet('dividendyield.parquet', index = False)

    def download_accounting_files_new(self, data_name = ''):

        print("Downloading demonstration: ", data_name)

        demonstrations_download_link = os.getenv("DEMONSTRATIONS_DOWNLOAD_LINK_NEW")
        full_link = demonstrations_download_link
        print(full_link)

        accounting_item = pd.DataFrame()

        params = { 'item': data_name, 'tipoPeriodo': 'ANUAL'}

        try:
            # response = requests.get(full_link, headers=self.headers)
            response = requests.get(full_link, headers=self.headers, params=params)
            print(response)
            print("OK.")
        except:
            print("Item não encontrado!")
            exit()

        # print(response.json())

        response_df = pd.DataFrame(response.json())
        print ('response_df: \n', response_df)

        accounting_item = pd.concat([accounting_item, response_df], ignore_index=True)
        
        print ('accounting_item: \n', accounting_item)

        # accounting_item.to_parquet(f'{data_name}12m.parquet', index = False)

    def download_indicators(self, indicator = ''):

        print("Downloading Dividend Yield")
        
        indicators_download_link = os.getenv("DIVIDENDYIELD_DOWNLOAD_LINK")
        full_link = indicators_download_link
        print(full_link)

        indicators_df = pd.DataFrame()

        # profile_updater = uap.UpdateAssetProfile()

        # assets_database_df = profile_updater.read_profile_database()

        # ticker_list = list(assets_database_df['ticker'])

        # ticker_list = [ticker for ticker in ticker_list if ticker is not None]

        URL_BASE = 'https://api.fintz.com.br'
        endpoint = URL_BASE + '/bolsa/b3/avista/busca'
        res = requests.get(endpoint, headers=self.headers)
        
        fintz_asset_list = res.json()

        print(fintz_asset_list)

        ticker_list = re.compile(r'^[A-Z]{4}(3|4|11)$')

        # Filtrar os tickers que seguem o padrão brasileiro
        ticker_list = [empresa['ticker'] for empresa in fintz_asset_list if ticker_list.match(empresa['ticker'])]

        print('ticker_list: \n',ticker_list)

        for ticker in ticker_list:

            print('ticker: ', ticker)

            params = { 'indicador': indicator, 'ticker': ticker }

            try:
                # response = requests.get(full_link, headers=self.headers)
                response = requests.get(full_link, headers=self.headers, params=params)
                print("OK.")
            except:
                print("Indicador não encontrado!")
                exit()

            # print(response.json())

            response_df = pd.DataFrame(response.json())
            # print ('response_df: \n', response_df)

            # indicators_df.append(response_df)
            # Concatenação vertical
            indicators_df = pd.concat([indicators_df, response_df], ignore_index=True)
            
            print ('indicators_df: \n', indicators_df)

        indicators_df = indicators_df[['ticker', 'data', 'valor']]
        indicators_df = indicators_df.sort_values(['data', 'ticker'])
        indicators_df['valor'] = 1/indicators_df['valor']
        indicators_df.to_parquet('indicators-testtttt.parquet', index = False)






if __name__ == "__main__":

    data_from_fintz = FintzData()

    # data_from_fintz.download_accounting_files_new(data_name='PatrimonioLiquido')
    # data_from_fintz.download_accounting_files_new(data_name='Disponibilidades')
    # data_from_fintz.download_indicators(indicator='P_VP')

    
    start_date = '2024-08-25'
    end_date = '2024-08-29'

    indicators = pd.read_parquet('p_vp_invert.parquet')

    # print('indicators: \n', indicators)
    print(indicators[indicators['ticker']=='CMIG4'])


    # pvp = pd.read_parquet('p_vp_invert.parquet')
    # pvp = pvp[(pvp['data'] >= start_date) & (pvp['data'] <= end_date)]

    # print('pvp: \n', pvp)
    # print(pvp[pvp['ticker']=='CMIG4'])

    # total_number_of_stocks = total_number_of_stocks[['ticker', 'data', 'valor']]
    # total_number_of_stocks = total_number_of_stocks.rename(columns={'valor': 'valor_nos'})
    # total_number_of_stocks['data'] = pd.to_datetime(total_number_of_stocks['data'])
    # total_number_of_stocks['ticker'] = total_number_of_stocks['ticker'].astype(str)
    # total_number_of_stocks['valor_nos'] = total_number_of_stocks['valor_nos'].astype(float)




    # # Dados das empresas que você deseja plotar
    # empresas = ['PFRM3', 'USIM5', 'WEGE3']  # Adicione aqui os tickers das empresas desejadas

    # # Filtrando os dados apenas para as empresas selecionadas
    # dados_empresas_selecionadas = total_number_of_stocks[total_number_of_stocks['ticker'].isin(empresas)].copy()

    # # Convertendo a coluna 'data' para o tipo datetime usando .loc
    # dados_empresas_selecionadas.loc[:, 'data'] = pd.to_datetime(dados_empresas_selecionadas['data'])

    # # Criando uma figura e um eixo
    # fig, ax = plt.subplots(figsize=(10, 6))

    # # Loop sobre cada empresa para plotar seus dados
    # for empresa in empresas:
    #     dados_empresa = dados_empresas_selecionadas[dados_empresas_selecionadas['ticker'] == empresa]
    #     ax.plot(dados_empresa['data'], dados_empresa['valor_nos'], label=empresa)

    # # Adicionando título e rótulos aos eixos
    # ax.set_title('Valor nos últimos diários das empresas selecionadas')
    # ax.set_xlabel('Data')
    # ax.set_ylabel('Valor nos')
    # ax.legend()

    # # Rotacionando as datas no eixo x para melhor legibilidade
    # plt.xticks(rotation=45)

    # # Exibindo o gráfico
    # plt.tight_layout()
    # plt.show()