import requests
import pandas as pd
import os
import urllib.request
from dotenv import load_dotenv

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

        download_link = (response.json())['link']

        urllib.request.urlretrieve(download_link, f"cotacoes.parquet")

        quotations = pd.read_parquet('cotacoes.parquet')

        columns_to_adjust = ['preco_abertura', 'preco_maximo', 'preco_medio', 'preco_minimo']

        for coluna in columns_to_adjust:

            quotations[f'{coluna}_ajustado'] = quotations[coluna] * quotations['fator_ajuste']

        quotations['preco_fechamento_ajustado'] = quotations.groupby('ticker')['preco_fechamento_ajustado'].transform('ffill')

        quotations = quotations.sort_values('data', ascending=True)

        #print(df[df['ticker'] == 'WEGE3'])

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

            download_link = (response.json())['link']
            urllib.request.urlretrieve(download_link, f"{data_name}.parquet")
            
            #indicator = pd.read_parquet(f"{data_name}.parquet")
            #print(indicator[indicator['ticker'] == 'WEGE3'])
            #print(indicator)

        else:
            print("Escolha uma demonstração ou indicador.")