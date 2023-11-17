import pandas as pd
import os
from dotenv import load_dotenv
import requests

class DownloadByApi:

    def __init__(self):
        
        print("Inicializing Downloader by API!")

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

    def getting_bc_data(self, bc_dict):

        self.bc_dict = bc_dict

        bc_codes_dict = {especitif_key: valor['bc_code'] for especitif_key, valor in self.bc_dict.items() if 'bc_code' in valor}
        # print(bc_codes_dict.values())
        # print(bc_codes_dict.keys())

        for name, code in bc_codes_dict.items():

            file_name = f'{name}.parquet'
            print('Data: ', name)

            url_banco_central = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados?formato=json'

            data = requests.get(url_banco_central)

            json_data = data.json()

            df = pd.DataFrame(json_data)

            df['data'] = pd.to_datetime(df['data'], format = '%d/%m/%Y')
            df = df.set_index('data')

            df['valor'] = df['valor'].astype(float)

            df = df.resample("M").last() #reorganizando os dados pra outra periodicidade.

            print(df)
        
            df.to_parquet(file_name, index = False)

if __name__ == "__main__":

    bc_dict = {
                    'selic':     {'bc_code': '432'},
                    'ipca':    {'bc_code': '433'},
                    'dolar':     {'bc_code': '1'},
                    # 'TEST':   {'bc_code': '2'},
                    }

    data = DownloadByApi()

    bc_data = data.getting_bc_data(bc_dict)