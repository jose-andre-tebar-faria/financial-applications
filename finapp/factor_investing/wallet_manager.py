import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from io import StringIO
from datetime import datetime

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
    # PREPARANDO DADOS
    ##
    #
    def preparing_setup_data(self, setups_dict, rebalance_periods, number_of_assets, user_name, create_date):
        
        self.setups_dict = setups_dict

        setups_dataframe = pd.DataFrame(columns=['wallet_id', 'wallet_name', 'number_of_assets', 'actual_wallet_total_number_of_assets', 'user_name', 'proportion', 'create_date', 'close_date', 'rebalance_periods', 'last_rebalance_date', 'indicator_1', 'indicator_2', 'indicator_3'])
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
    # LENDO SETUPS
    ##
    #
    def read_setups(self, username = None):

        file_not_found = False

        try:
            wallets_parquet = pd.read_parquet(f'{self.full_desired_path}/wallets.parquet')
            wallets_df = pd.DataFrame(wallets_parquet)
            if username != None:
                username = str(username)
                wallets_df = wallets_df[wallets_df['user_name'] == username]
            print('\nSetup configuration: \n', wallets_df)
        except:
            wallets_df = None
            file_not_found = True
            print("File not found.")

        return file_not_found, wallets_df
        
    #
    ##
    # VERIFICANDO EXISTÊNCIA DO SETUP NO DATABASE
    ##
    #
    def verify_setup_existence(self, wallet_manager, wallet_id):

        setup_existent = False
        self.wallet_id = str(wallet_id)

        file_not_found, setups_df = wallet_manager.read_setups()
        # print('Setup database: \n', setups_df)

        if(file_not_found):

            print('\t --- file wallets.parquet does not exists!')

        else:
            # print(self.wallet_id)
            # print(setups_df['wallet_id'])
            setup_existent = self.wallet_id in str(setups_df['wallet_id'])
            # print(setup_existent)

        return setup_existent

    #
    ##
    # INSERINDO SETUP NO DATABASE
    ##
    #
    def insert_setup(self, wallet_manager, new_setup):

        wallet_id_existent = None
        new_wallet_id = None
        wallet_existent = False
        esta_contido = False
    
        # print('New setup: \n', new_setup)

        file_not_found, setups_df = wallet_manager.read_setups()
        # print('Setup database: \n', setups_df)

        if(file_not_found):

            print('\t+++creating file wallets.parquet.')
            
            new_wallet_id = new_setup['wallet_id'].iloc[0]
            # print('new_wallet_id', new_wallet_id)

            # print('Setup updated: \n', new_setup)
            new_setup.to_parquet(f'{self.full_desired_path}/wallets.parquet', index = True)
        else:
            wallet_id_database_list = list(setups_df['wallet_id'])
            wallet_id_database_list = list(set(wallet_id_database_list))
            # print(wallet_id_database_list)

            for wallet_id_database in wallet_id_database_list:
                setup_to_verify = setups_df[setups_df['wallet_id'] == wallet_id_database]
                df_merge = pd.merge(setup_to_verify, new_setup, on=['wallet_name', 'proportion', 'rebalance_periods', 'user_name', 'indicator_1', 'indicator_2', 'indicator_3'], how='left', indicator=True)
                # print(df_merge)
                found_in_database = (df_merge['_merge'] == 'both').all()
                # print(found_in_database)
                if(found_in_database):
                    esta_contido = True
                    # wallet_id_existent = (setups_df[['wallet_id']][setups_df['wallet_name'] == df_merge['wallet_name']]).at[0,'wallet_id']
                    wallet_id_existent = setup_to_verify['wallet_id'].iloc[0]
                    # print('wallet_id_existent', wallet_id_existent)
                    
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

                new_wallet_id = setup_to_concat['wallet_id'].iloc[0]
                # print('new_wallet_id', new_wallet_id)

                updated_setup.to_parquet(f'{self.full_desired_path}/wallets.parquet', index = True)
        
        # print('wallet_id_existent', wallet_id_existent)
        # print('new_wallet_id', new_wallet_id)
        if(wallet_id_existent == None and new_wallet_id == None):
            print('\n ---no wallet defined or found!')
            wallet_existent = False
        else:
            wallet_existent = True
            if(wallet_id_existent == None):
                wallet_id = new_wallet_id
            else:
                wallet_id = wallet_id_existent
        # print('wallet_id', wallet_id)

        return wallet_id, wallet_existent
        # return wallet_id_existent, new_wallet_id

    #
    ##
    # APAGANDO SETUPS
    ##
    #
    def delete_setup(self, wallet_manager, wallet_id, user_name):

        setup_to_delete = pd.DataFrame()
        
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
                new_setup = setups_df.drop(setups_df[condition].index)
                print('New setup: \n', new_setup)
                
                new_setup.to_parquet(f'{self.full_desired_path}/wallets.parquet', index = True)

        return setup_to_delete

    #
    ##
    # FECHANDO SETUPS
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
    # LENDO AS COMPOSIÇÕES DAS CARTEIRAS
    ##
    #
    def read_portifolios_composition(self):

        file_not_found = False

        try:
            compositions_parquet = pd.read_parquet(f'{self.full_desired_path}/wallets_composition.parquet')
            compositions_df = pd.DataFrame(compositions_parquet)
            # print('\nWallet composition configuration: \n', compositions_df)
        except:
            compositions_df = None
            file_not_found = True

            if(file_not_found):

                print('\n\t+++creating file wallets_composition.parquet.')
                
                empty_composition = pd.DataFrame()

                empty_composition.to_parquet(f'{self.full_desired_path}/wallets_composition.parquet', index = True)
            
            print("\nFile not found.")

        return file_not_found, compositions_df

    #
    ##
    # VALIDANDO A COMPOSIÇÃO DA CARTEIRA
    ##
    #

    def validate_portifolio_composition(self, wallet_defined):
        
        validation_result = False

        print(wallet_defined)

        sum_of_proportions = self.wallet_defined['wallet_proportion'].astype(float).sum()

        if(sum_of_proportions >= 0.9999):
            validation_result = True
        else:
            print('\t---sum of wallet proportions is not 100%!\n')

        return validation_result

    #
    ##
    # ATUALIZANDO A COMPOSIÇÃO DA CARTEIRA
    ##
    #
    def update_portifolio_composition(self, wallet_manager, wallet_id, wallet_defined):

        self.wallet_id = wallet_id
        self.wallet_defined = wallet_defined
        self.wallet_manager = wallet_manager

        esta_contido = False

        file_not_found, compositions_df = self.wallet_manager.read_portifolios_composition()
        setup_existence = self.wallet_manager.verify_setup_existence(self.wallet_manager, self.wallet_id)
        validation_result = self.wallet_manager.validate_portifolio_composition(self.wallet_defined)

        if(file_not_found):

            if(validation_result and setup_existence):
                print('\n\t+++creating file wallets_composition.parquet.')
                
                self.wallet_defined['wallet_id'] = wallet_id
                self.wallet_defined['executed'] = False
                self.wallet_defined['execution_date'] = pd.NA
                self.wallet_defined['rebalance_date'] = pd.to_datetime(self.wallet_defined['rebalance_date'])

                print('\nFirst setup!')
                print('\nNew composition: \n', self.wallet_defined)
                self.wallet_defined.to_parquet(f'{self.full_desired_path}/wallets_composition.parquet', index = True)
            else:
                if(setup_existence == False):
                    print('Setup does not exist in database.\n')
                if(validation_result == False):
                    print('Wallet validation FAILED.\n')
        else:

            if(validation_result and setup_existence):
                # print(compositions_df)
                self.wallet_defined['wallet_id'] = self.wallet_id
                self.wallet_defined['executed'] = False
                self.wallet_defined['execution_date'] = pd.NA
                self.wallet_defined['rebalance_date'] = pd.to_datetime(self.wallet_defined['rebalance_date'])
                # print(self.wallet_defined)

                wallet_id_database_list = list(compositions_df['wallet_id'])
                wallet_id_database_list = list(set(wallet_id_database_list))
                # print(wallet_id_database_list)

                for wallet_id_database in wallet_id_database_list:
                    # print(compositions_df)
                    # print(wallet_id_database)
                    setup_to_verify = compositions_df[compositions_df['wallet_id'] == str(wallet_id_database)]
                    # print(setup_to_verify)
                    # print(self.wallet_defined)
                    df_merge = pd.merge(setup_to_verify, self.wallet_defined, on=['wallet_id', 'ticker', 'rebalance_date', 'executed', 'execution_date'], how='left', indicator=True)
                    # print(df_merge)
                    found_in_database = (df_merge['_merge'] == 'both').all()
                    # print(found_in_database)
                    if(found_in_database):
                        esta_contido = True
                        # wallet_id_existent = (setups_df[['wallet_id']][setups_df['wallet_name'] == df_merge['wallet_name']]).at[0,'wallet_id']
                        wallet_id_existent = setup_to_verify['wallet_id'].iloc[0]
                        print('\nwallet_id_existent: ', wallet_id_existent)

                if(esta_contido):
                    print('\nWallet composition duplicated!')
                    
                    print('\t--- nothing to do!')
                else:
                    print('New wallet composition!')
                    
                    max_composition_index = compositions_df.index.max()
                    # print('max_composition_index: ', max_composition_index)

                    if(np.isnan(max_composition_index)):
                        print('First setup!\n')
                    else:
                        self.wallet_defined.index = self.wallet_defined.index + max_composition_index + 1

                    print('Wallet composition to concat: \n', self.wallet_defined)

                    print('\t...updating file wallets_composition.parquet.')
                
                    updated_wallet_composition = pd.concat([compositions_df, self.wallet_defined], ignore_index=False)
                    print('\nNew composition: \n', updated_wallet_composition)

                    updated_wallet_composition.to_parquet(f'{self.full_desired_path}/wallets_composition.parquet', index = True)
            else:
                if(setup_existence == False):
                    print('\n ---setup does not exist in database.\n')
                if(validation_result == False):
                    print('Wallet validation FAILED.\n')


    #
    ##
    # APAGANDO SETUPS
    ##
    #
    def delete_portifolio_composition(self, wallet_id, rebalance_date):

        file_not_found, compositions_df = wallet_manager.read_portifolios_composition()
        # print('Setup database: \n', setups_df)

        if(file_not_found):
            print('\twallets.parquet does not exist!')
        else:
            condition = (compositions_df['wallet_id'] == wallet_id) & (compositions_df['rebalance_date'] == rebalance_date)
            setup_to_delete = compositions_df[condition]
            print('Setup to delete: \n', setup_to_delete)

            if(setup_to_delete.empty):
                print('Setup does not exist!')
            else:
                new_setup = compositions_df.drop(compositions_df[condition].index)
                print('New setup: \n', new_setup)
                
                new_setup.to_parquet(f'{self.full_desired_path}/wallets_composition.parquet', index = True)
    
    
    
    #
    ##
    # VERIFICANDO NECESSIDADE DE REBALANCEAMENTO
    ##
    #
    def verify_compositions_to_execute(self, wallet_manager, wallet_id = None):

        file_not_found, compositions_df = wallet_manager.read_portifolios_composition()

        if(file_not_found):

            print('\t --- file wallets_composition.parquet does not exists!')
            
        else:
            compostion_to_execute = compositions_df[compositions_df['executed'] == False]
            compostion_to_execute.sort_values(['rebalance_date', 'ticker'], inplace=True)
            print('Wallets composition not executed: \n', compostion_to_execute)

            return compostion_to_execute

    #
    ##
    # LENDO UM TIPO TRANSAÇÃO
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
    # GERANDO UM TIPO TRANSAÇÃO
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
                print('Operation type duplicated!')
                
                print('\t--- nothing to do!')
            else:
                print('New type transaction!')

                max_type_transaction_index = type_transaction_df.index.max()
                # print('max_type_transaction_index: ', max_type_transaction_index)

                if(np.isnan(max_type_transaction_index)):
                    print('First setup!\n')
                else:
                    operation_type_df.index = operation_type_df.index + max_type_transaction_index + 1

                print('Operation type to concat: \n', operation_type_df)

                print('\t...updating file type_transaction.parquet.')
            
                updated_transaction_type = pd.concat([type_transaction_df, operation_type_df], ignore_index=False)
                print('Setup updated: \n', updated_transaction_type)

                updated_transaction_type.to_parquet(f'{self.full_desired_path}/type_transaction.parquet', index = True)

    #
    ##
    # REMOVENDO UM TIPO TRANSAÇÃO
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
    # GERANDO UMA TRANSAÇÃO
    ##
    #
    def create_transaction(self, ticker, operation_type, transaction_date, wallet_id):

        self.ticker = ticker
        self.wallet_id = wallet_id
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

    # file_not_found, wallets_df = wallet_manager.read_setups()

    # print(wallets_df[['wallet_id', 'wallet_name', 'number_of_assets', 'user_name', 'proportion', 'close_date', 'rebalance_periods', 'last_rebalance_date']])

    # new_setup_to_insert = wallet_manager.preparing_setup_data(setups_dict = setup_dict, rebalance_periods = 2, user_name = 'pacient-zero', create_date = '1892-10-23')
    # new_setup_to_insert = wallet_manager.preparing_setup_data(setups_dict = setup_dict, rebalance_periods = rebalance_periods, number_of_assets = asset_quantity, user_name = user_name, create_date = create_date)
    # wallet_id, wallet_existent = wallet_manager.insert_setup(wallet_manager = wallet_manager, new_setup = new_setup_to_insert)

    # wallet_manager.close_setup(wallet_id='first-shot', user_name='pacient-zero', close_date = '2023-11-22')
    # wallet_manager.close_setup(wallet_id='first-shot', user_name='tebinha', close_date = '2023-11-21')

    # wallet_manager.delete_setup(wallet_manager = wallet_manager, wallet_id='first-shot', user_name='error')
    # wallet_manager.delete_setup(wallet_manager = wallet_manager, wallet_id='9178', user_name='andre-tebar')
    # wallet_manager.delete_setup(wallet_manager = wallet_manager, wallet_id='5380', user_name='tebinha')
    # wallet_manager.delete_setup(wallet_manager = wallet_manager, wallet_id='2504', user_name='jandretebarf')


    ##############
    # WALLET COMPOSITION CONFIGURATION
    ##############

    data0 = """rebalance_date,ticker,wallet_proportion
            2023-10-16,BRFS3,0.25
            2023-10-16,CEAB3,0.25
            2023-10-16,PETR4,0.25
            2023-10-16,WEGE3,0.25
            """
    data1 = """rebalance_date,ticker,wallet_proportion
            2023-11-16,NINJ3,0.33
            2023-11-16,TEND3,0.34
            2023-11-16,CSUD3,0.33
            """
    
    data2 = """rebalance_date,ticker,wallet_proportion
            2023-12-16,WEGE3,0.5
            2023-12-16,PETR4,0.5
            """
    
    # last_wallet_csv = pd.read_csv(StringIO(data2))
    # last_wallet_defined = pd.DataFrame(last_wallet_csv)
    # last_wallet_defined['rebalance_date'] = pd.to_datetime(last_wallet_defined['rebalance_date'])
    # last_wallet_defined['wallet_proportion'] = (last_wallet_defined['wallet_proportion']).astype(float)
    # print('last_wallet_defined: \n', last_wallet_defined)

    # if wallet_existent is False:
    #     print('\n ---no wallet defined or found! forcing save_wallet_composion to FALSE...\n')
    #     wallet_id = str(wallet_id)
    #     save_wallet_composion = False
    # print('wallet_id', wallet_id)

    # wallet_manager.read_portifolios_composition()
    # wallet_manager.update_portifolio_composition(wallet_manager = wallet_manager, wallet_id = wallet_id, wallet_defined = last_wallet_defined)
    # wallet_manager.delete_portifolio_composition(wallet_id = '4235', rebalance_date = '2023-11-20')

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

    # wallet_manager.read_type_transaction()
    # wallet_manager.create_type_transaction(operation_type = operation_type, operation_code = operation_code, operation_name = operation_name)
    # wallet_manager.delete_type_transaction(operation_code = operation_code)



    ##############
    # BUY/SELL MANAGER
    ##############


    # wallet_manager.verify_compositions_to_execute(wallet_manager=wallet_manager)