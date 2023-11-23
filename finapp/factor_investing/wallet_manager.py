import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from io import StringIO
from datetime import datetime

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
    def preparing_setup_data(self, setups_dict, rebalance_periods, number_of_assets, user_name, create_date):
        
        self.setups_dict = setups_dict

        setups_dataframe = pd.DataFrame(columns=['wallet_id', 'wallet_name', 'number_of_assets', 'actual_wallet_total_number_of_assets', 'user_name', 'proportion', 'create_date', 'close_date', 'rebalance_periods', 'last_rebalance_date'])
        setups_dataframe['create_date'] = pd.to_datetime(setups_dataframe['create_date'])
        setups_dataframe['close_date'] = pd.to_datetime(setups_dataframe['close_date'])
        setups_dataframe['last_rebalance_date'] = pd.to_datetime(setups_dataframe['last_rebalance_date'])
        
        wallet_id = np.random.randint(1,9999)
        wallet_id = str(wallet_id)
        # print(wallet_id)

        wallet_index = 0

        for wallet_name, wallet in setups_dict.items():

            indicador_index = 1

            setups_dataframe.loc[wallet_index, 'wallet_id'] = wallet_id
            setups_dataframe.loc[wallet_index, 'wallet_name'] = wallet_name
            setups_dataframe.loc[wallet_index, 'user_name'] = user_name
            setups_dataframe.loc[wallet_index, 'proportion'] = wallet['peso']
            setups_dataframe.loc[wallet_index, 'create_date'] = create_date
            setups_dataframe.loc[wallet_index, 'rebalance_periods'] = rebalance_periods
            setups_dataframe.loc[wallet_index, 'number_of_assets'] = number_of_assets

            indicadores = wallet['indicadores']
            
            for indicador, ordem in indicadores.items():

                setups_dataframe.loc[wallet_index, f'indicator_{indicador_index}'] = indicador
                indicador_index+=1

            wallet_index+=1

        print('Setup to use: \n', setups_dataframe)
            
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
            print('Setup configuration: \n', wallets_df)
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
    def insert_setup(self, wallet_manager, new_setup):
        
        print('New setup: \n', new_setup)

        file_not_found, setups_df = wallet_manager.read_setups()
        # print('Setup database: \n', setups_df)

        if(file_not_found):

            print('\t+++creating file wallets.parquet.')
            
            # print('Setup updated: \n', new_setup)
            new_setup.to_parquet(f'{self.full_desired_path}/wallets.parquet', index = True)
        else:
            
            df_merge = pd.merge(setups_df, new_setup, on=['wallet_name', 'proportion', 'rebalance_periods', 'user_name'], how='left', indicator=True)
            esta_contido = (df_merge['_merge'] == 'both').any()
            # print(esta_contido)

            if(esta_contido):
                print('Setup duplicated!')
                
                print('\t--- nothing to do!')
            else:
                print('New setup!')

                max_setup_index = setups_df.index.max()
                # print('max_setup_index: ', max_setup_index)


                setup_to_concat = new_setup.copy()
                if(np.isnan(max_setup_index)):
                    print('First setup!\n')
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
    def delete_setup(self, wallet_manager, wallet_id, user_name):

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
# LENDO AS COMPOSIÇÕES DAS CARTEIRAS
###
##
#
    def read_portifolios_composition(self):

        file_not_found = False

        try:
            compositions_parquet = pd.read_parquet(f'{self.full_desired_path}/wallets_composition.parquet')
            compositions_df = pd.DataFrame(compositions_parquet)
            print('\nWallet composition configuration: \n', compositions_df)
        except:
            compositions_df = None
            file_not_found = True
            print("\nFile not found.")

        return file_not_found, compositions_df

