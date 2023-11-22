import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import update_asset_profile as uap

class WalletManager:

    def __init__(self):
         
        print("\nInicializing Wallet Manager!")

        load_dotenv()

        current_folder = os.getcwd()

        project_folder = os.getenv("PROJECT_FOLDER")
        databse_folder = os.getenv("DATABASE_FOLDER")
        self.full_desired_path = os.path.join(project_folder,databse_folder)

        if(current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

#
##
###
# PREPARANDO DADOS
###
##
#
    def preparing_setup_data(self, setups_dict, user_name, create_date):
        
        self.setups_dict = setups_dict

        setups_dataframe = pd.DataFrame(columns=['wallet_id', 'wallet_name', 'user_name', 'proportion', 'create_date', 'close_date'])
        # setups_dataframe = setups_dataframe.set_index('wallet_name', drop=True)
        setups_dataframe['create_date'] = pd.to_datetime(setups_dataframe['create_date'])
        setups_dataframe['close_date'] = pd.to_datetime(setups_dataframe['close_date'])

        wallet_index = 0

        for wallet_name, wallet in setups_dict.items():

            indicador_index = 1

            setups_dataframe.loc[wallet_index, 'wallet_id'] = 'first-shot'
            setups_dataframe.loc[wallet_index, 'wallet_name'] = wallet_name
            setups_dataframe.loc[wallet_index, 'user_name'] = user_name
            setups_dataframe.loc[wallet_index, 'proportion'] = wallet['peso']
            setups_dataframe.loc[wallet_index, 'create_date'] = create_date

            indicadores = wallet['indicadores']
            
            for indicador, ordem in indicadores.items():

                setups_dataframe.loc[wallet_index, f'indicator_{indicador_index}'] = indicador
                indicador_index+=1

            wallet_index+=1

        # print(setups_dataframe)
            
        return setups_dataframe

#
##
###
# LENDO SETUPS
###
##
#
    def read_setups(self):

        file_not_found = False

        try:
            wallets_parquet = pd.read_parquet(f'{self.full_desired_path}/wallets.parquet')
            wallets_df = pd.DataFrame(wallets_parquet)
            print('Wallet setup: \n', wallets_df)
        except:
            wallets_df = None
            file_not_found = True
            print("File not found.")

        return file_not_found, wallets_df
        
#
##
###
# INSERINDO SETUP NO DATABASE
###
##
#
    def insert_setup(self, new_setup):
        
        print('New setup: \n', new_setup)

        file_not_found, setups_df = wallet_manager.read_setups()
        # print('Setup database: \n', setups_df)

        if(file_not_found):

            print('\t+++creating file wallets.parquet.')
            
            # print('Setup updated: \n', new_setup)
            new_setup.to_parquet(f'{self.full_desired_path}/wallets.parquet', index = True)
        else:
            
            df_merge = pd.merge(setups_df, new_setup, on=['wallet_id', 'create_date', 'user_name'], how='left', indicator=True)
            esta_contido = (df_merge['_merge'] == 'both').any()
            # print(esta_contido)

            if(esta_contido):
                print('Setup duplicated!')
                
                print('\t--- nothing to do!')
            else:
                print('New setup!')

                # Obter o maior valor do índice do DataFrame à esquerda
                max_setup_index = setups_df.index.max()
                print('max_setup_index: ', max_setup_index)

                # Ajustar o índice do DataFrame à direita
                # setup_to_concat = new_setup.reset_index(drop=True) + int(max_setup_index) + 1

                setup_to_concat = new_setup.copy()  # Criar uma cópia para evitar alterar o DataFrame original
                if(np.isnan(max_setup_index)):
                    print('First setup!')
                else:
                    setup_to_concat.index = setup_to_concat.index + max_setup_index + 1

                print('Wallet to concat: \n', setup_to_concat)

                print('\t...updating file wallets.parquet.')
            
                updated_setup = pd.concat([setups_df, setup_to_concat], ignore_index=False)
                print('Setup updated: \n', updated_setup)

                updated_setup.to_parquet(f'{self.full_desired_path}/wallets.parquet', index = True)

#
##
###
# APAGANDO SETUPS
###
##
#
    def delete_setup(self, wallet_id, user_name):

        file_not_found, setups_df = wallet_manager.read_setups()
        # print('Setup database: \n', setups_df)

        if(file_not_found):
            print('\twallets.parquet does not exist!')
        else:
            condition = (setups_df['wallet_id'] == wallet_id) & (setups_df['user_name'] == user_name)
            setup_to_delete = setups_df[condition]
            print('Setup to delete: \n', setup_to_delete)

            if(setup_to_delete.empty):
                print('Setup does not exist!')
            else:
                # new_setup = setups_df.loc[(setups_df['wallet_id'] != wallet_id) & (setups_df['user_name'] != user_name)]
                new_setup = setups_df.drop(setups_df[condition].index)
                print('New setup: \n', new_setup)
                
                new_setup.to_parquet(f'{self.full_desired_path}/wallets.parquet', index = True)

#
##
###
# FECHANDO SETUPS
###
##
#
    def close_setup(self, wallet_id, user_name, close_date):

        file_not_found, setups_df = wallet_manager.read_setups()

        if(file_not_found):
                print('\twallets.parquet does not exist!')
        else:
            print('Setup database: \n', setups_df)
            condition = (setups_df['wallet_id'] == wallet_id) & (setups_df['user_name'] == user_name)

            setup_to_close = setups_df[condition]
            print('Setup to close: \n', setup_to_close)

            index_list_to_close = list(setup_to_close.index)
            # print(index_list_to_close)

            if(len(index_list_to_close) != 0):
                
                # print(setup_to_close.loc[index_list_to_close[0], 'close_date'])

                if((pd.notna(setup_to_close.loc[index_list_to_close[0], 'close_date']))):
                    print('Setup already closed!')    
                else:            
                    for index in index_list_to_close:
                        setups_df.loc[index, 'close_date'] = close_date
                    
                    print('New setup: \n', setups_df)

                    setups_df.to_parquet(f'{self.full_desired_path}/wallets.parquet', index = True)
            else:
                print('Setup does not exist!')








#
##
###
# ATUALIZANDO A COMPOSIÇÃO DA CARTEIRA
###
##
#

# input = asset_dataframe

# Last wallet defined below:
#           data ticker  peso
# 0  2023-11-16  BRFS3   0.1
# 1  2023-11-16  CEAB3   0.1
# 2  2023-11-16  CSED3   0.1
# 3  2023-11-16  CSUD3   0.1
# 4  2023-11-16  MDNE3   0.2
# 5  2023-11-16  NINJ3   0.1
# 6  2023-11-16  SEER3   0.1
# 7  2023-11-16  TEND3   0.1
# 8  2023-11-16  VLID3   0.1

    def update_wallet_composion(self, wallet, update_date, asset_dataframe):

        self.wallet = wallet
        self.asset_dataframe = asset_dataframe

#
##
###
# LENDO A COMPOSIÇÃO DA CARTEIRA
###
##
#
    def read_wallet_composion(self, wallet):
        
        self.wallet = wallet







#
##
###
# GERANDO UMA TRANSAÇÃO
###
##
#
    def create_transaction(self, asset, operation_type, transaction_date, wallet):

        self.asset = asset
        self.wallet = wallet
        self.operation_type = operation_type
        self.transaction_date = transaction_date









if __name__ == "__main__":

    setup_dict =  {
                    'wallet-momentum': {
                        'indicadores': {
                            'momento_6_meses': {'caracteristica': 'decrescente'}
                            },
                        'peso': 0.2},
                    'wallet-mix': {
                        'indicadores': {
                            'ValorDeMercado': {'caracteristica': 'crescente'},
                            # 'EBIT_EV': {'caracteristica': 'decrescente'},
                            # 'momento_6_meses': {'caracteristica': 'decrescente'}
                            },
                        'peso': 0.8}
                    }

    wallet_manager = WalletManager()
    
    # wallet_manager.read_setups()

    # new_setup_to_insert = wallet_manager.preparing_setup_data(setups_dict = setup_dict, user_name = 'pacient-zero', create_date = '1892-10-23')
    new_setup_to_insert = wallet_manager.preparing_setup_data(setups_dict = setup_dict, user_name = 'tebinha', create_date = '1992-08-12')
    wallet_manager.insert_setup(new_setup = new_setup_to_insert)

    # wallet_manager.close_setup(wallet_id='first-shot', user_name='pacient-zero', close_date = '2023-11-22')
    # wallet_manager.close_setup(wallet_id='first-shot', user_name='tebinha', close_date = '2023-11-21')

    # wallet_manager.delete_setup(wallet_id='first-shot', user_name='error')
    # wallet_manager.delete_setup(wallet_id='first-shot', user_name='tebinha')
    # wallet_manager.delete_setup(wallet_id='first-shot', user_name='pacient-zero')