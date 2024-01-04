import download_by_fintz as dbf
import download_by_api as dba
import download_by_webscrapping as dbw
import make_indicators as mi
import risk_premiuns as rp
import rate_risk_premiuns as rrp
import factor_calculator as fc
import market_premium as mp
import regression_model as rm
import update_asset_profile as uap
import create_bcg_matrix as cbm
import wallet_manager as wm

import os
from dotenv import load_dotenv
import pandas as pd
from itertools import combinations
import subprocess
import numpy as np
from dateutil.relativedelta  import relativedelta
from datetime import datetime
import time

class FinappController:

    def __init__(self):
                
        print("Inicializing FinappController!")
        
        load_dotenv()

    def calculate_combinations(self, premium_name, len_premium_name, single_combinations = False, double_combinations = False, triple_combinations = False):

        # self.premium_name = premium_name
        all_combinations = []
        self.list_combinations = []

        # self.triple_combinations = triple_combinations
        # self.double_combinations = double_combinations
        # self.single_combinations = single_combinations

        if(len_premium_name >= 3 and triple_combinations):
            all_combinations = list(combinations(premium_name, 3))

            for combination in all_combinations:
                self.list_combinations.append(combination)

        if(len_premium_name >= 2 and double_combinations):
            all_combinations = list(combinations(premium_name, 2))

            for combination in all_combinations:
                self.list_combinations.append(combination)
        
        if(len_premium_name >= 1 and single_combinations):
            all_combinations = list(combinations(premium_name, 1))

            for combination in all_combinations:
                self.list_combinations.append(combination)

        return self.list_combinations

    def create_file_names(self, list_combinations, indicators_dict):

        self.list_combination_file_name = []

        self.list_combinations = list_combinations
        self.indicators_dict = indicators_dict

        for combination in self.list_combinations:
            indicators_dict_new = {key: self.indicators_dict[key] for key in combination} 

            desired_value = 'file_name'
            self.premium_name = [file_name[desired_value] for file_name in indicators_dict_new.values()]
            self.premium_name = '-with-'.join(self.premium_name)

            self.list_combination_file_name.append(self.premium_name)

        return self.list_combination_file_name

    def reading_folder_files(self):

        parsed_premium_files_name = []

        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.databse_folder = os.getenv("PREMIUNS_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.databse_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

        full_files_name = [file for file in os.listdir(self.full_desired_path) if os.path.isfile(os.path.join(self.full_desired_path, file))]

        # print(full_files_name)

        for file_name in full_files_name:
            last_underscore_location = file_name.rfind("_")
            if last_underscore_location != -1:
                parsed_premium_files_name.append(file_name[:last_underscore_location])

        # parsed_premium_files_name.remove('market_premium.parquet')

        # print(parsed_premium_files_name)

        return parsed_premium_files_name

    def prepare_data_for_rate_premiuns_risks(self, indicators_dict, single_combinations, double_combinations, triple_combinations):
        
        finapp = FinappController()

        # single_combinations = bool(single_combinations)
        # double_combinations = bool(double_combinations)
        # triple_combinations = bool(triple_combinations)

        premium_name = indicators_dict.keys()
        premium_name = list(premium_name)
        # print(premium_name)
        len_premium_name = len(premium_name)
        # print(len_premium_name)

        list_combinations = finapp.calculate_combinations(premium_name, len_premium_name, single_combinations, double_combinations,
                                                          triple_combinations)
        print('\nlist_combinations: \n', list_combinations)

        print('Number of combinations: ', len(list_combinations))

        list_combination_file_name = finapp.create_file_names(list_combinations, indicators_dict)

        premium_name_dict = dict.fromkeys(list_combination_file_name, 1000000)
        
        print('.\n.\nPremium names dictionary: \n\t', premium_name_dict, '\n.\n.')

        return premium_name_dict

    def create_wallet_dict(self, indicators_dict, premiuns_statistics_to_show, premiuns_to_dict):
        
        # print(indicators_dict)

        indicators_comb_list = list(premiuns_statistics_to_show['premium_name'])
        print(f'\nindicators_comb_list: \n', indicators_comb_list)

        marker = '-with-'
        auto_wallet_dict = {}
        # number_of_wallets = len(best_indicators_list)
        number_of_wallets = len(premiuns_to_dict)
        wallet_proportion = 1/number_of_wallets
        print(f'\nwallet_proportion: \n', wallet_proportion)

        default_wallet = {
                        'wallet-1': {'indicadores': {}, 'peso': 1}, 
                        'wallet-2': {'indicadores': {}, 'peso': 1},
                        'wallet-3': {'indicadores': {}, 'peso': 1},
                        'wallet-4': {'indicadores': {}, 'peso': 1},
                        'wallet-5': {'indicadores': {}, 'peso': 1},
                        }

        wallet_number = 1
        existing_wallets_list = []
        
        print(f'\npremiuns_to_dict: \n', premiuns_to_dict)
        indicators_comb_list = [indicators_comb_list[position - 1] for position in premiuns_to_dict]
        print(f'\nindicators_comb_list: \n', indicators_comb_list)


        for indicators_comb in indicators_comb_list:
            split_indicator = indicators_comb.split(marker)
            # print(split_indicator)

            indicators_list = []

            for file_name in split_indicator:

                chave_encontrada = None

                for chave, subdicionario in indicators_dict.items():
                    if 'file_name' in subdicionario and subdicionario['file_name'] == file_name:
                        chave_encontrada = chave
                        indicators_list.append(chave)
                        break
            print(f'\nindicators_list for wallet-{wallet_number}: ', indicators_list)

            for file_name in indicators_list:
                # print(file_name)
                # print(indicators_dict)

                if file_name in indicators_dict:
                    
                    order_value = indicators_dict[file_name]['order']
                    # print(order_value)

                    wallet_name = 'wallet-' + str(wallet_number)
                    # print(wallet_name)
                    default_wallet[wallet_name]['indicadores'][file_name] = {'caracteristica': order_value}
                    default_wallet[wallet_name]['peso'] = wallet_proportion
                    # print(auto_wallet_dict)
                    # print('\nWallet dict to append: \n', default_wallet)

                auto_wallet_dict.update(default_wallet)
                # print('\nAutomatic wallet dict created: \n', auto_wallet_dict)

            existing_wallets_list.append(wallet_name)
            # print(existing_wallets_list)
            wallet_number+=1

        print('\nExisting wallets in dict created: ', existing_wallets_list)

        setup_dict = {wallet: auto_wallet_dict[wallet] for wallet in existing_wallets_list}
        # print('\nAutomatic wallet dict created: \n', setup_dict)

        return setup_dict

    def create_automatic_wallet(self, ranking_indicator, indicators_dict):
        
        # print(ranking_indicator)
        # print(indicators_dict)

        number_of_top_indicators = 2
        best_indicators_list = []

        best_indicators_list = list(ranking_indicator['nome_indicador'].head(number_of_top_indicators))
        print(f'\nOs {number_of_top_indicators} primeiros indicadores: \n', best_indicators_list)

        marker = '-with-'
        auto_wallet_dict = {}
        number_of_wallets = len(best_indicators_list)
        wallet_proportion = 1/number_of_wallets

        default_wallet = {
                        'wallet-1': {'indicadores': {}, 'peso': 1}, 
                        'wallet-2': {'indicadores': {}, 'peso': 1},
                        'wallet-3': {'indicadores': {}, 'peso': 1},
                        'wallet-4': {'indicadores': {}, 'peso': 1},
                        }

        wallet_number = 1
        existing_wallets_list = []
        
        for indicators_comb in best_indicators_list:
            split_indicator = indicators_comb.split(marker)
            # print(split_indicator)

            indicators_list = []

            for file_name in split_indicator:

                chave_encontrada = None

                for chave, subdicionario in indicators_dict.items():
                    if 'file_name' in subdicionario and subdicionario['file_name'] == file_name:
                        chave_encontrada = chave
                        indicators_list.append(chave)
                        break
            print(f'\nindicators_list for wallet-{wallet_number}: ', indicators_list)

            for file_name in indicators_list:
                # print(file_name)
                # print(indicators_dict)

                if file_name in indicators_dict:
                    
                    order_value = indicators_dict[file_name]['order']
                    # print(order_value)

                    wallet_name = 'wallet-' + str(wallet_number)
                    # print(wallet_name)
                    default_wallet[wallet_name]['indicadores'][file_name] = {'caracteristica': order_value}
                    default_wallet[wallet_name]['peso'] = wallet_proportion
                    # print(auto_wallet_dict)
                    # print('\nWallet dict to append: \n', default_wallet)

                auto_wallet_dict.update(default_wallet)
                # print('\nAutomatic wallet dict created: \n', auto_wallet_dict)

            existing_wallets_list.append(wallet_name)
            # print(existing_wallets_list)
            wallet_number+=1

        print('\nExisting wallets in dict created: ', existing_wallets_list)

        setup_dict = {wallet: auto_wallet_dict[wallet] for wallet in existing_wallets_list}
        # print('\nAutomatic wallet dict created: \n', setup_dict)

        return setup_dict

    def compose_last_wallet_with_bcg_matrix(self, last_wallet, bcg_dimensions_list):
        
        analysis_assets_list = last_wallet['ticker']
        print('\nWallet assets list: \n', analysis_assets_list)

        last_wallet['ticker'] = last_wallet['ticker'].str[:4]        
        last_wallet = last_wallet.rename(columns={'ticker': 'asset'})

        last_wallet = last_wallet.set_index('asset', drop=True)
        # last_wallet = last_wallet.drop(columns = 'index')
        # print(last_wallet)

        bcg_matrix_acess = cbm.BcgMatrix(bcg_dimensions_list)
        bcg_matrix = bcg_matrix_acess.read_bcg_matrix_database()

        bcg_matrix_df = pd.DataFrame(bcg_matrix)

        bcg_matrix_df = bcg_matrix_df.set_index('asset', drop=True)
        bcg_matrix_df = bcg_matrix_df.drop(columns = 'index')
        # print(bcg_matrix_df)
        
        final_analysis = pd.merge(bcg_matrix_df, last_wallet, on='asset')
        print('\nNightvision: \n', final_analysis.sort_values(by=['sector', 'subsector']))
        
        return analysis_assets_list, final_analysis

    def calculate_wallet_returns(self, analysis_assets_list, rebalance_date, next_rebalance_date):
        
        current_folder = os.getcwd()

        project_folder = os.getenv("PROJECT_FOLDER")
        databse_folder = os.getenv("DATABASE_FOLDER")
        full_desired_path = os.path.join(project_folder,databse_folder)

        if(current_folder != full_desired_path):
            os.chdir(full_desired_path)

        quotations_database_parquet = pd.read_parquet(f'{full_desired_path}/cotacoes.parquet')
        
        quotations_database = pd.DataFrame(quotations_database_parquet[['data', 'ticker', 'preco_fechamento_ajustado']][quotations_database_parquet['ticker'].isin(analysis_assets_list)])
        quotations_database['data'] = pd.to_datetime(quotations_database['data'])
        quotations_database.sort_values(['ticker', 'data'], inplace=True)

        last_quotation_date = quotations_database.loc[quotations_database.index[-1], 'data']
        last_quotation_date = pd.to_datetime(last_quotation_date)
        print('\nlast_quotation_date: ', last_quotation_date)

        rebalance_date = pd.to_datetime(rebalance_date)
        print('\nwallet rebalance_date: ', rebalance_date)

        next_rebalance_date = pd.to_datetime(next_rebalance_date)
        print('\nwallet next_rebalance_date: ', next_rebalance_date)

        if last_quotation_date < next_rebalance_date:
            next_rebalance_date = last_quotation_date
        print('\nwallet next_rebalance_date after: ', next_rebalance_date)

        periods_since_rebalance = quotations_database[(quotations_database['data'] >= rebalance_date) & (quotations_database['data'] <= next_rebalance_date)]
        
        ## CAPTURAR PREÇOS
        print('\nperiods_since_rebalance: \n', periods_since_rebalance)
        assets_prices = periods_since_rebalance.groupby('ticker')['preco_fechamento_ajustado'].agg(['first', 'last']).reset_index()
        assets_prices.columns = ['ticker', 'initial_price', 'max_update_price']
        print('\nassets_prices: \n', assets_prices)

        periods_since_rebalance = periods_since_rebalance.groupby('ticker').count()
        print('\nperiods_since_rebalance: ', periods_since_rebalance)
        periods_since_rebalance = int(periods_since_rebalance.iloc[0,0])
        periods_since_rebalance = periods_since_rebalance - 1
        print('\nperiods_since_rebalance: ', periods_since_rebalance)

        assets_prices['percentual_variation'] = ((assets_prices['max_update_price'] - assets_prices['initial_price']) / assets_prices['initial_price']) * 100
        print('\nassets_prices: \n', assets_prices)

        last_period_variation = assets_prices

        print('\nNumber of assets in final wallet: ', len(analysis_assets_list))

        last_period_variation = pd.DataFrame(last_period_variation)
        
        print('\nlast_period_variation: \n', last_period_variation)
    
        last_period_variation = last_period_variation.reset_index(drop=False)
        # last_period_variation.rename(columns={'ticker': 'asset'}, inplace=True)
        # last_period_variation['asset'] = last_period_variation['asset'].str[:-1]
        
        return next_rebalance_date, last_period_variation, periods_since_rebalance

    def create_factor_file_names(self, setup_dict):
        
        pdf_name = ''

        print("Setup configuration =")

        for nome_carteira, carteira in setup_dict.items():
                
                print("\n\t", nome_carteira, '\n\t\t peso: ', carteira['peso'] * 100, '%')

                pdf_name = pdf_name + nome_carteira + "_peso" + str(carteira['peso']).replace(".", "") + "_" 

                indicadores = carteira['indicadores']

                print("\t\t indicator(s): ")
                
                for indicador, ordem in indicadores.items():

                    print('\t\t\t', indicador)

                    pdf_name = pdf_name + indicador + "_"

        print('\n\tAssets per wallet: ', asset_quantity)
        print('\n\tRebalance periods: ', rebalance_periods)

        pdf_name = pdf_name + str(rebalance_periods) + '_' + str(liquidity_filter) + "M_" + str(asset_quantity) + "A.pdf"

        return pdf_name
    
    def create_report_file_name(self, setup_dict, wallet_id, asset_quantity, rebalance_periods, liquidity_filter, username_existent):
        
        pdf_name = ''
        description_pdf = ''

        print("Setup configuration =")

        for nome_carteira, carteira in setup_dict.items():
                
                print("\n\t", nome_carteira, '\n\t\t peso: ', carteira['peso'] * 100, '%')

                description_pdf = description_pdf + nome_carteira + "_peso" + str(carteira['peso']).replace(".", "") + "_" 

                indicadores = carteira['indicadores']

                print("\t\t indicator(s): ")
                
                for indicador, ordem in indicadores.items():

                    print('\t\t\t', indicador)

                    description_pdf = description_pdf + indicador + "_"

        print('\n\tAssets per wallet: ', asset_quantity)
        print('\n\tRebalance periods: ', rebalance_periods)

        description_pdf = description_pdf + str(rebalance_periods) + '_' + str(liquidity_filter) + "M_" + str(asset_quantity) + "A"

        pdf_name = 'report-' + 'walet_id' + str(wallet_id) + '-' + str(username_existent) + '.pdf' 

        return pdf_name, description_pdf

    def create_setup_dict(self, rebalance_wallet_id, indicators_dict_database):
        
        wallet_manager = wm.WalletManager()

        setup_dict = {}
        rebalance_periods_setup = 0
        asset_quantity_setup = 0
        #
        ## READING SETUP
        #
        file_not_found, setup_df = wallet_manager.read_setups()
        print(f'\nsetup database: \n', setup_df)

        setup = setup_df[setup_df['wallet_id'] == str(rebalance_wallet_id)]
        print(f'\nsetup {rebalance_wallet_id}: \n', setup)


        if setup.empty:
            print('\n\t --- inexistent.')
        
            return setup_dict, rebalance_periods_setup, asset_quantity_setup
        else:
            print('\n\t +++ found.')

            #
            ## CAPTURING REBALANCE PERIODS AND NUMBER OF ASSETS PER WALLET
            #
            rebalance_periods_setup = int(setup['rebalance_periods'].iloc[0])
            print('\nrebalance_periods_setup: ', rebalance_periods_setup)
            asset_quantity_setup = int(setup['number_of_assets'].iloc[0])
            print('\nasset_quantity_setup: ', asset_quantity_setup)

            #
            ## CREATE DICT PONDERATED WALLET
            #
            dataframe_columns = ['wallet_name', 'number_of_assets', 'proportion', 'indicator_1', 'indicator_2', 'indicator_3']
            setup_dict_df = pd.DataFrame(columns=dataframe_columns)
            
            setup_to_dict_df = setup[dataframe_columns]
            print('\nsetup_to_dict_df: \n', setup_to_dict_df)

            setup_dict = {}

            for index, row in setup_to_dict_df.iterrows():
                wallet_name = row['wallet_name']
                indicators_dict = {}

                for indicator_col in ['indicator_1', 'indicator_2', 'indicator_3']:
                    indicator_name = row[indicator_col]
                    
                    if indicator_name is not None and indicator_name in indicators_dict_database:
                        indicators_dict[indicator_name] = {'caracteristica': indicators_dict_database[indicator_name]['order']}

                setup_dict[wallet_name] = {'indicadores': indicators_dict, 'peso': row['proportion']}

            print('\nsetup_dict: \n', setup_dict)

        return setup_dict, rebalance_periods_setup, asset_quantity_setup
     
    def sliding_window(self, start_date, end_date, step_months):

        current_date = pd.to_datetime(end_date)
        start_date = pd.to_datetime(start_date)
        months_window_size = pd.DateOffset(months=step_months)
        if step_months > 6:
            months_offset = 3
        else:
            months_offset = 2


        while current_date > start_date:
            window_end = current_date
            window_start = current_date - months_window_size

            # Verifica se a data da primeira janela ultrapassa o start_date
            if window_start < start_date:
                window_start = start_date

            yield window_start, window_end

            # current_date -= pd.DateOffset(months=step_months/2)
            current_date -= pd.DateOffset(months=months_offset)

    def find_next_rebalance_date(self, compositions_df, wallet_id, rebalance_date):

        # compositions_df['wallet_id'] = compositions_df['wallet_id'].astype(int)

        # Filtrar o DataFrame para a carteira específica
        # wallet_df = compositions_df[compositions_df['wallet_id'] == int(wallet_id)]
        
        # Ordenar o DataFrame pela coluna 'rebalance_date'
        compositions_df = compositions_df.sort_values('rebalance_date')
        
        # Obter a última rebalance_date fornecida como input ou a data atual
        if rebalance_date is None:
            last_rebalance_date = datetime.now().date()
        else:
            last_rebalance_date = pd.to_datetime(rebalance_date).date()
        
        # Filtrar as datas maiores que a última rebalance_date
        next_rebalance_dates = compositions_df[compositions_df['rebalance_date'] > pd.to_datetime(last_rebalance_date)]['rebalance_date']
        
        # Se houver datas futuras, pegue a primeira, senão, retorne None
        if not next_rebalance_dates.empty:
            next_rebalance_date = next_rebalance_dates.iloc[0].date()
            return next_rebalance_date
        else:
            next_rebalance_date = datetime.now()
            next_rebalance_date = next_rebalance_date.strftime('%Y-%m-%d')
            return next_rebalance_date



###########################EXECUTORS#######################################

    def run_update_database(self, update_fintz_database = None, update_api_database = None, update_webscrapping_database = None, 
                            fintz_indicators_list = None, fintz_demonstration_list = None, initial_date = None,
                            bc_dict = None):

        print(".\n..\n...\nUpdating Database!\n...\n..\n.")

        if(update_fintz_database == None):
            update_fintz_database = False
        
        if(update_api_database == None):
            update_api_database = False
            
        if(update_webscrapping_database == None):
            update_webscrapping_database = False

        if(initial_date == None):
            initial_date = "2000-01-01"

        if(update_fintz_database):

            data_from_fintz = dbf.FintzData()

            for demonstration in fintz_demonstration_list:
                data_from_fintz.download_accounting_files(demonstration=True, data_name = demonstration)

            for indicator in fintz_indicators_list:
                data_from_fintz.download_accounting_files(indicator=True, data_name = indicator)

            data_from_fintz.download_cdi(initial_date=initial_date)
            data_from_fintz.download_ibov(initial_date=initial_date)
            data_from_fintz.download_quotations()
        
        if(update_api_database):

            data_from_api = dba.DownloadByApi()

            bc_data = data_from_api.getting_bc_data(bc_dict)

        if(update_webscrapping_database):

            data_from_webscrapping = dbw.DownloadByWebscrapping()

            b3_sectors = data_from_webscrapping.getting_b3_assets_sector_by_site()

        if(update_fintz_database == False and update_api_database == False and update_webscrapping_database == False):
            print(".\n.\n=== NOTHING TO DO! ===")
        else:
            print(".\n.\n=== UPDATE COMPLETE! ===")

    def run_calculate_risk_premiuns(self, indicators_dict, single_combinations, double_combinations, triple_combinations, update_existing_file):

        finapp = FinappController()
        
        premium_dataframe = pd.DataFrame()

        print(".\n..\n...\nCalculating Risk Premiuns!\n...\n..\n.")
        beta = mp.MarketPremium()

        print('\nindicators_dict: ' , indicators_dict)

        beta.calculate_market_premium()

        premium_name = indicators_dict.keys()
        len_premium_name = len(premium_name)

        list_combinations = finapp.calculate_combinations(premium_name, len_premium_name, single_combinations, double_combinations, triple_combinations)

        if(len(list_combinations) > 0):
            
            print('.\n.\nNumber of combinations: ', len(list_combinations), '\n.\n.')

            # print(list_combinations)
            print(indicators_dict)
            list_combination_file_name = finapp.create_file_names(list_combinations, indicators_dict)

            folder_files = finapp.reading_folder_files()

            combination_step = 1

            for combination, premium_name in zip(list_combinations, list_combination_file_name):

                indicators_dict_new = {key: indicators_dict[key] for key in combination} 

                print('<\nStep: ', combination_step)
                print('Premium dictionary: \n\t', indicators_dict_new)
                print('\tpremium_name: ' , premium_name)

                if((premium_name not in folder_files) or update_existing_file):

                    premium = rp.RiskPremium(indicators_dict_new, premium_name, liquidity = 1000000)
                    
                    print("Preparing Data....")
                    premium.getting_quotations()
                    premium.getting_possible_dates()
                    premium.filtering_volume()
                    premium.getting_indicators()
                    premium.discovering_initial_month()
                    print("OK.")
                    premium_dataframe = premium.calculating_premiuns()
                    # print(premium_dataframe)
                    # print(premium_name)

                    premium.saving_premiuns()
                    print("Premium saved.\n>")
                else:
                    print('[SKIP] Premium already in the database!')
                combination_step+=1
        else:
            print("Nothing to do.")
        
        print(".\n.\n=== CALCULATIONS COMPLETE! ===")

        return list_combinations, premium_dataframe

    def run_rate_risk_premius(self, indicators_dict, final_analysis_date, rating_premiuns_file_name, number_of_top_comb_indicators, 
                              single_combinations, double_combinations, triple_combinations, create_rating_pdf):
        
        print(".\n..\n...\nRating Risk Premiuns!\n...\n..\n.")
        
        fail_to_execute = False

        dataframe_columns = ['ranking_single_indicators', 'contagem', 'nome_indicador']
        distribution_indicadors = pd.DataFrame(columns = dataframe_columns)
        
        dataframe_columns = ['acum_primeiro_quartil', 'acum_segundo_quartil', 'acum_terceiro_quartil', 'acum_quarto_quartil', 'nome_indicador', 'ranking_indicators']
        ranking_indicator = pd.DataFrame(columns=dataframe_columns)

        top_indicators = pd.DataFrame()

        finapp = FinappController()

        indicators_dict = dict(indicators_dict)
        print('\nindicators_dict: \n', indicators_dict)

        single_combinations = bool(single_combinations)
        double_combinations = bool(double_combinations)
        triple_combinations = bool(triple_combinations)

        premium_name_dict = finapp.prepare_data_for_rate_premiuns_risks(indicators_dict, single_combinations, double_combinations, triple_combinations)
        # print('.\n.\npremium_name_dict: \n', premium_name_dict)

        rating_premiuns = rrp.MakeResultsPremium(final_analysis_date = final_analysis_date, factors_dict = premium_name_dict, file_name = rating_premiuns_file_name)
        
        file_not_found, premios_de_risco = rating_premiuns.getting_premiuns()
        # print('.\n.\npremios_de_risco: \n', premios_de_risco)
        print('.\n.\npremios_de_risco: \n', premios_de_risco[premios_de_risco['nome_premio'] == 'MOMENTO_MM_7_40-with-P_VP_INVERT'])
        
        if file_not_found == False:
            dataframe_columns = ['acum_primeiro_quartil', 'acum_segundo_quartil', 'acum_terceiro_quartil', 'acum_quarto_quartil', 'nome_indicador', 'ranking_indicators']
            ranking_indicator = pd.DataFrame(columns=dataframe_columns)

            ranking_indicator = rating_premiuns.retorno_quartis()
            # print('.\n.\nranking_indicator: \n', ranking_indicator[['ranking_indicators', 'nome_indicador', 'acum_primeiro_quartil']])
            print('.\n.\nranking_indicator: \n', ranking_indicator)

            list_premium_name = {especitif_key: valor['file_name'] for especitif_key, valor in indicators_dict.items() if 'file_name' in valor}
            list_premium_name = list(list_premium_name.values())

            top_indicators = ranking_indicator.head(number_of_top_comb_indicators)

            for premium_to_match in list_premium_name:

                for indicator in top_indicators['nome_indicador']:

                    top_indicators[premium_to_match+'_Contido'] = top_indicators['nome_indicador'].apply(lambda x: premium_to_match in x)

            top_indicators['Pure'] = top_indicators['nome_indicador'].isin(list_premium_name)

            print('.\n.\ntop_indicators', number_of_top_comb_indicators, 'combinated: \n', top_indicators[['ranking_indicators', 'nome_indicador', 'acum_primeiro_quartil']])


            dataframe_columns = ['ranking_single_indicators', 'contagem', 'nome_indicador']
            distribution_indicadors = pd.DataFrame(columns = dataframe_columns)

            distribution_indicadors['nome_indicador'] = list_premium_name
            distribution_indicadors['contagem'] = 0

            distribution_indicadors = pd.merge(distribution_indicadors, ranking_indicator, on = 'nome_indicador', how = 'left')
            distribution_indicadors = distribution_indicadors.drop(columns=['acum_segundo_quartil', 'acum_terceiro_quartil', 'acum_quarto_quartil',  'ranking_indicators'])
            # print(distribution_indicadors)

            for i, indicator in enumerate(distribution_indicadors['nome_indicador']):
                indicator_presence = top_indicators[indicator+'_Contido'].sum()
                distribution_indicadors.loc[i, 'contagem'] = indicator_presence

            distribution_indicadors = distribution_indicadors.sort_values(by=['contagem','acum_primeiro_quartil'], ascending = [False, False])

            distribution_indicadors['ranking_single_indicators'] = distribution_indicadors['contagem'].rank(ascending=False)
            
            print('.\n.\ndistribution_indicadors: \n', distribution_indicadors)

            #
            ##
            # CREATING PDF
            ##
            #
            if(create_rating_pdf):
                list_premiuns_to_pdf = list(top_indicators['nome_indicador'])
                rating_premiuns.create_pdf_images(list_premiuns_to_pdf)
                rating_premiuns.fazer_pdf(list_premiuns_to_pdf)

            return distribution_indicadors, ranking_indicator, top_indicators, fail_to_execute
        else:
            fail_to_execute = True
            print('fail')
            return distribution_indicadors, ranking_indicator, top_indicators, fail_to_execute

    def run_rank_risk_premiuns(self, indicators_dict, final_analysis_date, rating_premiuns_file_name, 
                              single_combinations, double_combinations, triple_combinations, create_rating_pdf,
                              step_months_rank_list, columns_rank_list,
                              premiuns_to_dict, premiuns_to_show):
        
        print(".\n..\n...\nRanking Risk Premiuns!\n...\n..\n.")
        
        # finapp = FinappController()

        fail_to_execute = False

        factor_calc_initial_date    = '2012-01-31'
        factor_calc_end_date        = '2023-12-31'
        
        all_variables_present           = False
        all_selected_premiuns_present   = False
        enable_to_create_dict           = False

        include_max_window              = False

        step_months_list = step_months_rank_list
        
        setup_dict = {}
        
        columns_rank_database_list = ['profit_perc', 'anual_mean_acum_returns', 'anual_high_acum_returns', 'anual_low_acum_returns']

        if step_months_rank_list is None or step_months_list is None or columns_rank_list is None:
            all_variables_present = False
            print('\nall_variables_present: \n', all_variables_present)
        else:
            all_variables_present = True
            # print('\nall_variables_present: \n', all_variables_present)

        if columns_rank_list != None:
            all_variables_present = all(elem in columns_rank_database_list for elem in columns_rank_list)
            # print('\nall_variables_present: \n', all_variables_present)

        if step_months_rank_list != None:
            existent_in_analysis = all(isinstance(elemento, int) for elemento in step_months_rank_list)
            # print('\nexistent_in_analysis: \n', existent_in_analysis)
        else:
            existent_in_analysis = False
            print('\nexistent_in_analysis: \n', existent_in_analysis)

        if premiuns_to_show == None or premiuns_to_show > 15:
            #caso não sejá passado quantidade de premios para exibir ou for muito grande, força os 5 primeiros
            premiuns_to_show = 5
            enable_to_create_dict = False
        else:
            enable_to_create_dict = True
            
        if premiuns_to_dict != None:
            all_selected_premiuns_present = all(premiuns_to_show >= elemento for elemento in premiuns_to_dict)
            # print('\nall_selected_premiuns_present: \n', all_selected_premiuns_present)

            if len(premiuns_to_dict) > 5:
                enable_to_create_dict = False
        else:
            all_selected_premiuns_present = False
            print('\nall_selected_premiuns_present: \n', all_selected_premiuns_present)

        # condições de execução
        if existent_in_analysis and (len(step_months_rank_list) > 0) and all_variables_present:

            finapp = FinappController()

            dataframe_columns = ['premium_name', 'liquidity', 'months_window_size', 'analyzed_windows', 'profit_perc', 'mean_acum_returns' , 'anual_mean_acum_returns', 'anual_high_acum_returns', 'anual_low_acum_returns']
            premiuns_statistics = pd.DataFrame(columns=dataframe_columns)

            print(".\n..\n...\nExtracting Statistics from Risk Premiuns!\n...\n..\n.")

            indicators_dict = dict(indicators_dict)
            print('\nindicators_dict: \n', indicators_dict)

            single_combinations = bool(single_combinations)
            double_combinations = bool(double_combinations)
            triple_combinations = bool(triple_combinations)
            
            premium_name_dict = finapp.prepare_data_for_rate_premiuns_risks(indicators_dict, single_combinations, double_combinations, triple_combinations)
            print('.\n.\npremium_name_dict: \n', premium_name_dict)

            rating_premiuns = rrp.MakeResultsPremium(final_analysis_date = factor_calc_end_date, factors_dict = premium_name_dict, file_name = rating_premiuns_file_name)

            file_not_found, premios_de_risco = rating_premiuns.getting_premiuns()
            # print('.\n.\npremios_de_risco: \n', premios_de_risco)

            premios_de_risco['data'] = pd.to_datetime(premios_de_risco['data'])

            index = 0

            number_of_executions = 0

            profit_count = 0
            loss_count = 0

            if include_max_window:

                initial_date = pd.to_datetime(factor_calc_initial_date)
                end_date = pd.to_datetime(factor_calc_end_date)

                max_months = (end_date.year - initial_date.year) * 12 + (end_date.month - initial_date.month)
                max_months = int(max_months)
                max_months+=1
                # print('\nmax_months: \n', max_months)

                if max_months not in step_months_list:

                    step_months_list.append(max_months)
                    # print('\nstep_months_list: \n', step_months_list)

            days_in_window = None

            for chave, valor in premium_name_dict.items():

                # print('\nchave: \n', chave)
                

                for step_months in step_months_list:

                    # print('\nstep_month: ', step_months)

                    ## INSERIR AQUI A VALIDAÇÃO DAS CHAVES E CÁLCULO DE RENTABILIDADE DA ÚLTIMA JANELA DE step_months
                    
                    profit_count = 0
                    loss_count = 0

                    window_size_threshold = (step_months*30) * (11 / 12)
                    # print('\nwindow_size_threshold: ', window_size_threshold)

                    mean_acum_returns = 0
                    acum_primeiro_quartil_list = []

                    high_acum_returns = 0
                    low_acum_returns = 0

                    analyzed_windows = 0

                    for window_start, window_end  in finapp.sliding_window(start_date=factor_calc_initial_date, end_date=factor_calc_end_date, step_months=step_months):
                        
                        window_start = pd.to_datetime(window_start)
                        window_end = pd.to_datetime(window_end)

                        days_in_window = (window_end - window_start).days
                        days_in_window = float(days_in_window)

                        if days_in_window > window_size_threshold:

                            # print(f"\nWindow: {window_start} to {window_end}")
                            # print('\ndays_in_window: ', days_in_window)

                            recorte_premios_de_risco = premios_de_risco[premios_de_risco['data'] >= window_start]
                            recorte_premios_de_risco = recorte_premios_de_risco[recorte_premios_de_risco['data'] <= window_end]
                            # print('\nrecorte_premios_de_risco: \n', recorte_premios_de_risco)

                            fator = recorte_premios_de_risco[(recorte_premios_de_risco['nome_premio'] == chave) &
                                                                (recorte_premios_de_risco['liquidez'] == valor)]
                            # print('\nfator: \n', fator)
                            # print('\nfator[nome_premio]: \n', fator[fator['nome_premio'] == 'MOMENTO_MM_7_40-with-P_VP_INVERT'])

                            acum_primeiro_quartil = (fator['primeiro_quartil'].cumprod() - 1).iloc[-1]
                            # print('\nacum_primeiro_quartil: \n', acum_primeiro_quartil)

                            acum_primeiro_quartil = float(acum_primeiro_quartil)
                            acum_primeiro_quartil_list.append(acum_primeiro_quartil)
                            # print('\nacum_primeiro_quartil_list: \n', acum_primeiro_quartil_list)
                            
                            if acum_primeiro_quartil > 0:
                                profit_count+=1
                            else:
                                loss_count+=1
                            
                            analyzed_windows+=1
                            number_of_executions+=1
                    
                    if len(acum_primeiro_quartil_list) > 0:
                        mean_acum_returns = sum(acum_primeiro_quartil_list) / len(acum_primeiro_quartil_list)
                        # print('\nmean_acum_returns: \n', mean_acum_returns)

                        anual_mean_acum_returns = ((1 + mean_acum_returns) ** (12 / step_months)) - 1
                        # print('\nanual_mean_acum_returns: \n', anual_mean_acum_returns)

                        high_acum_returns = max(acum_primeiro_quartil_list)
                        anual_high_acum_returns = ((1 + high_acum_returns) ** (12 / step_months)) - 1

                        low_acum_returns = min(acum_primeiro_quartil_list)
                        anual_low_acum_returns = ((1 + low_acum_returns) ** (12 / step_months)) - 1

                        total_count = profit_count + loss_count
                        # print('\ntotal_count: \n', total_count)

                        profit_perc = (profit_count / total_count ) * 100
                        # print('\nprofit_perc: \n', profit_perc)

                        premiuns_statistics.loc[index, 'premium_name'] = chave
                        premiuns_statistics.loc[index, 'liquidity'] = valor
                        premiuns_statistics.loc[index, 'months_window_size'] = step_months
                        premiuns_statistics.loc[index, 'analyzed_windows'] = analyzed_windows
                        premiuns_statistics.loc[index, 'profit_perc'] = profit_perc
                        premiuns_statistics.loc[index, 'mean_acum_returns'] = mean_acum_returns
                        premiuns_statistics.loc[index, 'anual_mean_acum_returns'] = anual_mean_acum_returns
                        premiuns_statistics.loc[index, 'anual_high_acum_returns'] = anual_high_acum_returns
                        premiuns_statistics.loc[index, 'anual_low_acum_returns'] = anual_low_acum_returns

                        premiuns_statistics = premiuns_statistics.sort_values('anual_mean_acum_returns', ascending = False)

                        index+=1

            print('\npremiuns_statistics: \n', premiuns_statistics)
            analyzed_windows_df = pd.DataFrame(columns=['months_window_size','analyzed_windows'])
            premiuns_statistics = premiuns_statistics.sort_values('months_window_size', ascending = True)
            analyzed_windows_df = premiuns_statistics.loc[:, ['months_window_size','analyzed_windows']].copy()
            print('\nanalyzed_windows: \n', analyzed_windows)

            premiuns_statistics = premiuns_statistics.sort_values('anual_mean_acum_returns', ascending = False)
            # print('\npremiuns_statistics: \n', premiuns_statistics)

            number_of_combinations = index / len(step_months_list)
            number_of_combinations = int(number_of_combinations)
            # print('\nnumber_of_combinations: \n', number_of_combinations)

            number_of_analysed_windows = number_of_executions / number_of_combinations
            number_of_analysed_windows = int(number_of_analysed_windows)
            # print('\nnumber_of_analysed_windows: \n', number_of_analysed_windows)

            # print('\nnumber_of_executions: \n', number_of_executions)

            columns_to_pivot = ['analyzed_windows', 'profit_perc', 'anual_mean_acum_returns', 'anual_high_acum_returns', 'anual_low_acum_returns']

            final_statistics = premiuns_statistics.pivot(index='premium_name', columns='months_window_size', values=columns_to_pivot)
            final_statistics.reset_index(inplace=True)
            final_statistics.columns = ['premium_name'] + [f'{col}_{level}_months' for col, level in final_statistics.columns[1:]]

            statistics_columns_name = premiuns_statistics.columns.tolist()
            remove_columns = ['premium_name', 'mean_acum_returns', 'liquidity', 'months_window_size']
            statistics_columns_name = [x for x in statistics_columns_name if x not in remove_columns]

            # Prefixo e sufixo desejados
            prefix = '_'
            sufix = '_months'

            # Adicionar prefixo e sufixo a cada elemento da lista
            columns_sufix_list = [prefix + str(item) + sufix for item in step_months_list]

            # print('\npremiuns_statistics: \n', premiuns_statistics)
            # print('\nfinal_statistics: \n', final_statistics)
            # print('\nstatistics_columns_name: \n', statistics_columns_name)
            # print('\nstep_months_list: \n', columns_sufix_list)

            #
            ##
            ### RANKING
            ##
            #
            columns_rank_sufix_list = [element for element in columns_sufix_list if any(str(step_month) in element for step_month in step_months_rank_list)]
            # print('\ncolumns_rank_sufix_list: \n', columns_rank_sufix_list)

            print(".\n..\n...\nRanking Risk Premiuns!\n...\n..\n.")

            columns_to_rank = [item + sufix for item in columns_rank_list for sufix in columns_rank_sufix_list]
            print('\ncolumns_to_rank: \n', columns_to_rank)

            ranking_premiuns_statistics = final_statistics[columns_to_rank].rank(ascending=False, method='min')

            ranking_premiuns_statistics.columns = ['rank_' + coluna for coluna in columns_to_rank]
            ranking_premiuns_statistics['rank_final'] = ranking_premiuns_statistics.sum(axis=1).rank(ascending=True, method='min')
            # print('\nranking_premiuns_statistics: \n', ranking_premiuns_statistics)

            premiuns_statistics = pd.concat([final_statistics, ranking_premiuns_statistics], axis=1)
            premiuns_statistics = premiuns_statistics.sort_values('rank_final', ascending = True)
            # print('\npremiuns_statistics: \n', premiuns_statistics)

            columns_to_show = ['premium_name'] + columns_to_rank + ['rank_final']

            # Filtrar colunas com base nos elementos desejados
            premiuns_statistics_to_show = premiuns_statistics.filter(items=columns_to_show)
            
            #
            #OPTIONAL
            best_indicators_list = []
            best_indicators_list = list(premiuns_statistics_to_show['premium_name'].head(premiuns_to_show))
            print(f'\nOs {premiuns_to_show} primeiros indicadores são: \n', best_indicators_list)

            ##
            # CREATE AUTOMATIC PONDERATED WALLET
            ##
            # todos os premius indicados para ir ao dicionário de carteiras devem estar dentro dos premios a serem exibidos
            if enable_to_create_dict and all_selected_premiuns_present:
                print('entrou')
                setup_dict = finapp.create_wallet_dict(indicators_dict, premiuns_statistics_to_show, premiuns_to_dict)
                # print('\nsetup_dict: \n', setup_dict)
            else:
                print('\n\n\t---- não satisfez condições para criação do setup_dict.')

            ##### OUTPUTS #####

            print('\npremiuns_statistics_to_show: \n', premiuns_statistics_to_show)
            print('\nnumber_of_analysed_windows: \n', number_of_analysed_windows)

            ##### OUTPUTS #####

        return premiuns_statistics_to_show, analyzed_windows_df, setup_dict, fail_to_execute

    def run_factor_calculator(self, setup_dict, factor_calc_end_date, factor_calc_initial_date, asset_quantity, rebalance_periods, liquidity_filter, create_wallets_pfd, pdf_name):

        print(".\n..\n...\nGenerating Wallet(s)!\n...\n..\n.")

        #before initialize class must define the name of the file
        # pdf_name = ''
        if create_wallets_pfd:
            # pdf_name = finapp.create_factor_file_names(setup_dict)
            print('pdf_name: '), pdf_name
        
        rebalance_periods = int(rebalance_periods)

        backtest = fc.MakeBacktest(data_final = factor_calc_end_date, data_inicial = factor_calc_initial_date, 
                                   filtro_liquidez=(liquidity_filter * 1000000), balanceamento = rebalance_periods, 
                                   numero_ativos = asset_quantity, corretagem = 0.01, nome_arquivo = pdf_name, **setup_dict)

        print('\n +++ pegando_dados')
        backtest.pegando_dados()
        print('\n +++ filtrando_datas')
        backtest.filtrando_datas()
        print('\n +++ criando_carteiras')
        backtest.criando_carteiras()
        print('\n +++ calculando_retorno_diario')
        wallets, returns = backtest.calculando_retorno_diario()

        print('\nlast 30 wallet days: \n',returns.tail(30))
        # print('wallets: \n',wallets)
        # print(returns)

        #
        ##
        # CREATE PDF REPORT
        ##
        #
        if(create_wallets_pfd):
            backtest.make_report()

        return wallets, returns

    def run_nightvision_wallet(self, compositions_df, wallet_id, rebalance_date):
        
        final_analysis = pd.DataFrame()
        last_analysis_date = None
        weighted_average_returns = None

        bcg_dimensions_list = [
                    'sector', 
                    'subsector',
                ]
        
        finapp = FinappController()





        next_rebalance_date = finapp.find_next_rebalance_date(compositions_df, wallet_id, rebalance_date)
        print('next_rebalance_date: \n', next_rebalance_date)
        print('rebalance_date: \n', rebalance_date)

        nightvision_wallet = compositions_df[compositions_df['rebalance_date'] == rebalance_date]
        
        nightvision_wallet = nightvision_wallet[['rebalance_date','ticker','wallet_proportion']]
        nightvision_wallet.rename(columns={'rebalance_date': 'data', 'wallet_proportion': 'peso'}, inplace=True)
        nightvision_wallet = nightvision_wallet.set_index('data', drop=True)
        nightvision_wallet = nightvision_wallet.reset_index()
        print('\nnightvision_wallet: \n', nightvision_wallet)

        # compositions_df = compositions_df[['rebalance_date','ticker','wallet_proportion']]
        # compositions_df.rename(columns={'rebalance_date': 'data', 'wallet_proportion': 'peso'}, inplace=True)
        # compositions_df = compositions_df.set_index('data', drop=True)
        # print('compositions_df: \n', compositions_df)


        if nightvision_wallet.empty:
            return final_analysis, last_analysis_date, weighted_average_returns
        else:








            # last_wallet = compositions_df.loc[compositions_df.index[0]]
            # last_wallet = last_wallet.reset_index()
            # print('\nLast wallet defined below: \n', last_wallet)
            
            # last_wallet_rebalance_date = last_wallet.loc[last_wallet.index[-1], 'data']
            # last_wallet_rebalance_date = pd.to_datetime(last_wallet_rebalance_date)
            # print('\nLast wallet rebalance_date: ', last_wallet_rebalance_date)

            #
            ## une a matrix BCG (bcg_matrix) aos últimos resultados da carteira
            #
            # analysis_assets_list, final_analysis = finapp.compose_last_wallet_with_bcg_matrix(last_wallet, bcg_dimensions_list)
            analysis_assets_list, final_analysis = finapp.compose_last_wallet_with_bcg_matrix(nightvision_wallet, bcg_dimensions_list)

            final_analysis = final_analysis.reset_index(drop=False)
            
            #
            ## calcula o rendimento de cada ativo e médio desde o último rebalanciamento da carteira
            #
            # last_analysis_date, last_period_variation, periods_since_rebalance = finapp.calculate_wallet_returns(analysis_assets_list, last_wallet_rebalance_date)
            next_rebalance_date, last_period_variation, periods_since_rebalance = finapp.calculate_wallet_returns(analysis_assets_list, rebalance_date, next_rebalance_date)

            print('\n\nlast_period_variation: \n',last_period_variation)

            # last_period_variation.rename(columns={'ticker': 'asset'}, inplace=True)
            last_period_variation['asset'] = last_period_variation['ticker'].str[:-1]
            print('\n\nlast_period_variation: \n',last_period_variation)

            final_analysis = pd.merge(final_analysis, last_period_variation, on='asset')
            print('\n\nfinal_analysis: \n',final_analysis)
            
            print(final_analysis.columns)
            
            weighted_average_returns = (final_analysis['percentual_variation'] * final_analysis['peso']).sum() / final_analysis['peso'].sum()
            print(f'\nweighted_average wallet rentability past {periods_since_rebalance} periods: ', round(weighted_average_returns,2) , '%')

            print(".\n.\n=== GENERATION COMPLETE! ===")

            return final_analysis, next_rebalance_date, weighted_average_returns

    def run_rebalance_setups(self, rebalance_wallet_id, rebalance_calc_end_date, indicators_dict_database, factor_calc_initial_date, liquidity_filter):

        finapp = FinappController()

        create_wallets_pfd = False
        pdf_name = 'testtttt.pdf'

        wallet_to_database = pd.DataFrame()
        rebalance_wallet_id = rebalance_wallet_id
        indicators_dict_database = indicators_dict_database
        rebalance_calc_end_date = rebalance_calc_end_date

        setup_dict, rebalance_periods_setup, asset_quantity_setup = finapp.create_setup_dict(rebalance_wallet_id, indicators_dict_database)
        rebalance_periods_setup = int(rebalance_periods_setup)
        # print('rebalance_periods_setup: ', rebalance_periods_setup)

        wallet_manager = wm.WalletManager()

        if len(setup_dict) == 0:
            return wallet_to_database
        else:
            #
            ## CALCULATE BACKTEST TO VERIFY REBALANCE POSSIBILITY
            #
            wallets, returns = finapp.run_factor_calculator(setup_dict, 
                                                            factor_calc_end_date=rebalance_calc_end_date, factor_calc_initial_date=factor_calc_initial_date, 
                                                            asset_quantity=asset_quantity_setup, rebalance_periods=rebalance_periods_setup, liquidity_filter=liquidity_filter,
                                                            create_wallets_pfd=create_wallets_pfd, pdf_name=pdf_name)
            # print('wallets: \n', wallets)
            #
            ## FINDING LAST WALLET
            #
            last_calculated_wallet = wallets.loc[wallets.index[-1]]
            last_calculated_wallet = last_calculated_wallet.reset_index()
            last_calculated_wallet.rename(columns={'data': 'rebalance_date', 'peso': 'wallet_proportion'}, inplace=True)
            last_calculated_wallet['rebalance_date'] = pd.to_datetime(last_calculated_wallet['rebalance_date'])
            last_calculated_wallet['ticker'] = last_calculated_wallet['ticker'].astype(str)
            last_calculated_wallet['wallet_proportion'] = last_calculated_wallet['wallet_proportion'].astype(float)
            print('\nCalculated wallet defined below: \n', last_calculated_wallet)
            
            last_calculated_rebalance_date = last_calculated_wallet.loc[last_calculated_wallet.index[-1], 'rebalance_date']
            last_calculated_rebalance_date = pd.to_datetime(last_calculated_rebalance_date)
            print('\ncalculation_rebalance_date: ', last_calculated_rebalance_date)

            #
            ## READING WALLET COMPOSITION DATABASE
            #
            file_not_found, compositions_df = wallet_manager.read_portifolios_composition()

            if(file_not_found == False):
            
                wallet_composition = compositions_df[compositions_df['wallet_id'] == str(rebalance_wallet_id)]
                print(f'\ncomposition of wallet_id {rebalance_wallet_id}: \n', wallet_composition)
                
                #verificar se o df está vazio
                if wallet_composition.empty:
                    print('\nnew composition!')

                    wallet_to_database = last_calculated_wallet

                    print('\nWallet to database: \n', wallet_to_database)

                    wallet_manager.update_portifolio_composition(wallet_manager = wallet_manager, wallet_id = rebalance_wallet_id, wallet_defined = wallet_to_database)

                else:
                    last_rebalance_date = wallet_composition.loc[wallet_composition.index[-1], 'rebalance_date']
                    last_rebalance_date = pd.to_datetime(last_rebalance_date)
                    print('\nlast_rebalance_date: ', last_rebalance_date)

                    last_wallet_composition =  wallet_composition[wallet_composition['rebalance_date'] == last_rebalance_date]
                    # print('\nlast_wallet_composition: \n', last_wallet_composition)
                    last_wallet_composition_to_compare = last_wallet_composition[['rebalance_date', 'ticker', 'wallet_proportion']]
                    last_wallet_composition_to_compare = last_wallet_composition_to_compare.reset_index(drop=True)
                    last_wallet_composition_to_compare['rebalance_date'] = pd.to_datetime(last_wallet_composition_to_compare['rebalance_date'])
                    last_wallet_composition_to_compare['ticker'] = last_wallet_composition_to_compare['ticker'].astype(str)
                    last_wallet_composition_to_compare['wallet_proportion'] = last_wallet_composition_to_compare['wallet_proportion'].astype(float)
                    print('\nwallet_composition_to_compare: \n', last_wallet_composition_to_compare)
                    
                    wallet_to_database = last_wallet_composition_to_compare

                    #
                    ## COMPARE DATES AND WALLET COMPOSITION (CALCULATED with LAST DATABASE COMPOSITION)
                    #
                    are_equal = last_wallet_composition_to_compare.equals(last_calculated_wallet)

                    if(are_equal):
                        print('\nequals!')
                    else:
                        print('\ndiff!')

                    if(last_rebalance_date == last_calculated_rebalance_date):
                        print('\nup-to-date!')
                        wallet_to_database = last_calculated_wallet
                    else:
                        print('\nneed to update composition!')

                        wallet_to_database = last_calculated_wallet

                        print('\nWallet to database: \n', wallet_to_database)

                        # wallet_manager.update_portifolio_composition(wallet_manager = wallet_manager, wallet_id = rebalance_wallet_id, wallet_defined = wallet_to_database)
                        
                        print('\nUPDATED!')

                    if((last_rebalance_date == last_calculated_rebalance_date) and are_equal):
                        print('\nboth!')
            else:
                wallet_to_database = last_calculated_wallet

                print('\nWallet to database: \n', wallet_to_database)

                # wallet_manager.update_portifolio_composition(wallet_manager = wallet_manager, wallet_id = rebalance_wallet_id, wallet_defined = wallet_to_database)
                
            return wallet_to_database

    def run_optimize_setup(self, rebalance_wallet_id, indicators_dict_database):
        
        fail_to_execute = False

        rebalance_periods_list      = [21,42,126]
        asset_quantity_list         = [3,7]
        step_months_list            = [12,36,60]
        # step_months_list            = [60]

        factor_calc_initial_date    = '2012-12-31'
        factor_calc_end_date        = '2023-12-06'

        finapp = FinappController()

        setup_dict, rebalance_periods_setup, asset_quantity_setup = finapp.create_setup_dict(rebalance_wallet_id, indicators_dict_database)
        wallet_manager = wm.WalletManager()

        if len(setup_dict) == 0:
            fail_to_execute = True
            return fail_to_execute
        else:
            for step_months in step_months_list:

                print('\nstep_month: ', step_months)

                for window_start, window_end  in finapp.sliding_window(start_date=factor_calc_initial_date, end_date=factor_calc_end_date, step_months=step_months):
                    # window_end = window_start + pd.DateOffset(months=step_months)
                    print(f"Window: {window_start} to {window_end}")

                    window_start_str = window_start.strftime('%Y-%m-%d')
                    window_end_str = window_end.strftime('%Y-%m-%d')
                    # print(window_start_str)
                    # print(window_end_str)

                    # wallets, returns = finapp.run_factor_calculator(setup_dict, 
                    #                                                 window_end_str, window_start_str, 
                    #                                                 asset_quantity, rebalance_periods, liquidity_filter, 
                    #                                                 create_wallets_pfd)
                    # print(returns)

            fail_to_execute = False
            return fail_to_execute

    def run_make_indicators(self):

        print(".\n..\n...\nUpdating Indicators!\n...\n..\n.")

        indicator = mi.MakeIndicator()

        indicator.making_momentum(months = 1)
        indicator.making_momentum(months = 6)
        indicator.making_momentum(months = 12)
        indicator.ratio_moving_mean(mm_curta = 7, mm_longa = 40)
        indicator.median_volume(months = 1)
        indicator.beta(years = 1)
        indicator.volatility(years = 1)
        indicator.pl_divida_bruta()
        indicator.ebit_divida_liquida()
        
        peg_ratio = indicator.peg_ratio()
        # print('last 15 peg_ratios: \n', peg_ratio.tail(15)) #[[peg_ratio['ticker'] == 'WEGE3']]

        p_vp = indicator.p_vp()
        # print(p_vp.tail(20))

        p_ebit = indicator.p_ebit()
        # print(p_ebit.tail(20))

        net_margin = indicator.net_margin()
        # print(net_margin.tail(20))

        print(".\n.\n=== UPDATE COMPLETE! ===")

    def run_execute_rebalance(self, wallet_id, rebalance_date):
        
        wallet_manager = wm.WalletManager()

        current_folder = os.getcwd()
        
        orders = pd.DataFrame()
        
        project_folder = os.getenv("PROJECT_FOLDER")
        databse_folder = os.getenv("DATABASE_FOLDER")
        full_desired_path = os.path.join(project_folder,databse_folder)

        if(current_folder != full_desired_path):
            os.chdir(full_desired_path)

        quotations_database_parquet = pd.read_parquet(f'{full_desired_path}/cotacoes.parquet')
        
        quotations_database = pd.DataFrame(quotations_database_parquet)
        quotations_database['data'] = pd.to_datetime(quotations_database['data'])
        quotations_database.sort_values(['ticker', 'data'], inplace=True)
        # print('quotations_database: \n',quotations_database)
        
        file_not_found, compositions_df = wallet_manager.read_portifolios_composition(wallet_id)

        compositions_df['rebalance_date'] = pd.to_datetime(compositions_df['rebalance_date'])
        
        # Filtrar o DataFrame pela wallet_id e a data passada
        df_filtrado = compositions_df[(compositions_df['wallet_id'] == str(wallet_id)) & (compositions_df['rebalance_date'] == pd.to_datetime(rebalance_date))]

        # Verificar se há registros para a data passada
        if df_filtrado.empty:
            print(f"\nNenhum registro encontrado para a wallet_id {wallet_id} na data {rebalance_date}.")
            return

        # Obter a última data existente no banco para a wallet_id antes da data passada
        ultima_data_antes_passada = compositions_df[(compositions_df['wallet_id'] == str(wallet_id)) & (compositions_df['rebalance_date'] < pd.to_datetime(rebalance_date))]['rebalance_date'].max()

        if pd.isnull(ultima_data_antes_passada):
            # Se não houver data anterior, considerar que a variação é toda a quantidade da data passada
            df_resultado = df_filtrado[['wallet_id', 'rebalance_date', 'ticker', 'wallet_proportion']].copy()
            # print(df_resultado)
            df_resultado['perc_variation'] = 100.0  # Variação é 100% quando não há data anterior
            df_resultado['wallet_proportion_actual'] = df_resultado['wallet_proportion']
            df_resultado['wallet_proportion_previous'] = 0
        else:
            # Filtrar o DataFrame para incluir apenas as linhas correspondentes à última data antes da data passada
            df_ultima_data_antes_passada = compositions_df[(compositions_df['wallet_id'] == str(wallet_id)) & (compositions_df['rebalance_date'] == ultima_data_antes_passada)]

            # Usar o método merge para obter as proporções para a data passada e a última data antes da data passada
            df_merge = pd.merge(df_filtrado, df_ultima_data_antes_passada, on=['ticker'], how='outer', suffixes=('_actual', '_previous'))

            # Preencher valores nulos com 0
            df_merge = df_merge.fillna(0)
            print('df_merge: \n',df_merge)
            
            rebalance_date_previous = pd.to_datetime(df_merge['rebalance_date_previous']).head(1).iloc[0]
            rebalance_date_actual = pd.to_datetime(df_merge['rebalance_date_actual']).head(1).iloc[0]
            
            analysis_assets_list = list(df_merge['ticker'])
            
            print('rebalance_date_previous: ',rebalance_date_previous)
            print('rebalance_date_actual: ',rebalance_date_actual)
            print('quotations_database: \n',quotations_database[['ticker', 'data','preco_fechamento_ajustado']])
            
            df_prices = pd.DataFrame()
            df_previous = pd.DataFrame()
            df_actual = pd.DataFrame()
            quotations_database = pd.DataFrame(quotations_database_parquet[['data', 'ticker', 'preco_fechamento_ajustado']][quotations_database_parquet['ticker'].isin(analysis_assets_list)])
            # print('quotations_database: \n',quotations_database)

            # Crie DataFrames para D1
            d1_data = {'ticker': analysis_assets_list}
            d1_df = pd.DataFrame(d1_data)

            # Converta a coluna 'data' para datetime
            quotations_database['data'] = pd.to_datetime(quotations_database['data'])

            # Filtrar D2 para as datas desejadas
            d2_filtered = quotations_database[quotations_database['data'].isin([rebalance_date_actual, rebalance_date_previous])]

            # Junte os DataFrames D1 e D2 com base no ticker
            final_df = pd.merge(d1_df, d2_filtered, on='ticker', how='left', suffixes=('_actual', '_previous'))
            
            tickers = final_df['ticker'].unique()
            dates = final_df['data'].unique()
            
            # result_df = pd.DataFrame(columns=['ticker', 'date_1', 'price_date_1', 'date_2', 'price_date_2'])

            # Criar um DataFrame vazio
            result_data = []

            # Loop pelos tickers
            for ticker in tickers:
                # Obter os preços para o ticker específico
                ticker_data = quotations_database[quotations_database['ticker'] == ticker]
                
                # Criar um dicionário para armazenar as informações
                info_dict = {'ticker': ticker}
                
                # Loop pelas datas
                for date in dates:
                    # Obter o preço para a data específica
                    price = ticker_data[ticker_data['data'] == date]['preco_fechamento_ajustado'].values
                    
                    # Adicionar as informações ao dicionário
                    info_dict[f'date_{dates.tolist().index(date) + 1}'] = date
                    info_dict[f'price_date_{dates.tolist().index(date) + 1}'] = price[0] if len(price) > 0 else None

                # Adicionar o dicionário à lista
                result_data.append(info_dict)
            
            result_df = pd.DataFrame(result_data)
            
            # Exibir o DataFrame final
            # print('result_df: \n', result_df)

            result_df = pd.merge(df_merge, result_df, on='ticker', how='left')
            # print('result_df: \n', result_df)

            # Selecionar as colunas necessárias
            result_df = result_df[['wallet_id_actual', 'rebalance_date_actual', 'ticker', 'wallet_proportion_actual', 'price_date_1', 'wallet_proportion_previous', 'price_date_2']].drop_duplicates()
            # print('result_df: \n', result_df)




        




            # result_df['relative_proportion_previous'] = result_df['wallet_proportion_previous'] * result_df['price_date_2']
            # result_df['relative_proportion_actual'] = result_df['wallet_proportion_actual'] * result_df['price_date_1']
            # print('result_df: \n', result_df)

            # sum_relative_proportion_previous = result_df['relative_proportion_previous'].sum()
            # sum_relative_proportion_actual = result_df['relative_proportion_actual'].sum()

            # print('sum_relative_proportion_previous:', sum_relative_proportion_previous)
            # print('sum_relative_proportion_actual:', sum_relative_proportion_actual)

            # result_df['unbalanced_proportion'] = result_df['relative_proportion_actual'] / result_df['price_date_2']

            # result_df['diff_proportion'] = result_df['unbalanced_proportion'] - result_df['wallet_proportion_previous']
            # print('result_df: \n', result_df)

            # sum_unbalanced_proportion = result_df['unbalanced_proportion'].sum()
            # sum_diff_proportion = result_df['diff_proportion'].sum()

            # print('sum_unbalanced_proportion:', sum_unbalanced_proportion)
            # print('sum_diff_proportion:', sum_diff_proportion)








            # Calcular a variação percentual para cada ticker
            df_merge['perc_variation'] = ((df_merge['wallet_proportion_actual'] - df_merge['wallet_proportion_previous']) / df_merge['wallet_proportion_previous']).replace([np.inf, -np.inf], 1) * 100

            # Selecionar as colunas necessárias
            df_resultado = df_merge[['wallet_id_actual', 'rebalance_date_actual', 'ticker', 'perc_variation', 'wallet_proportion_actual', 'wallet_proportion_previous']].drop_duplicates()
            print('df_resultado: \n',df_resultado)

        analysis_assets_list = list(df_resultado['ticker'][df_resultado['perc_variation'] < 0])
        # print('analysis_assets_list: \n',analysis_assets_list)
        
        quotations_database = pd.DataFrame(quotations_database_parquet[['data', 'ticker', 'preco_fechamento_ajustado']][quotations_database_parquet['ticker'].isin(analysis_assets_list)])
        
        orders = df_resultado[['ticker', 'perc_variation', 'wallet_proportion_actual', 'wallet_proportion_previous']][df_resultado['perc_variation'] != 0]
        print('orders: \n',orders)
       
        previous_asset_price = 0
        rebalance_asset_price = 0
        orders['perc_returns'] = 0
        
        # for asset in analysis_assets_list:
        for index, row in orders.iterrows():

            if row['perc_variation'] < 0:
                asset = row['ticker']
                print(asset)
                print('asset: ', asset)
                
                rebalance_date = pd.to_datetime(rebalance_date)
                print('rebalance_date: ', rebalance_date)

                try:
                    rebalance_asset_price = quotations_database['preco_fechamento_ajustado'][(quotations_database['data'] == rebalance_date) & (quotations_database['ticker'] == asset)].iloc[0]
                except:
                    rebalance_asset_price = 0
                    print(f'\t---price not found for ticker {asset} at {rebalance_date}')

                print('rebalance_asset_price: ',rebalance_asset_price)

                # Filtrar o DataFrame para incluir apenas as linhas antes da data de saída
                df_anterior = compositions_df[compositions_df['rebalance_date'] < rebalance_date]

                # Verificar quais ativos estavam presentes na composição anterior à data de saída
                ativos_anteriores = df_anterior[df_anterior['ticker'] == asset]

                # Se houver registros, a primeira data em que o ativo entrou será o valor mínimo de 'rebalance_date'
                if not ativos_anteriores.empty:
                    previous_rebalance_date = ativos_anteriores['rebalance_date'].min()
                    previous_rebalance_date = previous_rebalance_date.strftime('%Y-%m-%d')
                    orders.at[index, 'previous_rebalance_date'] = previous_rebalance_date
                    print('previous_rebalance_date: ', previous_rebalance_date)
                    # print(f'O ativo {asset} entrou na composição em: {previous_rebalance_date}')

                previous_asset_price = quotations_database['preco_fechamento_ajustado'][(quotations_database['data'] == pd.to_datetime(previous_rebalance_date)) & (quotations_database['ticker'] == str(asset))].iloc[0]
                
                # previous_asset_price = quotations_database['preco_fechamento_ajustado'][quotations_database['data'] == previous_rebalance_date]

                print('previous_asset_price: ', previous_asset_price)

                orders.at[index, 'rebalance_asset_price'] = rebalance_asset_price
                orders.at[index, 'previous_asset_price'] = previous_asset_price

                if previous_asset_price == 0 or rebalance_asset_price == 0:
                    print('\t---perc_return not calculated!')
                else:
                    perc_returns = round(((rebalance_asset_price - previous_asset_price) / rebalance_asset_price) * 100,1)
                    perc_returns = float(perc_returns)
                    print('perc_returns: ', perc_returns)
                    orders.at[index, 'perc_returns'] = perc_returns
            else:
                orders.at[index, 'rebalance_asset_price'] = 0
                orders.at[index, 'previous_asset_price'] = 0
                orders.at[index, 'previous_rebalance_date'] = 0

        orders = orders.sort_values(by='perc_variation', ascending=True)

        return orders

    def run_report_setups(self, wallet_id, factor_calc_end_date, indicators_dict_database, factor_calc_initial_date, liquidity_filter, create_wallets_pfd, username_existent):

        finapp = FinappController()

        wallet_to_database = pd.DataFrame()
        wallet_id = wallet_id
        indicators_dict_database = indicators_dict_database
        factor_calc_end_date = factor_calc_end_date

        setup_dict, rebalance_periods_setup, asset_quantity_setup = finapp.create_setup_dict(wallet_id, indicators_dict_database)
        rebalance_periods_setup = int(rebalance_periods_setup)
        asset_quantity_setup = int(asset_quantity_setup)
        print('\nasset_quantity_setup: ', asset_quantity_setup)
        print('\nrebalance_periods_setup: ', rebalance_periods_setup)

        if len(setup_dict) == 0:
            return wallet_to_database
        else:
            #
            ## CALCULATE BACKTEST TO VERIFY REBALANCE POSSIBILITY
            #
            
            pdf_name, description_pdf = finapp.create_report_file_name(setup_dict, wallet_id, 
                                                                       asset_quantity_setup, rebalance_periods_setup, liquidity_filter,
                                                                       username_existent)
            # print('pdf_name: ', pdf_name)
            # print('description_pdf: ', description_pdf)

            wallets, returns = finapp.run_factor_calculator(setup_dict, 
                                                            factor_calc_end_date=factor_calc_end_date, factor_calc_initial_date=factor_calc_initial_date, 
                                                            asset_quantity=asset_quantity_setup, rebalance_periods=rebalance_periods_setup, liquidity_filter=liquidity_filter,
                                                            create_wallets_pfd=create_wallets_pfd, pdf_name=pdf_name)
        
        return pdf_name

###########################EXECUTORS#######################################

if __name__ == "__main__":

    init_time_execution = time.time()

    finapp = FinappController()

    # enable database update
    update_database                 = False
    update_api_database             = False
    update_fintz_database           = False
    update_webscrapping_database    = False


    # enable asset profile update
    update_asset_profile            = False


    # enable create BCG Matrix
    update_bcg_matrix               = False


    # enable indicators update
    update_indicators               = False


    # enable calculate risk premiuns database update
    calculate_risk_premiuns         = False
    # choose de indicators combinations to rate
    single_combinations             = True
    double_combinations             = True
    triple_combinations             = True
    # true if you want to update a existing file
    update_existing_file            = False


    # enable rating risks
    rate_risk_premiuns              = False
    # final_analysis_date             = '2022-12-31'
    final_analysis_date             = '2024-12-31'
    rating_premiuns_file_name       = r'..\\PDFs\rating-BEST_INDICATORS.pdf'
    create_rating_pdf               = False
    
    
    # enable run a regression model
    execute_regression_model        = False


    # enable configure setup database
    config_setups                   = False
    number_of_top_indicators        = 2
    read_setup                      = False
    save_setup                      = False
    close_setup                     = False
    delete_setup                    = False
    # setup configurations
    rebalance_periods               = 21
    liquidity_filter                = 1
    asset_quantity                  = 5
    user_name_adm                   = 'jandretebarf'


    # enable rebalance wallet
    rebalance_wallets               = False
    factor_calc_initial_date        = '2020-12-31'
    rebalance_calc_end_date         = '2023-12-31'
    # rebalance_wallet_id             = '3657'
    # rebalance_wallet_id             = '5480'
    rebalance_wallet_id             = '4819'


    # enable generation of wallet
    generate_wallets                = False
    factor_calc_end_date            = '2024-12-30'
    create_wallets_pfd              = False
    

    # enable configure wallet composition database
    config_wallet_composition       = False
    read_wallet_composition         = False
    save_wallet_composion           = False


    # enable requirements.txt update
    optimize_setup                  = False

    # enable requirements.txt update
    update_requirements_txt         = False

    ###
    ##
    #update_database
    ##
    ###
    fintz_demonstration_list = [
                                'AcoesEmCirculacao', 'TotalAcoes',
                                'PatrimonioLiquido',
                                'LucroLiquido12m', 'LucroLiquido',
                                'ReceitaLiquida', 'ReceitaLiquida12m', 
                                'DividaBruta', 'DividaLiquida',
                                # 'Disponibilidades', 
                                'Ebit', 'Ebit12m',
                                # 'Impostos', 'Impostos12m',
                                # 'LucroLiquidoSociosControladora',
                                # 'LucroLiquidoSociosControladora12m'
                                ]

    fintz_indicators_list = [
                            # 'L_P', 'ROE', 'ROIC', 'EV', 'LPA', 'P_L', 'EBIT_EV', 
                            'ValorDeMercado'
                            ]
    
    bc_dict = {
                'selic':    {'bc_code': '432'},
                'ipca':     {'bc_code': '433'},
                'dolar':    {'bc_code': '1'},
                }

    if(update_database):

        finapp.run_update_database(update_fintz_database = update_fintz_database, update_api_database = update_api_database, update_webscrapping_database = update_webscrapping_database,
                                   fintz_indicators_list = fintz_indicators_list, fintz_demonstration_list = fintz_demonstration_list)

    ###
    ##
    #update_asset_profile
    ##
    ###
    if(update_asset_profile):

        print(".\n..\n...\nUpdating Asset Profile!\n...\n..\n.")

        profile_updater = uap.UpdateAssetProfile()

        profile_updater.getting_assets_database()
        profile_updater.getting_assets_from_quotation()
        profile_updater.calculationg_growth_rate()
        profile_updater.calculationg_marketshare()
        profile_updater.save_profile_database()

        profile_updater.read_profile_database()
   
    ###
    ##
    #bcg_matrix
    ##
    ###
    bcg_dimensions_list = [
                        'sector', 
                        'subsector',
                    ]

    if(update_bcg_matrix):

        print(".\n..\n...\nCreating BCG Matrix!\n...\n..\n.")

        bcg_matrix = cbm.BcgMatrix(bcg_dimensions_list)

        bcg_matrix.create_bcg_matrix()

    ###
    ##
    #make_indicators
    ##
    ###
    if(update_indicators):

        finapp.run_make_indicators()

    ###
    ##
    #risk_premiuns
    ##
    ###
    indicators_dict = {
                        'ValorDeMercado':     {'file_name': 'TAMANHO_VALOR_DE_MERCADO',   'order': 'crescente'},
                        # 'ROIC':               {'file_name': 'QUALITY_ROIC',               'order': 'decrescente'},
                        # 'ROE':                {'file_name': 'QUALITY_ROE',                'order': 'decrescente'},
                        # 'EBIT_EV':            {'file_name': 'VALOR_EBIT_EV',              'order': 'decrescente'},
                        # 'L_P':                {'file_name': 'VALOR_L_P',                  'order': 'decrescente'},
                        # 'vol_252':            {'file_name': 'RISCO_VOL',                  'order': 'crescente'},
                        # 'ebit_dl':            {'file_name': 'ALAVANCAGEM_EBIT_DL',        'order': 'decrescente'},
                        # 'pl_db':              {'file_name': 'ALAVANCAGEM_PL_DB',          'order': 'decrescente'},
                        'mm_7_40':            {'file_name': 'MOMENTO_MM_7_40',            'order': 'decrescente'},
                        # 'momento_1_meses':    {'file_name': 'MOMENTO_R1M',                'order': 'decrescente'},
                        # 'momento_6_meses':    {'file_name': 'MOMENTO_R6M',                'order': 'decrescente'},
                        'momento_12_meses':   {'file_name': 'MOMENTO_R12M',               'order': 'decrescente'},
                        # 'peg_ratio':          {'file_name': 'PEG_RATIO_INVERT',           'order': 'decrescente'},
                        'p_vp_invert':        {'file_name': 'P_VP_INVERT',                'order': 'decrescente'},
                        # 'p_ebit_invert':      {'file_name': 'P_EBIT_INVERT',              'order': 'decrescente'},
                        # 'net_margin':         {'file_name': 'NET_MARGIN',                 'order': 'decrescente'},
                        }

    indicators_dict_database = {
                        'ValorDeMercado':     {'file_name': 'TAMANHO_VALOR_DE_MERCADO',   'order': 'crescente'},
                        'ROIC':               {'file_name': 'QUALITY_ROIC',               'order': 'decrescente'},
                        'ROE':                {'file_name': 'QUALITY_ROE',                'order': 'decrescente'},
                        'EBIT_EV':            {'file_name': 'VALOR_EBIT_EV',              'order': 'decrescente'},
                        'L_P':                {'file_name': 'VALOR_L_P',                  'order': 'decrescente'},
                        'vol_252':            {'file_name': 'RISCO_VOL',                  'order': 'crescente'},
                        'ebit_dl':            {'file_name': 'ALAVANCAGEM_EBIT_DL',        'order': 'decrescente'},
                        'pl_db':              {'file_name': 'ALAVANCAGEM_PL_DB',          'order': 'decrescente'},
                        'mm_7_40':            {'file_name': 'MOMENTO_MM_7_40',            'order': 'decrescente'},
                        'momento_1_meses':    {'file_name': 'MOMENTO_R1M',                'order': 'decrescente'},
                        'momento_6_meses':    {'file_name': 'MOMENTO_R6M',                'order': 'decrescente'},
                        'momento_12_meses':   {'file_name': 'MOMENTO_R12M',               'order': 'decrescente'},
                        'peg_ratio':          {'file_name': 'PEG_RATIO_INVERT',           'order': 'decrescente'},
                        'p_vp_invert':        {'file_name': 'P_VP_INVERT',                'order': 'decrescente'},
                        'p_ebit_invert':      {'file_name': 'P_EBIT_INVERT',              'order': 'decrescente'},
                        'net_margin':         {'file_name': 'NET_MARGIN',                 'order': 'decrescente'},
                        }
    

    if(calculate_risk_premiuns):

        finapp.run_calculate_risk_premiuns(indicators_dict, 
                                          single_combinations, double_combinations, triple_combinations, 
                                          update_existing_file)

    ###
    ##
    #rate_risk_premiuns   
    ##
    ###
    number_of_top_comb_indicators = 5

    if(rate_risk_premiuns):

        distribution_indicadors, ranking_indicator, top_indicators, fail_to_execute = finapp.run_rate_risk_premius(
                                                                            indicators_dict=indicators_dict,
                                                                            final_analysis_date=final_analysis_date, 
                                                                            rating_premiuns_file_name=rating_premiuns_file_name,
                                                                            number_of_top_comb_indicators=number_of_top_comb_indicators,
                                                                            create_rating_pdf=create_rating_pdf,
                                                                            single_combinations=single_combinations,
                                                                            double_combinations=double_combinations,
                                                                            triple_combinations=triple_combinations)
        
        

        ##
        # CREATE AUTOMATIC PONDERATED WALLET
        ##
        setup_dict = finapp.create_automatic_wallet(ranking_indicator, indicators_dict)

        ##
        # exibindo resultado do melhor indicador combinado
        ##
        best_indicator = ranking_indicator[ranking_indicator['ranking_indicators'] == 1]
        print('.\n.\nO melhor indicador até a data definida foi: ', str(best_indicator['nome_indicador'].iloc[-1]))
        print('\t rentabilidade acumulada do primeiro_quartil: ', int((best_indicator['acum_primeiro_quartil'].iloc[-1]) * 100), '%')
        print('\t rentabilidade acumulada do segundo_quartil: ', int((best_indicator['acum_segundo_quartil'].iloc[-1]) * 100), '%')
        print('\t rentabilidade acumulada do terceiro_quartil: ', int((best_indicator['acum_terceiro_quartil'].iloc[-1]) * 100), '%')
        print('\t rentabilidade acumulada do quarto_quartil: ', int((best_indicator['acum_quarto_quartil'].iloc[-1]) * 100), '%')

        #
        ##
        # PREPARING DATA FOR REGRESSION
        number_of_top_single_indicators = 3
        top_single_indicators = distribution_indicadors.head(number_of_top_single_indicators)
        # print('.\n.\ntop_single_indicators', number_of_top_single_indicators, ': \n', top_single_indicators['nome_indicador'])

        premiuns_to_regression_dict = dict.fromkeys(top_single_indicators['nome_indicador'], 1000000)

        print('\nAutomatic wallet dict created: \n', setup_dict)

        print(".\n.\n=== RATING COMPLETE! ===")

    ###
    ##
    #regression_model
    ##
    ###
    if(execute_regression_model):

        print(".\n..\n...\nRunning Regression Model!\n...\n..\n.")

        print('\nPremius to regression: \n', premiuns_to_regression_dict)

        fazendo_modelo = rm.linear_regression(data_final_analise= "2021-12-31", dicionario_fatores = premiuns_to_regression_dict, 
                                       caminho_premios_de_risco=R'./finapp/files/risk_premiuns',
                                       caminho_cdi = R'./finapp/files')

        fazendo_modelo.getting_premium_data()
        fazendo_modelo.calculating_universe()
        fazendo_modelo.execute_regression()


    ###
    ##
    # save setup in database
    ##
    ###
    create_date_auto = datetime.now()
    create_date_auto = create_date_auto.strftime('%Y-%m-%d')

    if(config_setups):

        wallet_manager = wm.WalletManager()
        
        wallet_id_existent = None
        new_wallet_id = None
        wallet_existent = False

        if(read_setup):

            wallet_manager.read_setups()

        if(save_setup):
            
            new_setup_to_insert = wallet_manager.preparing_setup_data(setups_dict = setup_dict, number_of_assets = asset_quantity, rebalance_periods = rebalance_periods, user_name = user_name_adm, create_date = create_date_auto)

            wallet_id, wallet_existent, validation_df, setup_duplicated = wallet_manager.insert_setup(wallet_manager = wallet_manager, new_setup = new_setup_to_insert)
            # print('wallet_id_existent', wallet_id_existent)
            # print('new_wallet_id', new_wallet_id)

        if(close_setup):

            wallet_manager.close_setup(wallet_id='first-shot', user_name='pacient-zero', close_date = '2099-18-12')

        if(delete_setup):

            wallet_manager.delete_setup(wallet_manager = wallet_manager, wallet_id='227', user_name='andre-tebar')
    
        ###
    

    ##
    # rebalance wallets
    ##
    ###
    if(rebalance_wallets):

        print(".\n..\n...\nRebalancing Wallet(s)!\n...\n..\n.")

        # print('\nrebalance_wallet_id: \n', rebalance_wallet_id)

        wallet_to_database = finapp.run_rebalance_setups(rebalance_wallet_id, rebalance_calc_end_date, indicators_dict_database, factor_calc_initial_date,
                                                        liquidity_filter)


    ###
    ##
    #factor_calculator
    ##
    ###
    if(generate_wallets):

        wallets, returns = finapp.run_factor_calculator(setup_dict, 
                                                            factor_calc_end_date=factor_calc_end_date, factor_calc_initial_date=factor_calc_initial_date, 
                                                            asset_quantity=asset_quantity, rebalance_periods=rebalance_periods, liquidity_filter=liquidity_filter,
                                                            create_wallets_pfd=create_wallets_pfd)

        print('\n\n',wallets)

        finapp.run_last_generated_wallet(wallets)


    ###
    ##
    # configure wallet composition
    ##
    ###
    if(config_wallet_composition):

        print(".\n..\n...\nConfiguring Wallet(s) Composition!\n...\n..\n.")

        wallet_manager = wm.WalletManager()

        # if wallet_existent is False:
        #     print('\n ---no wallet defined or found! forcing save_wallet_composion to FALSE...\n')
        #     wallet_id = str(wallet_id)
        #     save_wallet_composion = False

        if(read_wallet_composition):
            
            file_not_found, compositions_df = wallet_manager.read_portifolios_composition()
        
        if(save_wallet_composion):

            print('\nWallet to database: \n', wallet_to_database)

            wallet_manager.update_portifolio_composition(wallet_manager = wallet_manager, wallet_id = rebalance_wallet_id, wallet_defined = wallet_to_database)



    ###
    ##
    # optimize setup
    ##
    ###
    if(optimize_setup):
        print('')
        finapp.run_optimize_setup(rebalance_wallet_id, indicators_dict_database)

    ###
    ##
    #update requirements.txt file
    ##
    ###
    if(update_requirements_txt):

        print("initializing requirements update")
        requirements_update_command = "pip freeze"
        requirements_data = subprocess.check_output(requirements_update_command, shell=True, text=True)

        current_folder = os.getcwd()

        project_folder = os.getenv("PROJECT_FOLDER")

        if(current_folder != project_folder):
            os.chdir(project_folder)

        requirements_file_name = 'requirements.txt'
            
        full_desired_path = os.path.join(project_folder, requirements_file_name)

        with open(full_desired_path, "w") as arquivo:
            arquivo.write(requirements_data)
    
    end_time_execution = time.time()

    execution_time_in_sec = round((end_time_execution - init_time_execution), 2)
    execution_time_in_min = round((execution_time_in_sec / 60.0), 2)

    print(f'\nexcution_time: {execution_time_in_sec} seconds. [{execution_time_in_min} min]')