#
##
###
# ATUALIZANDO A COMPOSIÇÃO DA CARTEIRA
###
##
#

    def update_portifolio_composition(self, wallet_manager, wallet_id, wallet_defined):

        self.wallet_id = wallet_id
        self.wallet_defined = wallet_defined
        self.wallet_manager = wallet_manager

        file_not_found, compositions_df = self.wallet_manager.read_portifolios_composition()
        

        if(file_not_found):

            print('\t+++creating file wallets_composition.parquet.')
            
            compositions_df = pd.DataFrame(columns=['rebalance_date', 'ticker', 'wallet_proportion', 'wallet_id'])
            compositions_df['rebalance_date'] = pd.to_datetime(compositions_df['rebalance_date'])
            
            destin_columns = {'rebalance_date': 'rebalance_date', 'wallet_proportion': 'wallet_proportion', 'ticker': 'ticker'}

            for new_column, origin_column in destin_columns.items():
                compositions_df[new_column] = self.wallet_defined.loc[:, origin_column]
            
            compositions_df['wallet_id'] = self.wallet_id

            print('\nFirst setup!')
            print('\nNew composition: \n', compositions_df)
            compositions_df.to_parquet(f'{self.full_desired_path}/wallets_composition.parquet', index = True)
        else:
            # print(compositions_df)
            self.wallet_defined['wallet_id'] = self.wallet_id
            # print(self.wallet_defined)

            df_merge = pd.merge(compositions_df, self.wallet_defined, on=['ticker', 'wallet_id', 'rebalance_date'], how='left', indicator=True)
            esta_contido = (df_merge['_merge'] == 'both').any()
            # print(esta_contido)
            
            if(esta_contido):
                print('\nWallet composition duplicated!')
                
                print('\t--- nothing to do!')
            else:
                print('New wallet composition!')
                
                max_composition_index = compositions_df.index.max()
                # print('max_composition_index: ', max_composition_index)

                composition_to_concat = pd.DataFrame(columns=['rebalance_date', 'ticker', 'wallet_proportion', 'wallet_id'])
                composition_to_concat['rebalance_date'] = pd.to_datetime(composition_to_concat['rebalance_date'])
                
                destin_columns = {'rebalance_date': 'rebalance_date', 'wallet_proportion': 'wallet_proportion', 'ticker': 'ticker'}

                for new_column, origin_column in destin_columns.items():
                    composition_to_concat[new_column] = self.wallet_defined.loc[:, origin_column]

                composition_to_concat['wallet_id'] = self.wallet_id

                if(np.isnan(max_composition_index)):
                    print('First setup!\n')
                else:
                    composition_to_concat.index = composition_to_concat.index + max_composition_index + 1

                print('Wallet composition to concat: \n', composition_to_concat)

                print('\t...updating file wallets_composition.parquet.')
            
                updated_wallet_composition = pd.concat([compositions_df, composition_to_concat], ignore_index=False)
                print('\nNew composition: \n', updated_wallet_composition)

                updated_wallet_composition.to_parquet(f'{self.full_desired_path}/wallets_composition.parquet', index = True)






#
##
###
# LENDO UM TIPO TRANSAÇÃO
###
##
#
    def read_type_transaction(self, operation_type = None, operation_code = None, operation_name = None):
        
        file_not_found = False

        try:
            type_transaction_parquet = pd.read_parquet(f'{self.full_desired_path}/type_transaction.parquet')
            type_transaction_df = pd.DataFrame(type_transaction_parquet)
            print('Type transactions configuration: \n', type_transaction_df)
        except:
            type_transaction_df = None
            file_not_found = True
            print("File not found.")

        return file_not_found, type_transaction_df

#
##
###
# GERANDO UM TIPO TRANSAÇÃO
###
##
#
    def create_type_transaction(self, operation_type, operation_code, operation_name):

        file_not_found, type_transaction_df = wallet_manager.read_type_transaction()

        print('\t+++creating file type_transaction.parquet.')
        
        operation_type_df = pd.DataFrame(columns=['operation_type', 'operation_code', 'operation_name', 'create_date'])

        new_operation_type = {
                                'operation_type': operation_type, 'operation_code': operation_code, 
                                'operation_name': operation_name, 'create_date': datetime.now()
                                }
        
        operation_type_df = pd.concat([operation_type_df , pd.DataFrame([new_operation_type])], ignore_index=True)
        print('\nnew operation_type: \n', operation_type_df)

        if(file_not_found):
            print('First type_transaction setup!\n')
            print('\nSetup to update: \n', operation_type_df)
            operation_type_df.to_parquet(f'{self.full_desired_path}/type_transaction.parquet', index = True)
        else:
            df_merge = pd.merge(type_transaction_df, operation_type_df, on=['operation_type', 'operation_code', 'operation_name'], how='left', indicator=True)
            esta_contido = (df_merge['_merge'] == 'both').any()
            # print(esta_contido)
            
            if(esta_contido):
                print('Wallet composition duplicated!')
                
                print('\t--- nothing to do!')
            else:
                print('New wallet composition!')

                max_type_transaction_index = type_transaction_df.index.max()
                # print('max_type_transaction_index: ', max_type_transaction_index)

                if(np.isnan(max_type_transaction_index)):
                    print('First setup!\n')
                else:
                    operation_type_df.index = operation_type_df.index + max_type_transaction_index + 1

                print('Wallet composition to concat: \n', operation_type_df)

                print('\t...updating file type_transaction.parquet.')
            
                updated_transaction_type = pd.concat([type_transaction_df, operation_type_df], ignore_index=False)
                print('Setup updated: \n', updated_transaction_type)

                updated_transaction_type.to_parquet(f'{self.full_desired_path}/type_transaction.parquet', index = True)

#
##
###
# REMOVENDO UM TIPO TRANSAÇÃO
###
##
#
    def delete_type_transaction(self, operation_code):

        file_not_found, type_transaction_df = wallet_manager.read_type_transaction()

        if(file_not_found):
            print('\type_transaction.parquet does not exist!')
        else:
            condition = (type_transaction_df['operation_code'] == operation_code)
            type_transaction_to_delete = type_transaction_df[condition]
            print('Setup to delete: \n', type_transaction_to_delete)

            if(type_transaction_to_delete.empty):
                print('Setup does not exist!')
            else:
                # new_setup = setups_df.loc[(setups_df['wallet_id'] != wallet_id) & (setups_df['user_name'] != user_name)]
                new_setup = type_transaction_df.drop(type_transaction_df[condition].index)
                print('New setup: \n', new_setup)
                
                new_setup.to_parquet(f'{self.full_desired_path}/type_transaction.parquet', index = True)








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
                        'peso': 0.35},
                    'wallet-mix': {
                        'indicadores': {
                            'ValorDeMercado': {'caracteristica': 'crescente'},
                            # 'EBIT_EV': {'caracteristica': 'decrescente'},
                            # 'momento_6_meses': {'caracteristica': 'decrescente'}
                            },
                        'peso': 0.65}
                    }

    rebalance_periods = 42
    asset_quantity = 7

    user_name = 'tebinha'
    create_date = '1992-08-12'

    wallet_manager = WalletManager()
    
    ##############
    # SETUP CONFIGURATION
    ##############

    file_not_found, wallets_df = wallet_manager.read_setups()

    # print(wallets_df[['wallet_id', 'wallet_name', 'number_of_assets', 'user_name', 'proportion', 'close_date', 'rebalance_periods', 'last_rebalance_date']])

    # new_setup_to_insert = wallet_manager.preparing_setup_data(setups_dict = setup_dict, rebalance_periods = 2, user_name = 'pacient-zero', create_date = '1892-10-23')
    # new_setup_to_insert = wallet_manager.preparing_setup_data(setups_dict = setup_dict, rebalance_periods = rebalance_periods, number_of_assets = asset_quantity, user_name = user_name, create_date = create_date)
    # wallet_manager.insert_setup(wallet_manager = wallet_manager, new_setup = new_setup_to_insert)

    # wallet_manager.close_setup(wallet_id='first-shot', user_name='pacient-zero', close_date = '2023-11-22')
    # wallet_manager.close_setup(wallet_id='first-shot', user_name='tebinha', close_date = '2023-11-21')

    # wallet_manager.delete_setup(wallet_manager = wallet_manager, wallet_id='first-shot', user_name='error')
    # wallet_manager.delete_setup(wallet_manager = wallet_manager, wallet_id='9178', user_name='andre-tebar')
    # wallet_manager.delete_setup(wallet_manager = wallet_manager, wallet_id='5380', user_name='tebinha')
    # wallet_manager.delete_setup(wallet_manager = wallet_manager, wallet_id='5537', user_name='pacient-zero')





    ##############
    # WALLET COMPOSITION CONFIGURATION
    ##############

    data = """rebalance_date,ticker,wallet_proportion
            2023-11-16,BRFS3,0.1
            2023-11-16,CEAB3,0.1
            2023-11-16,CSED3,0.1
            2023-11-16,CSUD3,0.1
            2023-11-16,MDNE3,0.2
            2023-11-16,NINJ3,0.1
            2023-11-16,SEER3,0.1
            2023-11-16,TEND3,0.1
            2023-11-16,VLID3,0.1
            """
    
    data2 = """rebalance_date,ticker,wallet_proportion
            2023-11-16,WEGE3,0.5
            2023-11-16,PETR4,0.5
            """
    
    # last_wallet_csv = pd.read_csv(StringIO(data))
    # last_wallet_defined = pd.DataFrame(last_wallet_csv)
    # print('last_wallet_defined: \n', last_wallet_defined)

    wallet_id = '627'

    wallet_manager.read_portifolios_composition()
    # wallet_manager.update_portifolio_composition(wallet_manager = wallet_manager, wallet_id = wallet_id, wallet_defined = last_wallet_defined)





    ##############
    # OPERATION TYPES CONFIGURATION
    ##############

    # operation_type = 'credit'
    # operation_code = 'C-01'
    # operation_name = 'contribuiton'

    # operation_type = 'debit'
    # operation_code = 'R-01'
    # operation_name = 'redemption'

    # operation_type = 'credit'
    # operation_code = 'S-01'
    # operation_name = 'sell'

    # operation_type = 'debit'
    # operation_code = 'P-01'
    # operation_name = 'purchase'

    wallet_manager.read_type_transaction()
    # wallet_manager.create_type_transaction(operation_type = operation_type, operation_code = operation_code, operation_name = operation_name)
    # wallet_manager.delete_type_transaction(operation_code = operation_code)