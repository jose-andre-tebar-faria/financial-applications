import finapp_controller as fc
import telegram_user_manager as tum
import wallet_manager as wm

import numpy as np
from io import StringIO
import time
import ast
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta, timezone
import re
import concurrent.futures
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, CallbackContext, ContextTypes

class TelegramManager:

    def __init__(self):
                
        print("\n\nInicializing Telegram Manager!\n.")

        load_dotenv()

        current_folder = os.getcwd()

        project_folder = os.getenv("PROJECT_FOLDER")
        databse_folder = os.getenv("DATABASE_FOLDER")
        self.full_desired_path = os.path.join(project_folder,databse_folder)

        if(current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

    # responses
    def handle_responses(answer_text: str, text: str, username: str, new_user: bool, adm_interaction: bool, fail_to_execute: bool, enable_interaction: bool, is_command:bool):

        processed_text: str = text.lower()

        print('\nnew_user: ', new_user)
        print('\nadm_interaction: ', adm_interaction)
        print('\nenable_interaction: ', enable_interaction)
        print('\nis_command: ', is_command)
        print('\nfail_to_execute: ', fail_to_execute)
        # print('\nanswer_text: ', answer_text)

        if(is_command and fail_to_execute == False):
            if 'save_username' in processed_text:
                if new_user:
                    if enable_interaction:
                        return f'🔒 thanks to setup your user!!\n.\n😄 username: {username}'
                    else:
                        return f'💬 verify telegram setup - username, first name, last name must exists.'
                else:
                    return f'🔑 you already made a setup with us. thank you!!\n.\n😄 username: {username}'
            if 'rate_risk_premiuns' in processed_text:
                return answer_text
            if 'rank_risk_premiuns' in processed_text:
                return answer_text
            if 'rebalance_setup' in processed_text:
                return answer_text
            if 'read_setups' in processed_text:
                return answer_text  
            if 'nightvision' in processed_text:
                return answer_text
            if 'delete_setup' in processed_text:
                return answer_text
            if 'read_portifolio' in processed_text:
                return answer_text
            if 'execute_rebalance' in processed_text:
                return answer_text
            if 'report_setup' in processed_text:
                return answer_text
            if adm_interaction:
                if 'update_database' in processed_text:
                    return '📥 database updated! 📥'
                if 'make_indicators' in processed_text:
                    return '🧩 indicators updated! 🧩'
                if 'calculate_risk_premiuns' in processed_text:
                    return '✏ calculation complete! ✏'
            else:
                return '💬 command only for adms! 🍰'    
            return '💬 invalid command 😟'
        elif(is_command and fail_to_execute == True):
            return '💬 execution error! verify command... 🤨'

        if 'hello' in processed_text:
            return '💬 i see you!!'
        else:
            return '💬 Use o comando /help para te guiar quais os tipos de mensagens eu respondo.'
    
    ###
    ##
    # COMMANDS
    ##
    ###

    def update_database_command():
        
        finapp = fc.FinappController()
        
        # enable database update
        update_api_database             = False
        update_fintz_database           = True
        update_webscrapping_database    = False


        fintz_demonstration_list = [
                                    #'AcoesEmCirculacao', 'TotalAcoes',
                                    'PatrimonioLiquido',
                                    #'LucroLiquido12m', 'LucroLiquido',
                                    #'ReceitaLiquida', 'ReceitaLiquida12m', 
                                    #'DividaBruta', 'DividaLiquida',
                                    #'Disponibilidades', 
                                    #'Ebit', 'Ebit12m',
                                    #'Impostos', 'Impostos12m',
                                    #'LucroLiquidoSociosControladora',
                                    #'LucroLiquidoSociosControladora12m'
                                    ]

        fintz_indicators_list = [
                                'L_P', 'ROE', 'ROIC', 'EV', 'LPA', 'P_L', 'EBIT_EV', 'ValorDeMercado'
                                ]
        
        bc_dict = {
                    'selic':    {'bc_code': '432'},
                    'ipca':     {'bc_code': '433'},
                    'dolar':    {'bc_code': '1'},
                    }

        if(update_fintz_database):

            finapp.run_update_database(update_fintz_database = update_fintz_database, update_api_database = update_api_database, update_webscrapping_database = update_webscrapping_database,
                                    fintz_indicators_list = fintz_indicators_list, fintz_demonstration_list = fintz_demonstration_list,
                                    bc_dict = bc_dict)

    def make_indicators_command():
        
        finapp = fc.FinappController()

        finapp.run_make_indicators()

    def calculate_risk_premiuns_command(indicators_dict, single_combinations, double_combinations, triple_combinations, update_existing_file):
        
        list_combinations = []
        premium_dataframe = pd.DataFrame()

        finapp = fc.FinappController()
        
        list_combinations, premium_dataframe = finapp.run_calculate_risk_premiuns(indicators_dict=indicators_dict, 
                                                    single_combinations=single_combinations, double_combinations=double_combinations, triple_combinations=triple_combinations, 
                                                    update_existing_file=update_existing_file)
        
        return list_combinations, premium_dataframe

    def rate_risk_premiuns_command(indicators_dict, single_combinations, double_combinations, triple_combinations, create_rating_pdf, final_analysis_date):
                
        # final_analysis_date             = '2022-12-31'
        rating_premiuns_file_name       = r'..\\PDFs\rating-INDICATORS.pdf'
        # create_rating_pdf               = False
        distribution_indicadors = pd.DataFrame()
        
        number_of_top_comb_indicators = 5
    
        single_combinations = bool(single_combinations)
        double_combinations = bool(double_combinations)
        triple_combinations = bool(triple_combinations)

        finapp = fc.FinappController()
        
        distribution_indicadors, ranking_indicator, top_indicators, fail_to_execute = finapp.run_rate_risk_premius(
                                                        indicators_dict=indicators_dict,
                                                        final_analysis_date=final_analysis_date, 
                                                        rating_premiuns_file_name=rating_premiuns_file_name,
                                                        number_of_top_comb_indicators=number_of_top_comb_indicators,
                                                        create_rating_pdf=create_rating_pdf,
                                                        single_combinations=single_combinations, double_combinations=double_combinations,
                                                        triple_combinations=triple_combinations
                                                        )
                
        ##
        # CREATE AUTOMATIC PONDERATED WALLET
        ##
        setup_dict = finapp.create_automatic_wallet(ranking_indicator, indicators_dict)

        return distribution_indicadors, ranking_indicator, top_indicators, setup_dict, fail_to_execute

    def rank_risk_premiuns_command(indicators_dict, single_combinations, double_combinations, triple_combinations, create_rating_pdf, final_analysis_date, initial_analysis_date,
                                   step_months_rank_list, columns_rank_database_list, columns_rank_list, premiuns_to_dict, premiuns_to_show):
        
        rating_premiuns_file_name       = r'..\\PDFs\rating-INDICATORS.pdf'
        # create_rating_pdf               = False
    
        single_combinations = bool(single_combinations)
        double_combinations = bool(double_combinations)
        triple_combinations = bool(triple_combinations)

        finapp = fc.FinappController()

        premiuns_statistics_to_show, analyzed_windows_df, setup_dict, combined_min_data_inicial, data_inicial, combined_max_data_final, data_final, fail_to_execute = finapp.run_rank_risk_premiuns(indicators_dict, initial_analysis_date, final_analysis_date, 
                                                                                                                        rating_premiuns_file_name, 
                                                                                                                        single_combinations, double_combinations, triple_combinations, 
                                                                                                                        create_rating_pdf,
                                                                                                                        step_months_rank_list, columns_rank_database_list, columns_rank_list,
                                                                                                                        premiuns_to_dict, premiuns_to_show)


        print('\npremiuns_statistics_to_show: \n', premiuns_statistics_to_show)
        
        number_rank_combinations = len(premiuns_statistics_to_show)

        print('\nnumber_rank_combinations: ', number_rank_combinations)
        first_quartile = int(np.ceil(number_rank_combinations/4))
        print('\nfirst_quartile: ', first_quartile)

        filtered_premiuns_statistics_to_show = premiuns_statistics_to_show.head(first_quartile)

        file_names = []

        for indicator, indicator_info in indicators_dict.items():
            file_name = indicator_info['file_name']
            # print(f"Indicator: {indicator}, File Name: {file_name}")
            file_names.append(file_name)

        # print(file_names)
        
        # Cria todos os pares possíveis de indicadores
        pairs_of_indicators = [(file_names[i], file_names[j]) for i in range(len(file_names)) for j in range(i + 1, len(file_names))]

        # Contador para armazenar a contagem de cada file_name no primeiro quartil
        single_indicators_count_dict = {file_name: 0 for file_name in file_names}

        # Contador para armazenar a contagem de cada par de indicadores no primeiro quartil
        pair_indicators_count_dict = {par: 0 for par in pairs_of_indicators}

        # Itera sobre as linhas do DataFrame
        for index, row in premiuns_statistics_to_show.iterrows():
            premium_name = row['premium_name']
            
            # Verifica se cada file_name está contido no premium_name
            for file_name in file_names:
                if file_name in premium_name:
                    single_indicators_count_dict[file_name] += 1

            # Verifica se cada par de indicadores está contido no premium_name
            for pair in pairs_of_indicators:
                if all(indicador in premium_name for indicador in pair):
                    pair_indicators_count_dict[pair] += 1

        pair_indicators_total_count = list(pair_indicators_count_dict.values())[0]
        print ('\npair_indicators_total_count: \n', pair_indicators_total_count)
        single_indicators_total_count = list(single_indicators_count_dict.values())[0]
        print ('\nsingle_indicators_total_count: \n', single_indicators_total_count)


        # Reseta o Contador
        single_indicators_count_dict = {file_name: 0 for file_name in file_names}

        pair_indicators_count_dict = {par: 0 for par in pairs_of_indicators}

        # Itera sobre as linhas do DataFrame
        for index, row in filtered_premiuns_statistics_to_show.iterrows():
            premium_name = row['premium_name']
            
            # Verifica se cada file_name está contido no premium_name
            for file_name in file_names:
                if file_name in premium_name:
                    single_indicators_count_dict[file_name] += 1

            # Verifica se cada par de indicadores está contido no premium_name
            for pair in pairs_of_indicators:
                if all(indicador in premium_name for indicador in pair):
                    pair_indicators_count_dict[pair] += 1

        # Cria um DataFrame a partir do dicionário de contagens
        single_indicator_count = pd.DataFrame(list(single_indicators_count_dict.items()), columns=['indicator', 'count_first_quartile'])

        single_indicator_count = single_indicator_count.sort_values(by='count_first_quartile', ascending=False)

        single_indicator_count = single_indicator_count.reset_index(drop=True)

        print ('\ncount_first_quartile: \n', single_indicator_count)

        # Cria um DataFrame a partir do dicionário de contagens
        pairs_indicator_count = pd.DataFrame(list(pair_indicators_count_dict.items()), columns=['pair_indicators', 'contagem_no_primeiro_quartil'])

        # Classifica o DataFrame pelo valor da contagem
        pairs_indicator_count = pairs_indicator_count.sort_values(by='contagem_no_primeiro_quartil', ascending=False)

        print('\npairs_indicator_count: \n', pairs_indicator_count)

        return premiuns_statistics_to_show, analyzed_windows_df, combined_min_data_inicial, data_inicial, combined_max_data_final, data_final, setup_dict, single_indicator_count, single_indicators_total_count, pairs_indicator_count, pair_indicators_total_count

    def rebalance_setup_command(rebalance_wallet_id, rebalance_calc_end_date, indicators_dict_database, factor_calc_initial_date, liquidity_filter):
        
        finapp = fc.FinappController()

        wallet_to_database = pd.DataFrame()

        # print(rebalance_wallet_id)
        print('rebalance_calc_end_date: ', rebalance_calc_end_date)
        # print(indicators_dict_database)
        # print(factor_calc_initial_date)
        # print(liquidity_filter)
        # print(wallet_to_database)

        wallet_to_database = finapp.run_rebalance_setups(rebalance_wallet_id=rebalance_wallet_id, 
                                                         rebalance_calc_end_date=rebalance_calc_end_date, 
                                                         indicators_dict_database=indicators_dict_database,
                                                         factor_calc_initial_date=factor_calc_initial_date,
                                                         liquidity_filter=liquidity_filter)
        
        # print(wallet_to_database)

        return wallet_to_database

    def read_setups_command(username_existent):

        wallet_manager = wm.WalletManager()
        file_not_found, wallets_df = wallet_manager.read_setups(username_existent)

        return wallets_df

    def nightvision_command(wallet_id, rebalance_date):

        weighted_average_returns = None
        last_analysis_date = None
        final_analysis = pd.DataFrame()

        finapp = fc.FinappController()

        wallet_manager = wm.WalletManager()

        file_not_found, compositions_df = wallet_manager.read_portifolios_composition()
        
        compositions_df['wallet_id'] = compositions_df['wallet_id'].astype(int)
        compositions_df = compositions_df[compositions_df['wallet_id'] == int(wallet_id)]

        print('compositions_df: \n', compositions_df)

        if compositions_df.empty:
            return final_analysis, last_analysis_date, weighted_average_returns
        else:
            final_analysis, last_analysis_date, weighted_average_returns = finapp.run_nightvision_wallet(compositions_df, wallet_id, rebalance_date)
                
            return final_analysis, last_analysis_date, weighted_average_returns

    def delete_setup_command(wallet_id, username_existent):

        setup_to_delete = pd.DataFrame()

        wallet_manager = wm.WalletManager()
        
        setup_to_delete = wallet_manager.delete_setup(wallet_manager = wallet_manager, wallet_id = wallet_id, user_name=username_existent)

        return setup_to_delete
    
    def read_portifolio_command(wallet_id):

        wallet_manager = wm.WalletManager()

        file_not_found, compositions_df = wallet_manager.read_portifolios_composition(wallet_id)

        if file_not_found:

            number_of_compositions = 0
            last_dates = []
            compositions_df = pd.DataFrame()

            return number_of_compositions, last_dates, compositions_df
        else:

            compositions_df['rebalance_date'] = pd.to_datetime(compositions_df['rebalance_date'])

            compositions_df = compositions_df.sort_values(by='rebalance_date', ascending=False)

            last_dates = compositions_df['rebalance_date'].unique()[:3]

            number_of_compositions = len(last_dates)

            compositions_df = compositions_df[compositions_df['rebalance_date'].isin(last_dates)]

        return number_of_compositions, last_dates, compositions_df

    def execute_rebalance_command(wallet_id, rebalance_date):

        finapp = fc.FinappController()

        orders = pd.DataFrame()

        orders = finapp.run_execute_rebalance(wallet_id, rebalance_date)

        return orders

    def report_setup_command(wallet_id, username_existent, indicators_dict_database):

        finapp = fc.FinappController()

        setup_dict, rebalance_periods_setup, asset_quantity_setup = finapp.create_setup_dict(wallet_id, indicators_dict_database)
        print('setup_dict: \n', setup_dict)
        rebalance_periods_setup = int(rebalance_periods_setup)
        print('rebalance_periods_setup: ', rebalance_periods_setup)

        factor_calc_end_date = '2024-01-31'
        factor_calc_initial_date = '2019-12-31'
        # asset_quantity_setup = 5
        liquidity_filter_setup = 1
        create_wallets_pfd = True

        # wallets, returns = finapp.run_factor_calculator(setup_dict=setup_dict, 
        #                                                     factor_calc_end_date=factor_calc_end_date, factor_calc_initial_date=factor_calc_initial_date, 
        #                                                     asset_quantity=asset_quantity_setup, rebalance_periods=rebalance_periods_setup, liquidity_filter=liquidity_filter_setup,
        #                                                     create_wallets_pfd=create_wallets_pfd)
        
        pdf_name = finapp.run_report_setups(wallet_id=wallet_id, 
                                            factor_calc_initial_date=factor_calc_initial_date, factor_calc_end_date=factor_calc_end_date, 
                                            indicators_dict_database=indicators_dict_database,
                                            liquidity_filter=liquidity_filter_setup,
                                            create_wallets_pfd=create_wallets_pfd, username_existent=username_existent)
                
        return pdf_name

    ###
    ##
    # TOOLS
    ##
    ###
    def extract_elements_from_command(match):

        indicators_list = []
        variables_list = []

        elements = match.group(1)

        if elements is not None:
            decoded_elements_list = elements.split(',')
            decoded_elements_list = [indicator.strip() for indicator in decoded_elements_list]
            
            number_of_variables = sum('=' in elemento for elemento in decoded_elements_list)
            # print(number_of_variables)

            if(number_of_variables > 0):
                indicators_list = decoded_elements_list[:-number_of_variables]
                variables_list = decoded_elements_list[-number_of_variables:]
                variables_list = [txt.replace(" ", "") for txt in variables_list]
            else:
                indicators_list = decoded_elements_list

        return indicators_list, variables_list
        
    def decode_command(command_string):

        indicators_list = []
        variables_list = []
        
        # lógica para aceitar quando o comando tem caracteres maiúsculos
        # command_string = command_string.lower()
        
        save_username_pattern = re.compile(r'save_username')
        update_fintz_database_pattern = re.compile(r'update_database')
        make_indicators_pattern = re.compile(r'make_indicators')
        read_setups_pattern = re.compile(r'read_setups')
        calculate_risk_premiuns_pattern = re.compile(r'calculate_risk_premiuns\s*\(([^)]+)\)')
        rate_risk_premiuns_pattern = re.compile(r'rate_risk_premiuns\s*\(([^)]+)\)')
        rank_risk_premiuns_pattern = re.compile(r'rank_risk_premiuns\s*\(([^)]+)\)')
        rebalance_setup_pattern = re.compile(r'rebalance_setup\s*\(([^)]+)\)')
        nightvision_pattern = re.compile(r'nightvision\s*\(([^)]+)\)')
        delete_setup_pattern = re.compile(r'delete_setup\s*\(([^)]+)\)')
        read_portifolio_pattern = re.compile(r'read_portifolio\s*\(([^)]+)\)')
        execute_rebalance_pattern = re.compile(r'execute_rebalance\s*\(([^)]+)\)')
        report_setup_pattern = re.compile(r'report_setup\s*\(([^)]+)\)')

        if save_username_pattern.match(command_string):

            return {'command': 'save_username'}, indicators_list, variables_list
        elif update_fintz_database_pattern.match(command_string):

            return {'command': 'update_database'}, indicators_list, variables_list
        elif make_indicators_pattern.match(command_string):

            return {'command': 'make_indicators'}, indicators_list, variables_list
        elif rebalance_setup_pattern.match(command_string):

            match = rebalance_setup_pattern.match(command_string)

            indicators_list, variables_list = TelegramManager.extract_elements_from_command(match)

            return {'command': 'rebalance_setup'}, indicators_list, variables_list
        elif nightvision_pattern.match(command_string):

            match = nightvision_pattern.match(command_string)

            indicators_list, variables_list = TelegramManager.extract_elements_from_command(match)

            return {'command': 'nightvision'}, indicators_list, variables_list
        elif calculate_risk_premiuns_pattern.match(command_string):

            match = calculate_risk_premiuns_pattern.match(command_string)

            indicators_list, variables_list = TelegramManager.extract_elements_from_command(match)

            return {'command': 'calculate_risk_premiuns'}, indicators_list, variables_list
        elif rate_risk_premiuns_pattern.match(command_string):

            match = rate_risk_premiuns_pattern.match(command_string)

            indicators_list, variables_list = TelegramManager.extract_elements_from_command(match)
            
            return {'command': 'rate_risk_premiuns'}, indicators_list, variables_list
        elif rank_risk_premiuns_pattern.match(command_string):

            match = rank_risk_premiuns_pattern.match(command_string)

            indicators_list, variables_list = TelegramManager.extract_elements_from_command(match)
            
            return {'command': 'rank_risk_premiuns'}, indicators_list, variables_list
        elif delete_setup_pattern.match(command_string):

            match = delete_setup_pattern.match(command_string)

            indicators_list, variables_list = TelegramManager.extract_elements_from_command(match)
            
            return {'command': 'delete_setup'}, indicators_list, variables_list
        elif read_portifolio_pattern.match(command_string):

            match = read_portifolio_pattern.match(command_string)

            indicators_list, variables_list = TelegramManager.extract_elements_from_command(match)
            
            return {'command': 'read_portifolio'}, indicators_list, variables_list
        elif execute_rebalance_pattern.match(command_string):

            match = execute_rebalance_pattern.match(command_string)

            indicators_list, variables_list = TelegramManager.extract_elements_from_command(match)
            
            return {'command': 'execute_rebalance'}, indicators_list, variables_list
        elif report_setup_pattern.match(command_string):

            match = report_setup_pattern.match(command_string)

            indicators_list, variables_list = TelegramManager.extract_elements_from_command(match)
            
            return {'command': 'report_setup'}, indicators_list, variables_list
        elif read_setups_pattern.match(command_string):
            
            return {'command': 'read_setups'}, indicators_list, variables_list
        else:
            return {'command': 'unknown'}, indicators_list, variables_list

    def create_rating_answer(distribution_indicadors, ranking_indicator, top_indicators, setup_dict, indicators_dict_database, save_setup, wallet_id, wallet_existent, wallets_df):

        markdown_text = f'🏆 rating complete! 🏆\n\n'

        distribution_indicadors['acum_primeiro_quartil'] = distribution_indicadors['acum_primeiro_quartil'].astype(float)
        distribution_indicadors['acum_primeiro_quartil'] = distribution_indicadors['acum_primeiro_quartil'] * 100
        distribution_indicadors['acum_primeiro_quartil'] = round(distribution_indicadors['acum_primeiro_quartil'], 1)

        top_indicators['acum_primeiro_quartil'] = top_indicators['acum_primeiro_quartil'].astype(float)
        top_indicators['acum_primeiro_quartil'] = top_indicators['acum_primeiro_quartil'] * 100
        top_indicators['acum_primeiro_quartil'] = round(top_indicators['acum_primeiro_quartil'], 1)

        len_top_indicators = len(top_indicators)
        len_ranking_indicator = len(ranking_indicator)

        markdown_text += f"Foram avaliados {len_ranking_indicator} combinações dos prêmios de risco atrelado aos indicadores e a está abaixo o rank{len_top_indicators}!! O ranking final foi feito por percentual de rentabilidade, no final é mostrado o ranking dos indicadores puros mostrando o número de vezes que o indicador apareceu no rank final.\n"
        markdown_text += f"\nrank{len_top_indicators}: \n\n"

        # print(indicators_dict_database)
        rank_position = 1

        for _, row in top_indicators.iterrows():
            
            file_names = []
            keys = []

            indicator = row['nome_indicador'].split('-with-')
            file_names.extend(indicator)
            file_names =list(file_names)
            # print(file_names)
            
            keys = [key for key, value in indicators_dict_database.items() if value['file_name'] in file_names]
            # print(keys)

            markdown_text += f"{rank_position}º LUGAR:\n"
            markdown_text += f"----------------------------\n"
            for indicator in keys:
                markdown_text += f"\t{indicator}\n"
            markdown_text += f"----------------------------\n"
            
            markdown_text += f"Rentabilidade -> {row['acum_primeiro_quartil']}% / pure: {row['Pure']}\n\n"

            rank_position+=1
        
        markdown_text += f"Abaixo o rank dos indicadores sozinhos, mostrando a própria rentabilidade e número de vezes que apareceu no TOP{len_top_indicators}: \n\n"

        max_key_length = max(len(str(key)) for key, value in indicators_dict_database.items())

        for _, row in distribution_indicadors.iterrows():
            key = [key for key, value in indicators_dict_database.items() if value['file_name'] in row['nome_indicador']]
            key = str(key)

            spaces = '\xa0' * (12) 

            markdown_text += f"{key}:\n{spaces}{row['acum_primeiro_quartil']}% / count: {row['contagem']}\n"


        if save_setup:
            markdown_text += f"\n Carteira já cadastrada! iD: {wallet_id}\n"
        # print('wallet_existent: ',wallet_existent)
        # print('wallet_id', wallet_id)
        # print('wallets_df', wallets_df)

        return markdown_text

    def create_ranking_header_answer(premiuns_statistics_to_show, step_months_rank_list, analyzed_windows_df, columns_rank_list, data_inicial, data_final):

        statistics_columns_name = []
        total_analysed_windows = 0

        number_of_combinations = len(premiuns_statistics_to_show)

        markdown_text = f'🏆 RANKING COMPLETO!!! 🏆\n\n'
        
        markdown_text += f"Foram avaliados {number_of_combinations} combinações dos prêmios de risco atrelados aos indicadores. Os cálculos foram feitos considerando a janela temporal de {data_inicial} até {data_final}. "
        markdown_text += f"\n\nA avaliação de desempenho foi realizada para os seguintes janelas temporais:\n"

        for period in step_months_rank_list:

            analysed_windows = analyzed_windows_df['analyzed_windows'][analyzed_windows_df['months_window_size'] == period]
            analysed_windows = int(analysed_windows.iloc[0])
            total_analysed_windows += analysed_windows

            markdown_text += f"          ⌛ {period} meses / {analysed_windows} janelas analisadas.\n"

        total_executions= number_of_combinations * total_analysed_windows

        markdown_text += f"\n🚅 Totalizando {total_executions} janelas temporais executadas!!\n"

        markdown_text += f"\n Escolheu-se a(s) seguinte(s) estatísitica(s) para realizar o ranking:\n"

        prefix = '_'
        sufix = '_months'

        columns_sufix_list = [prefix + str(item) + sufix for item in step_months_rank_list]

        for statistic in columns_rank_list:
            for sufix_columns in columns_sufix_list:
                column = statistic + sufix_columns
                statistics_columns_name.append(column)
                # print('\nstatistics_columns_name: \n', statistics_columns_name)
            markdown_text += f"          🌡 {statistic}\n"

        return markdown_text

    def create_indicator_count_answer(single_indicator_count, single_indicators_total_count, premiuns_statistics_to_show):
        
        number_of_combinations = len(premiuns_statistics_to_show)

        first_quartile = int(np.ceil(number_of_combinations/4))
        print('\nfirst_quartile: ', first_quartile)
        
        number_indicator_count = len(single_indicator_count)
        print('\nnumber_indicator_count: ', number_indicator_count)

        mean_count_first_quartile = int(sum(single_indicator_count['count_first_quartile']) / number_indicator_count)

        markdown_text = f'-- O ranking de indicadores mostrado abaixo realiza a contagem de vezes que cada indicador apareceu no primeiro quartil ({first_quartile}/{number_of_combinations}) do ranking. Cada indicador apareceu {single_indicators_total_count} vezes no ranking. \n\n'

        # Adiciona as linhas
        for _, row in single_indicator_count.iterrows():

            perc_quartile = (row['count_first_quartile']/first_quartile)*100
            perc_total = (row['count_first_quartile']/single_indicators_total_count)*100
            perc_quartile = round(float(perc_quartile),1)
            perc_total = round(float(perc_total),1)
            markdown_text += f" 💠 {row['indicator']} \n         - ocorrências no quartil: {row['count_first_quartile']}/{first_quartile} | {perc_quartile}% \n         - ocorrências no total:    {row['count_first_quartile']}/{single_indicators_total_count} | {perc_total}% \n"

        # Finaliza a string Markdown
        markdown_text += f'\nA média foi de {mean_count_first_quartile} aparições no primeiro quartil do ranking.'

        return markdown_text
    
    def create_pair_indicator_count_answer(pair_indicator_count, pair_indicators_total_count):
        
        number_pair_indicator_count = len(pair_indicator_count)
        print('\nnumber_pair_indicator_count: ', number_pair_indicator_count)

        first_ten_percent = int(np.ceil(number_pair_indicator_count/10))
        print('\nfirst_five_percent: ', first_ten_percent)

        pair_indicator_count = pair_indicator_count.head(first_ten_percent)

        mean_count_first_ten_percent = int(sum(pair_indicator_count['contagem_no_primeiro_quartil']) / first_ten_percent)

        markdown_text = f'-- O ranking mostrado abaixo exibe os 10% melhores ({first_ten_percent}/{number_pair_indicator_count}) pares de indicadores com respeito a mais ocorrências no primeiro quartil do ranking. Cada par apareceu {pair_indicators_total_count} vezes no ranking.\n\n'

        # Adiciona os cabeçalhos
        # markdown_text += "| pair_indicators | count_first_quartile |\n"
        # markdown_text += "|-----------|-----------------------|\n"

        # Adiciona as linhas
        # for _, row in pair_indicator_count.iterrows():
        #     markdown_text += f"| {row['pair_indicators']} | {row['contagem_no_primeiro_quartil']}/{pair_indicators_total_count} |\n"

        # Adiciona as linhas
        for _, row in pair_indicator_count.iterrows():

            perc_total = (row['contagem_no_primeiro_quartil']/pair_indicators_total_count)*100
            perc_total = round(float(perc_total),1)

            markdown_text += f"  🔍 {row['pair_indicators']} \n              - ocorrências no total: {row['contagem_no_primeiro_quartil']}/{pair_indicators_total_count} | {perc_total}%\n\n"

        # Finaliza a string Markdown
        # markdown_text += "```"
            
        markdown_text += f'\nA média foi de {mean_count_first_ten_percent} aparições de pares no primeiro quartil do ranking.'

        return markdown_text

    def create_ranking_answer(premiuns_to_show, premiuns_to_dict, columns_rank_list, step_months_rank_list, 
                              premiuns_statistics_to_show, setup_dict, indicators_dict_database, save_setup, wallet_id, wallet_existent, wallets_df, 
                              analyzed_windows_df,
                              append_text):
        
        print('\n>> creating ranking answer <<\n')

        top_rank_premiuns = premiuns_statistics_to_show.head(premiuns_to_show)
        # print('\ntop_rank_premiuns: \n', top_rank_premiuns)
        
        statistics_columns_name = []

        answer_text = ''
        markdown_text = f''

        prefix = '_'
        sufix = '_months'

        columns_sufix_list = [prefix + str(item) + sufix for item in step_months_rank_list]

        for statistic in columns_rank_list:
            for sufix_columns in columns_sufix_list:
                column = statistic + sufix_columns
                statistics_columns_name.append(column)

        markdown_text += f"\n-- RANKING {premiuns_to_show} PRIMEIROS\n"

        rank_position = 1

        for _, row in top_rank_premiuns.iterrows():
            
            file_names = []
            keys = []

            indicator = row['premium_name'].split('-with-')
            file_names.extend(indicator)
            file_names =list(file_names)
            # print(file_names)
            
            keys = [key for key, value in indicators_dict_database.items() if value['file_name'] in file_names]
            # print(keys)

            if rank_position == 1:
                markdown_text += f"\n🎖 {rank_position}º LUGAR:\n"
            elif rank_position == 2:
                markdown_text += f"\n🥈 {rank_position}º LUGAR:\n"
            elif rank_position == 3:
                markdown_text += f"\n🥉 {rank_position}º LUGAR:\n"
            else:
                markdown_text += f"\n{rank_position}º LUGAR:\n"

            markdown_text += f"----------------------------\n"
            for indicator in keys:
                markdown_text += f"  🔹 {indicator}\n"

            markdown_text += f"----------------------------\n"

            first_time = True
            last_column_name = ''

            for column_name in statistics_columns_name:

                column_name_str = str(column_name)
                
                if column_name[:9] != last_column_name[:9]:
                    first_time = True
                    last_column_name = column_name

                if '_perc_' in column_name:

                    row[column_name] = round(float(row[column_name]),2)

                    if first_time:
                        markdown_text += f"    profit_perc_\n"
                        first_time = False

                    months_to_show = column_name_str.rsplit('_', 2)[1]
                    months_to_show = column_name_str.rsplit('_', 2)[1]
                    column_name_to_show = months_to_show + '_months'

                    markdown_text += f"      🎰 {column_name_to_show} -> {row[column_name]}%\n"

                elif '_mean_acum_returns_' in column_name:

                    if first_time:
                        markdown_text += f"    anual_mean_acum_returns_\n"
                        first_time = False

                    row[column_name] = round(float(row[column_name])*100,2)

                    column_name_to_show = column_name_str.rsplit('_', 2)[1]
                    column_name_to_show = column_name_to_show + '_months'

                    markdown_text += f"       🟩 {column_name_to_show} -> {row[column_name]}% a.a.\n"

                elif '_high_acum_returns_' in column_name:
                    
                    row[column_name] = round(float(row[column_name])*100,2)

                    if first_time:
                        markdown_text += f"    anual_high_acum_returns_\n"
                        first_time = False

                    column_name_to_show = column_name_str.rsplit('_', 2)[1]
                    column_name_to_show = column_name_to_show + '_months'

                    markdown_text += f"       🟪 {column_name_to_show} -> {row[column_name]}% a.a.\n"
                elif '_low_acum_returns_' in column_name:
                    
                    row[column_name] = round(float(row[column_name])*100,2)

                    if first_time:
                        markdown_text += f"    anual_low_acum_returns_\n"
                        first_time = False

                    column_name_to_show = column_name_str.rsplit('_', 2)[1]
                    column_name_to_show = column_name_to_show + '_months'

                    markdown_text += f"       🟥 {column_name_to_show} -> {row[column_name]}% a.a.\n"
                elif 'last_acum_return_' in column_name:
                    
                    row[column_name] = round(float(row[column_name])*100,2)

                    if first_time:
                        markdown_text += f"    last_acum_return_\n"
                        first_time = False

                    column_name_to_show = column_name_str.rsplit('_', 2)[1]
                    # print(column_name_to_show)
                    column_name_to_show = column_name_to_show + '_months'
                    # print(column_name_to_show)

                    markdown_text += f"       🟧 {column_name_to_show} -> {row[column_name]}% \n"
                elif 'anual_std_dev_acum_returns_' in column_name:
                    
                    row[column_name] = round(float(row[column_name])*100,2)

                    if first_time:
                        markdown_text += f"    anual_std_dev_acum_returns_\n"
                        first_time = False

                    column_name_to_show = column_name_str.rsplit('_', 2)[1]
                    # print(column_name_to_show)
                    column_name_to_show = column_name_to_show + '_months'
                    # print(column_name_to_show)

                    markdown_text += f"       🟦 {column_name_to_show} -> {row[column_name]}%\n"
            
            rank_position+=1

        markdown_text += f"\n"

        markdown_text += append_text
        # print(markdown_text)

        answer_text = markdown_text

        return answer_text

    def create_read_setups_answer(username_existent, wallets_df):
        
        if wallets_df.empty:

            answer_text = '💬 setup duplicated! 🤨'
            return answer_text
        else:
        
            markdown_text = ''

            number_of_wallets = wallets_df['wallet_id'].nunique()
            number_of_wallets = int(number_of_wallets)

            markdown_text += f"📢 O usuário {username_existent} possui {number_of_wallets} setup(s) realizado(s).\n\n"
            # await update.message.reply_text(read_setups_txt)

            
            for _, group in wallets_df.groupby('wallet_id'):

                wallet_id = group['wallet_id'].iloc[0]
                rebalance_periods = group['rebalance_periods'].iloc[0]
                number_of_assets = group['number_of_assets'].iloc[0]
                create_date = group['create_date'].iloc[0]
                create_date = create_date.strftime('%Y-%m-%d')

                markdown_text += f"💼 wallet_id: {wallet_id}\n"
                markdown_text += f"----------------------------------------\n"

                markdown_text += f"          ⚙ rebalance_periods: {rebalance_periods}\n          ⚙ number_of_assets: {number_of_assets}\n          ⚙ create_date: {create_date}\n"

                print(f"wallet_id: {wallet_id}")
                print(f"          rebalance_periods: {rebalance_periods}")
                print(f"          number_of_assets: {number_of_assets}")
                print(f"          create_date: {create_date}")

                for _, row in group.iterrows():

                    wallet_name = row['wallet_name']
                    indicators = [indicator for indicator in row[['indicator_1', 'indicator_2', 'indicator_3']] if pd.notna(indicator)]
                    
                    markdown_text += f"          🔶 {wallet_name}:\n"

                    print(f"          {wallet_name}:")
                    for indicator in indicators:
                        print(f"                             {indicator}")
                        markdown_text += f"                             🔹 {indicator}\n"
                    
                markdown_text += f"\n"

            answer_text = markdown_text

            return answer_text

    def create_rebalance_setup_answer(username_existent, rebalance_wallet_id, wallet_to_database):

        markdown_text = '🏹🏹🏹 REBALANCE COMPLETE! 🏹🏹🏹\n\n'

        number_of_assets = wallet_to_database['ticker'].count()
        number_of_assets = int(number_of_assets)

        rebalance_date = wallet_to_database['rebalance_date'].iloc[0]
        rebalance_date = rebalance_date.strftime('%Y-%m-%d')

        markdown_text += f"📢 O usuário {username_existent} possui {number_of_assets} asset(s) na wallet_id = {rebalance_wallet_id}.\n\n Última atualização da carteira: {rebalance_date}\n"
        # await update.message.reply_text(read_setups_txt)

        for _, row in wallet_to_database.iterrows():

            ticker = row['ticker']
            wallet_proportion = row['wallet_proportion']
            wallet_proportion = round(wallet_proportion * 100,2)
            
            markdown_text += f"          ➡ {ticker}: {wallet_proportion}%\n"

        answer_text = markdown_text

        print(answer_text)

        return answer_text

    def create_nightvision_answer(wallet_id, final_analysis, last_analysis_date, weighted_average_returns):
        
        markdown_text = ''
        
        rebalance_date = final_analysis['data'].iloc[0]
        rebalance_date = rebalance_date.strftime('%Y-%m-%d')

        markdown_text += f"👓👓👓 NIGHTVISION! 👓👓👓\n\n"
        markdown_text += f"💼 wallet_id: {wallet_id} - data: {rebalance_date}\n"

        for _, row in final_analysis.iterrows():

            ticker = row['ticker']
            company_name = row['company_name']
            wallet_proportion = row['peso']
            sector = row['sector']
            subsector = row['subsector']
            last_period_variation = row['percentual_variation']
            last_period_variation = round(last_period_variation,2)
            last_growth_rate = row['last_growth_rate']
            last_growth_rate = round(last_growth_rate * 100,1)
            wallet_proportion = round(wallet_proportion * 100,2)
            initial_price = row['initial_price']
            max_update_price = row['max_update_price']
            
            markdown_text += f"----------------------------------------\n"
            if last_period_variation > 0:
                markdown_text += f"    🟢 {ticker}, rend: {last_period_variation}%\n"
            else:
                markdown_text += f"    🔴 {ticker}, rend: {last_period_variation}%\n"
            markdown_text += f"        ▪ Empresa: {company_name}\n"
            markdown_text += f"        ▪ Ramo: {sector} - {subsector}\n"
            markdown_text += f"        ▪ Peso do ativo na carteira: {wallet_proportion}%\n"
            markdown_text += f"        ▪ Crescimento da companhia no último ano: {last_growth_rate}%\n"
            markdown_text += f"        ▪ Preço dia {rebalance_date}: R$ {initial_price}\n"
            markdown_text += f"        ▪ Preço dia {last_analysis_date}: R$ {max_update_price}\n"

        if weighted_average_returns > 0:
            markdown_text += f"\n✅✅✅✅ GREEEEEN ✅✅✅✅\n\nA carteira está com um rendimento de {weighted_average_returns}% desde o último rebalanceamento ({rebalance_date}) até o dia {last_analysis_date}."
        else:
        
            markdown_text += f"\n❗❗❗❗ MANTÉM A ESTRATÉGIA ❗❗❗❗\nA carteira está com um rendimento de {weighted_average_returns}% desde o último rebalanceamento ({rebalance_date}) até o dia {last_analysis_date}.\n"
        
        answer_text = markdown_text

        return answer_text

    def create_delete_setup_answer(username_existent, setup_to_delete):

        if setup_to_delete.empty:

            answer_text = '💬 no setup to delete... 🤨'
            return answer_text
        else:
        
            markdown_text = ''
            wallet_id = setup_to_delete['wallet_id'].iloc[0]

            markdown_text += f"📢 O usuário {username_existent} solicitou a deleção do setup wallet_id= {wallet_id}. Configuração excluída abaixo: \n\n"
            # await update.message.reply_text(read_setups_txt)

            
            for _, group in setup_to_delete.groupby('wallet_id'):

                wallet_id = group['wallet_id'].iloc[0]
                rebalance_periods = group['rebalance_periods'].iloc[0]
                number_of_assets = group['number_of_assets'].iloc[0]
                create_date = group['create_date'].iloc[0]
                create_date = create_date.strftime('%Y-%m-%d')

                markdown_text += f"💼 wallet_id: {wallet_id}\n"
                markdown_text += f"---------------------------------------------\n"

                markdown_text += f"          ⚙ rebalance_periods: {rebalance_periods}\n          ⚙ number_of_assets: {number_of_assets}\n          ⚙ create_date: {create_date}\n"

                print(f"wallet_id: {wallet_id}")
                print(f"          rebalance_periods: {rebalance_periods}")
                print(f"          number_of_assets: {number_of_assets}")
                print(f"          create_date: {create_date}")

                for _, row in group.iterrows():

                    wallet_name = row['wallet_name']
                    indicators = [indicator for indicator in row[['indicator_1', 'indicator_2', 'indicator_3']] if pd.notna(indicator)]
                    
                    markdown_text += f"          🔶 {wallet_name}:\n"

                    print(f"          {wallet_name}:")
                    for indicator in indicators:
                        print(f"                             {indicator}")
                        markdown_text += f"                             🔹 {indicator}\n"
                    
                markdown_text += f"\n"

            answer_text = markdown_text

            return answer_text

    def create_read_portifolio_answer(username_existent, wallet_id, number_of_compositions, last_dates, compositions_df):

        markdown_text = ''

        if compositions_df.empty:

            answer_text = '💬 no portifolio existent... 🤨'
            return answer_text
        else:

            markdown_text += f"📢 O usuário {username_existent} solicitou o histórico de composições para o setup wallet_id= {wallet_id}."

            for date in last_dates:
                
                number_of_assets = len(compositions_df[compositions_df['rebalance_date'] == date])
                
                date = date.strftime('%Y-%m-%d')
                markdown_text += f" \n\n----------------------------------------\n🗓️ rebalance_date: {date}\n"

                for _, row in compositions_df.iterrows():
                    
                    if row['rebalance_date'].strftime('%Y-%m-%d') == date:
                        ticker = row['ticker']
                        wallet_proportion = row['wallet_proportion']
                        wallet_proportion = round(wallet_proportion * 100, 1)
                        
                        print(f"                             {ticker}")
                        markdown_text += f"        🔹 {ticker} - {wallet_proportion}%\n"
                        
                markdown_text += f"➡️ total of assets: {number_of_assets}"

            answer_text = markdown_text

        return answer_text

    def create_execute_rebalance_answer(wallet_id, rebalance_date, orders):
        
        execute_rebalance = True

        if len(orders) < 0:
            execute_rebalance = False

        markdown_text = ''
        
        if execute_rebalance:

            markdown_text = f'🧾🧾🧾 EXECUTION COMPLETE!! 🧾🧾🧾\n\nVocê solicitou o relatório de compra & venda referente a wallet_id = {wallet_id} para a data de rebalanceamento, rebalance_date = {rebalance_date}.\n\n'

            buy_orders = orders[orders['perc_variation'] > 0]
            sell_orders = orders[orders['perc_variation'] < 0]

            for _, row in orders.iterrows():

                ticker = row['ticker']
                wallet_proportion_actual = row['wallet_proportion_actual'] * 100
                perc_variation = row['perc_variation']
                wallet_proportion_previous = row['wallet_proportion_previous'] * 100
                perc_returns = row['perc_returns']
                rebalance_asset_price = row['rebalance_asset_price']
                previous_asset_price = row['previous_asset_price']
                previous_rebalance_date = row['previous_rebalance_date']

                markdown_text += f'--------------------\n'
                
                perc_variation = round(perc_variation,1)
                wallet_proportion_previous = round(wallet_proportion_previous,1)
                wallet_proportion_actual = round(wallet_proportion_actual,1)

                if ticker in list(buy_orders['ticker']):
                    markdown_text += f'⬅️ COMPRA: {ticker}\n'
                    markdown_text += f'     🔹 porcentagem de compra: {perc_variation}%\n'
                    markdown_text += f'     🔹 porcentagem anterior: {wallet_proportion_previous}%\n'
                    markdown_text += f'     🔹 porcentagem atual: {wallet_proportion_actual}%\n'
                elif ticker in list(sell_orders['ticker']):
                    markdown_text += f'➡️ VENDA: {ticker}\n'
                    markdown_text += f'     🔹 porcentagem de venda: {perc_variation}%\n'
                    markdown_text += f'     🔹 porcentagem anterior: {wallet_proportion_previous}%\n'
                    markdown_text += f'     🔹 porcentagem remanescente: {wallet_proportion_actual}%\n'
                    
                    if previous_asset_price !=0 and rebalance_asset_price != 0:
                        if perc_returns > 0:
                            markdown_text += f'     🟢 resultado do trade: {perc_returns}%\n'
                        else:
                            markdown_text += f'     🔴 resultado do trade: {perc_returns}%\n'
                        markdown_text += f'         🔸 preço de compra: R$ {previous_asset_price} ({previous_rebalance_date})\n'
                        markdown_text += f'         🔸 preço de venda: R$ {rebalance_asset_price}\n'
                    else:
                        markdown_text += f'         ⚠️ sem dados para avaliar o trade.\n'
        else:
                    
            markdown_text = f'🚧🚧🚧 Ordem inexistente! 🚧🚧🚧'
                    
        answer_text = markdown_text

        return answer_text

    def is_valid_date(date_str):
        
        try:
            final_analysis_date = pd.to_datetime(date_str)
            # final_analysis_date = final_analysis_date.strftime('%Y-%m-%d')
            return True
        except ValueError:
            return False
        
    def is_valid_integer(str):
        
        try:
            integer = int(str)
            # final_analysis_date = final_analysis_date.strftime('%Y-%m-%d')
            return True
        except ValueError:
            return False

    def is_valid_list(list_str):

        found_list = []

        # Padrão para identificar uma lista no texto (assumindo que seja algo entre colchetes [])
        list_pattern = r'\[.*?\]'

        is_integer_list = False
        is_string_list = False
        
        if list_str != None and isinstance(list_str, str):
            # Procura por padrões de lista no texto do comando
            found_lists = re.findall(list_pattern, list_str)
        else:
            found_lists = []
        
        size_found_lists = len(found_lists)

        if size_found_lists == 1:
            found_list = found_lists[0]
            
            size_found_list = len(found_list)
            print(size_found_list)
            
            # Verifica se pelo menos uma lista foi encontrada
            if found_lists:
                # Remove os colchetes e divide os elementos da lista
                elementos = re.findall(r'\b\w+\b', found_list)

                # Verifica se todos os elementos da lista são inteiros
                if all(elemento.isdigit() for elemento in elementos):
                    if size_found_list > 2:
                        found_list = found_list[1:-1]
                        elements_list = found_list.split(';')
                        found_list = [float(element_list) for element_list in elements_list]
                        found_list = [int(element_list) for element_list in found_list]
                        print(f"A lista {found_list} contém apenas inteiros.")
                        is_integer_list = True
                elif all(isinstance(elemento, str) for elemento in elementos):
                    if size_found_list > 2:
                        found_list = found_list[1:-1]
                        elements_list = found_list.split(';')
                        found_list = [str(element_list) for element_list in elements_list]
                        print(f"A lista {found_list} contém apenas strings.")
                        # found_list = ast.literal_eval(found_list)
                        is_string_list = True
                else:
                    print(f"A lista {found_list} contém uma mistura de inteiros e strings.")
            else:
                found_list = []
        else:
            print("O comando não contém uma lista válida.")

        return found_list, is_integer_list, is_string_list

###
##
#SLASH COMMANDS
##
###
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("/start executed")
    
    username: str = update.message.from_user.username
    first_name: str = update.message.from_user.first_name
    last_name: str = update.message.from_user.last_name
    print(f'name: {first_name} {last_name} - username: {username}')

    response_text = '''
**BORA COMEÇAR ???**

📣 Este BOT está conectado a aplicação FINAPP e eu sou seu intelocutor.
    
📈 Será aqui que realizaremos avaliações de indicadores fundamentalistas aplicando a técnica de Factor Investing para acompanhar a performance de ativos da classe de renda variável rentável mais rentável da história - ações!

🐭 Resumidamente com esse BOT será possível 1) avaliar e comparar a performance de rentabilidade de diferentes indicadores usando dados do mercado de ações brasileiro atualizados e com histórico de 10 anos e 2) salvar e gerir o resultado atual do acompanhamento do resultado de indicadores e/ou suas combinações através de setups.

🌎 *Jornada de Usuário*

    É importante deixar claro que todos os comandos aceitos pelo finapp-interlocutor estão contidos no /help, então caso tenha dúvidas não hesite em invocá-lo.

        1º- Necessário cadastro na base de dados Finapp usando o comando `save_username`. É obrigatório realizar o cadastro de Primeiro Nome, Último Nome e username na Aba de Configurações do Telegram.

        2º- Com o cadastro feito é possível rankear a performance dos prêmios de risco dos indicatores e/ou suas combinações (1a1, 2a2 e 3a3). Os indicadores que podem estar contidos dentro do parênteses do comando `rank_risk_premiuns()` podem ser vistos no comando /indicators.
        Você pode montar a estrutura desse comando copiando o comando no início do exemplo no /help e depois copiar os indicadores presentes no comando /indicators. Por exmplo, para avaliar a performance dos últimos 10 anos do indicador 'Momento 6 Meses' usa-se o comando:\n       📍 `rank_risk_premiuns(momento_6_meses)`

        Caso queira salvar um setup contendo as combinações que foram rankiadas & exibidas na mensagem, deve-se configurar a variável save_setup = True juntamente com a variável `premiuns_to_dict` que irá indicar quais posições do ranking estarão contidos no setup. Assim será criado um setup com um rebalanceamento de 21 dias e com 5 ativos para cada combinação. Importante notar que no final da mensagem de avaliação, caso seja escolhido salvar, será passado o `wallet_id` para ser usado como referência para próximos comandos.
        Exemplo para salvar o 1º e 3º lugar no ranking exibido considerando as combinações dos 3 indicadores informados:\n       📍 `rank_risk_premiuns(ValorDeMercado, momento_6_meses, p_vp_invert, save_setup=true, premiuns_to_dict=[1;3])`

        3º- Após salvar algum setup, você pode acessar os setups salvos pelo comando `read_setups`.

        4º- Para gerar um rebalanceamento de algum setup priamente configurado, você pode usar o comando `rebalance_setup(wallet_id=XXXX)` trocando o 'XXXX' pelo wallet_id desejado.

        5º- Para ter detalhes atualizados de algum setup, é possíval executar o comando `nightvision(wallet_id=XXXX)`. Será possível ver o resultado de cada ativo desde o último rebalanceamento com detalhes de cada ativo, além do resultado de todos os ativos juntos considerando as proporções.

        6º- Caso queira visualizar as últimas 3 composições de alguns setup, execute o comando `read_portifolio(wallet_id=XXXX)`.

        7º- Se optar por seguir a lista de ativos que representam algum setup previamente configurado, você pode usar o comando `execute_rebalance(wallet_id=XXXX)` para que o FINAPP te mostre o que precisa ser comprado e vendido para um rebalanceamento específico.
    
    💰💰💰
    '''
    response_text = response_text.replace('_', r'\_')
    response_text = response_text.replace('!', r'\!')
    response_text = response_text.replace('?', r'\?')
    response_text = response_text.replace(':', r'\:')
    response_text = response_text.replace('.', r'\.')
    response_text = response_text.replace('-', r'\-')
    response_text = response_text.replace('(', r'\(')
    response_text = response_text.replace(')', r'\)')
    response_text = response_text.replace('=', r'\=')
    response_text = response_text.strip()
    
    await update.message.reply_text(response_text, parse_mode='MarkdownV2')

async def indicators_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("/indicators executed")
    
    username: str = update.message.from_user.username
    first_name: str = update.message.from_user.first_name
    last_name: str = update.message.from_user.last_name
    print(f'name: {first_name} {last_name} - username: {username}')

    response_text = '''
    ⚙ **INDICATORS PAGE** ⚙

    Abaixo está a lista de todos os indicadores presentes hoje no FINAPP. Cada nome de indicador aparece no texto como copiável (só clicar) e possui uma breve descrição do indicador.

    💠 `ValorDeMercado`: Usado para se referir ao preço que o mercado está pagando por uma empresa.

    💠 `ROIC`: Mede a rentabilidade de dinheiro o que uma empresa é capaz de gerar em razão de todo o capital investido, incluindo os aportes por meio de dívidas.

    💠 `ROE`: Mede a capacidade de agregar valor de uma empresa a partir de seus próprios recursos e do dinheiro de investidores.

    💠 `EBIT_EV`: Este indicador mostra quanto tempo levaria para o valor calculado no EBIT pagar o investimento feito para comprá-la.

    💠 `L_P`: Dá uma ideia do quanto o mercado está disposto a pagar pelos lucros da companhia.

    💠 `net_margin`: Margem líquida da empresa.

    💠 `ebit_dl`: Proporção direta entre o EBIT e a Dívida Líquida da companhia. Quanto mais negativo, melhor.

    💠 `pl_db`: Proporção direta entre o Patrimônio Líquido e a Dívida Bruta de uma companhia.

    💠 `momento_1_meses`: Representa a média móvel do último mês dos retornos para cada ação.

    💠 `momento_6_meses`: Representa a média móvel dos últimos 6 meses dos retornos para cada ação.

    💠 `momento_12_meses`: Representa a média móvel dos últimos 12 meses dos retornos para cada ação.

    💠 `mm_7_40`: Representa a proporção (divisão) entre média móvel curta e média móvel longa.

    💠 `p_vp_invert`: Facilita a análise e comparação da relação do preço de negociação de um ativo e seu VPA (Valor Patrimonial por Ação).

    💠 `p_ebit_invert`: Indica qual é o preço da ação em relação as seu resultado EBIT. O EBIT pode ser considerado uma aproximação do lucro operacional da companhia.

    '''
    response_text = response_text.replace('_', r'\_')
    response_text = response_text.replace('!', r'\!')
    response_text = response_text.replace(':', r'\:')
    response_text = response_text.replace('.', r'\.')
    response_text = response_text.replace('-', r'\-')
    response_text = response_text.replace('=', r'\=')
    response_text = response_text.replace(')', r'\)')
    response_text = response_text.replace('(', r'\(')
    response_text = response_text.strip()

    await update.message.reply_text(response_text, parse_mode='MarkdownV2')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    print("/help executed")
    
    username: str = update.message.from_user.username
    first_name: str = update.message.from_user.first_name
    last_name: str = update.message.from_user.last_name
    print(f'name: {first_name} {last_name} - username: {username}')

    response_text = '''
💊
💊💊
💊💊💊
**Comandos**
💊💊💊
💊💊
💊

Os comandos mostrados abaixo podem ser executados diretamente na conversa com o bot quanto no grupo que o bot esteja. Para interagir com o bot em grupos, é necessário marcar o bot. 

✉ Para facilitar sua experiência, os comandos e seus exemplos são 'clicáveis'. Ou seja, clicou, copiou. 🎇 Quando um comando não tem parênteses, ele pode ser usado exatamente como está indicado no exemplo clicável.

----------------------------------------------
    💾 `save_username`: Realiza o cadastro do usuário na base do FINAPP, necessário para execuçãos dos outros comandos.
\n----------------------------------------------
    ⚖ `rank_risk_premiuns()`: Usado para realizar a avaliação de indicadores e/ou suas combinações. O comando trás como output uma mensagem contendo o resultado do rankeamento, gerando informações estatísticas relevantes para avaliação de performance dos indicadores. A avaliação é feita usando o método de janelas deslizantes e usamos janelas de 12 e 60 meses para rankeamento.\n
    exemplos:\n       📍`rank_risk_premiuns(momento_1_meses)`\n       📍`rank_risk_premiuns(momento_1_meses, save_setup = true)`\n       📍`rank_risk_premiuns(ROIC, mm_7_40, momento_6_meses, p_vp_invert,  premiuns_to_show=3, step_months_rank_list = [6;24;36], columns_rank_list = [profit_perc; anual_mean_acum_returns], premiuns_to_dict=[1;3], save_setup = false)`
\n----------------------------------------------
    📝 `read_setups`: Usado para visualização dos setups previamente configurados. vale resaltar que é possível salvar no máximo 5 setups diferntes.
\n----------------------------------------------
    ⚖ `rebalance_setup(wallet_id=XXXX)`: Após avaliação e definição do(s) setup(s), pelo comando `rank_risk_premiuns()` é possível gerar a lista de ativos que mais são representados pelos indicadores informado no corpo do comando (`wallet_id`).
\n----------------------------------------------
    👓 `nightvision(wallet_id=XXXX, rebalance_date=YYYY-MM-DD)`: Comando retorna uma mensagem contendo detalhes de cada ativo no setup indicada (`wallet_id`) para uma data de rebalanceamento específica, mostra retornos no período.
\n----------------------------------------------
    ❌ `delete_setup(wallet_id=XXXX)`: Usado para excluir um setup especificado (`wallet_id`).
\n----------------------------------------------
    🗓️ `read_portifolio(wallet_id=XXXX)`: Exibe as três últimas composições do setup especificado (`wallet_id`).
\n----------------------------------------------
    🧾 `execute_rebalance(wallet_id=XXXX, rebalance_date=YYYY-MM-DD)`: Exibe as ordens de compra & venda do setup especificado (`wallet_id`) para uma data de rebalanceamento específica (`rebalance_date`).
\n----------------------------------------------
    📊 `report_setup(wallet_id=XXXX)`: Gera um PDF com detalhes do setup especificado (`wallet_id`) para um histórico de utilização da estratégia desde jan-2020.

🔒
🔒🔒
*Comandos ADM*
🔒🔒
🔒

Comando possíveis de serem executados somente por administradores da plataforma, que são usados para carregamento de dados, criação de indicadores e cálculo de prêmios de risco.
----------------------------------------------
    📦 `update_database`: Usado para atualização da base de dados do FINAPP.
----------------------------------------------
    🧩 `make_indicators`: Usado para atualziação da base de dados de parte dos indicadores.
----------------------------------------------
    📖 `calculate_risk_premiuns()`: Usado para calcular os prêmios de risco dos indicadores e suas combinações.

    '''
# 💣💣💣 **Depreciado** 💣💣💣
#     ----------------------------------------------
#     ⚜ `rate_risk_premiuns()`: Rank selected indicators. You can send an optional attribut to save your setup with 'save_setup=True'. If you choose to save, Finapp will select the rank2 of combinations to create a setup with 2 wallets. Rebalance periods will be 21 and assets per wallet 5 (if the same asset is present in both wallets, it will receive more wallet proportion). You can use /indicators command to guide you.\n
#     examples:\n       📍`rate_risk_premiuns(momento_1_meses)`\n       📍`rate_risk_premiuns(momento_1_meses, save_setup = true)`
    
    response_text = response_text.replace('_', r'\_')
    response_text = response_text.replace('!', r'\!')
    response_text = response_text.replace(':', r'\:')
    response_text = response_text.replace('.', r'\.')
    response_text = response_text.replace('-', r'\-')
    response_text = response_text.replace('=', r'\=')
    response_text = response_text.replace(')', r'\)')
    response_text = response_text.replace('(', r'\(')
    response_text = response_text.strip()

    await update.message.reply_text(response_text, parse_mode='MarkdownV2')

async def deep_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    print("/deep executed")
    
    username: str = update.message.from_user.username
    first_name: str = update.message.from_user.first_name
    last_name: str = update.message.from_user.last_name
    print(f'name: {first_name} {last_name} - username: {username}')

    response_text = '''
💊

    '''
    
    response_text = response_text.replace('_', r'\_')
    response_text = response_text.replace('!', r'\!')
    response_text = response_text.replace(':', r'\:')
    response_text = response_text.replace('.', r'\.')
    response_text = response_text.replace('-', r'\-')
    response_text = response_text.replace('=', r'\=')
    response_text = response_text.replace(')', r'\)')
    response_text = response_text.replace('(', r'\(')
    response_text = response_text.strip()

    await update.message.reply_text(response_text, parse_mode='MarkdownV2')


###
##
#HANDLE MESSAGE
##
###
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    telegram_adm_id = os.getenv("TELEGRAM_ADM_ID")
    telegram_adm_id = str(telegram_adm_id)
    telegram_adm_id_list = telegram_adm_id
    # telegram_adm_id_list = list(telegram_adm_id)
    
    BOT_USERNAME = '@andretebar_bot'
    new_user = True
    adm_interaction             = False
    answer_in_group             = True
    fail_to_execute             = False
    enable_interaction          = True
    is_command                  = False
    all_indicators_existents    = False
    create_wallets_pfd          = False
    old_message                 = True
    answer_text                 = []
    max_window_size             = 120
    indicators_dict_database    = {
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
    columns_rank_database_list = ['profit_perc', 
                                  'anual_mean_acum_returns', 
                                  'anual_high_acum_returns', 
                                  'anual_low_acum_returns',
                                  'last_acum_return',
                                  'anual_std_dev_acum_returns']
    
    #ignoring old messages (older than 10 minutes)
    message_txt: str = update.message
    # print('message_txt: ', message_txt)
    date_txt: str = update.message.date
    # print('date_txt: ', date_txt)
    message_datetime = pd.to_datetime(date_txt)
    print('message_datetime: ', message_datetime)

    now = datetime.now(timezone.utc)
    time_threshold = now - timedelta(seconds=600)
    print('time_threshold: ', time_threshold)

    if (message_datetime > time_threshold):
        print('\nNew message!\n')
        old_message = False
    else:
        print('\nOld message, IGNORE!\n')

    message_type: str = update.message.chat.type
    # print('message_type: ', message_type)
    username: str = update.message.from_user.username
    print('username: ', username)
    id: str = update.message.from_user.id
    # print('id: ', id)
    first_name: str = update.message.from_user.first_name
    last_name: str = update.message.from_user.last_name
    print(f'name: {first_name} {last_name}')
    user_is_bot: str = update.message.from_user.is_bot
    # print('user_is_bot: ', user_is_bot)
    chat_id: str = update.message.chat_id
    print('chat_id: ', chat_id)

    if(username == None or first_name == None or last_name == None):
        enable_interaction = False
    print('enable_interaction: ', enable_interaction)

    telegram_user_manager = tum.TelegramUserManager()
    new_user_df = telegram_user_manager.prepare_telegram_user(user_id=id,username=username,first_name=first_name, last_name=last_name, is_bot=user_is_bot, is_adm=False)
    # print('new_user_df: \n', new_user_df)

    new_user, verifying_presence, username_existent, user_id_existent = telegram_user_manager.verify_telegram_user(new_user_df)
    # print(user_id_existent)
    # print(username_existent)

    #defining adm user
    if(user_id_existent in telegram_adm_id_list):
        adm_interaction = True

    text: str = update.message.text
    print(f'\n-> message from user ({username}) in {message_type}: "{text}"')

    user_text = text
    
    # parse text from groups
    if message_type == 'supergroup':
        if BOT_USERNAME in text:
            user_text: str = text.replace(BOT_USERNAME, '').strip()
            answer_in_group = True
        else:
            answer_in_group = False
    else:
        user_text = text

    # decode commands
    decoded_command_dict, decoded_indicators_list, decoded_variables_list = TelegramManager.decode_command(user_text)
    print('\ndecoded_command_dict: ', decoded_command_dict)
    decoded_command = decoded_command_dict['command']
    print('\ndecoded_command: ', decoded_command)
    print('\ndecoded_indicators_list: ', decoded_indicators_list)
    print('\ndecoded_variables_list: ', decoded_variables_list)
    
    # flag if it's a command
    if(decoded_command != 'unknown'):
        is_command = True

    # verify indicators and variables
    if len(decoded_indicators_list) > 0:
        
        
        indicators_database_list = list(indicators_dict_database.keys())
        print('\nindicators_database_list: ', indicators_database_list)

        all_indicators_existents = all(elemento in indicators_database_list for elemento in decoded_indicators_list)
        # print(all_indicators_existents)

        if(all_indicators_existents == False):
            fail_to_execute = True
    elif len(decoded_variables_list) > 0:
        
        all_indicators_existents = False

        if(all_indicators_existents == False):
            fail_to_execute = True
    
    single_combinations     = True
    double_combinations     = True
    triple_combinations     = True
    list_combinations = []
    premium_dataframe = pd.DataFrame()
    
    print('\nall_indicators_existents: ', all_indicators_existents)

    # verifying commands
    if (decoded_command != 'unknown' and answer_in_group):

        if(decoded_command == 'save_username'):
            fail_to_execute = False

            if message_type == 'supergroup':
                if answer_in_group:
                    await update.message.reply_text("Ok.")
            else:
                await update.message.reply_text("Ok.")

            if(new_user and enable_interaction):
                username_existent = username
                telegram_user_manager.insert_telegram_user(new_user_df)

        if(decoded_command == 'update_database' and adm_interaction):
            fail_to_execute = False

            if message_type == 'supergroup':
                if answer_in_group:
                    await update.message.reply_text("Ok.")
            else:
                await update.message.reply_text("Ok.")

            TelegramManager.update_database_command()
        
        if(decoded_command == 'make_indicators' and adm_interaction):
            fail_to_execute = False

            if message_type == 'supergroup':
                if answer_in_group:
                    await update.message.reply_text("Ok.")
            else:
                await update.message.reply_text("Ok.")

            TelegramManager.make_indicators_command()    

        if(decoded_command == 'calculate_risk_premiuns' and adm_interaction and all_indicators_existents):

            if message_type == 'supergroup':
                if answer_in_group:
                    await update.message.reply_text("Ok.")
            else:
                await update.message.reply_text("Ok.")

            update_existing_file    = False

            indicators_dict = {chave: indicators_dict_database[chave] for chave in decoded_indicators_list if chave in indicators_dict_database}
            # print(indicators_dict)

            ## rule to execute calculation of risk premiuns
            if ((len(indicators_dict) == len(decoded_indicators_list)) and len(decoded_variables_list) == 0):
                
                list_combinations, premium_dataframe = TelegramManager.calculate_risk_premiuns_command(indicators_dict, single_combinations, double_combinations, triple_combinations, 
                                                            update_existing_file)
                
                
                # if rating_failed:
                #     fail_to_execute = True
                # else:
                print(list_combinations)
                
                number_of_combinations = len(list_combinations)
                calculation_txt = f"✏ Foram calculadas {number_of_combinations} prêmios de risco atrealado as combinações montadas a partir dos indicadores presentes no comando.\n\n🗯 Lembrando que os cálculos são feitos considerando combinações tomadas 1a1, 2a2 e 3a3. Exemplo: {list_combinations[0]}"
                await update.message.reply_text(calculation_txt)

            else:
                fail_to_execute = True

        if(decoded_command == 'rate_risk_premiuns' and all_indicators_existents):
            
            if message_type == 'supergroup':
                if answer_in_group:
                    await update.message.reply_text("Ok.")
            else:
                await update.message.reply_text("Ok.")

            rating_premiuns_file_name       = r'..\\PDFs\rating-INDICATORS.pdf'

            save_setup = False
            create_pdf = False
            final_analysis_date = '2022-12-31'
            
            #verificar se as variaveis estão corretas
            decoded_variables_split_list = [(item.split('=')[0], item.split('=')[1]) for item in decoded_variables_list]
            # print(decoded_variables_split_list)

            for variable, value in decoded_variables_split_list:
                print(f"Variable: {variable}, Value: {value}")
                if variable == 'save_setup':
                    if value.lower() == 'true':
                        save_setup = True
                    elif value.lower() == 'false':
                        save_setup = False
                    else:
                        fail_to_execute = True
                elif variable == 'start_date':
                    final_analysis_date = value
                    if TelegramManager.is_valid_date(value):
                        final_analysis_date = pd.to_datetime(final_analysis_date)
                        final_analysis_date = final_analysis_date.strftime('%Y-%m-%d')
                        print(f"{final_analysis_date} DATA VÁLIDA.")
                    else:
                        validation_txt = f"({final_analysis_date}) não é uma data válida no formato esperado."
                        print(validation_txt)
                        await update.message.reply_text(validation_txt)
                        fail_to_execute = True
                elif variable == 'create_pdf':
                    if value.lower() == 'true':
                        create_pdf = True
                    elif value.lower() == 'false':
                        create_pdf = False
                    else:
                        fail_to_execute = True
                else:
                    fail_to_execute = True

            if fail_to_execute == False:

                indicators_dict = {chave: indicators_dict_database[chave] for chave in decoded_indicators_list if chave in indicators_dict_database}

                distribution_indicadors, ranking_indicator, top_indicators, setup_dict, fail_to_execute = TelegramManager.rate_risk_premiuns_command(indicators_dict, 
                                                                                    single_combinations=single_combinations, double_combinations=double_combinations, triple_combinations=triple_combinations, 
                                                                                    create_rating_pdf=create_pdf, 
                                                                                    final_analysis_date=final_analysis_date)
                if fail_to_execute == False:
                    print('\nsetup_dict: ', setup_dict)
                    print('\ndistribution_indicadors: \n', distribution_indicadors)
                    print('\nranking_indicator: \n', ranking_indicator)
                    print('\ntop_indicators: \n', top_indicators)

                    # save_setup = bool(save_setup)
                    print('\nsave_setup: ', save_setup)
                    wallet_id = None
                    wallet_existent = None 
                    wallets_df = None
                    if save_setup:
                        print('\nPODE SALVAR!!\n')

                        wallet_manager = wm.WalletManager()

                        file_not_found, wallets_df = wallet_manager.read_setups(username_existent)

                        print('\nwallets_df: ', wallets_df)
                        
                        number_of_wallets = wallets_df['wallet_id'].nunique()
                        number_of_wallets = int(number_of_wallets)
                        
                        print('\nnumber_of_wallets: ', number_of_wallets)

                        if number_of_wallets < 3:
                            create_date_auto = datetime.now()
                            create_date_auto = create_date_auto.strftime('%Y-%m-%d')

                            # receber os parametros number_of_assets & rebalance_periods do comando!!!
                            new_setup_to_insert = wallet_manager.preparing_setup_data(setups_dict = setup_dict, number_of_assets = 5, rebalance_periods = 21, user_name = username_existent, create_date = create_date_auto)

                            wallet_id, wallet_existent = wallet_manager.insert_setup(wallet_manager = wallet_manager, new_setup = new_setup_to_insert)
                            
                            # answer_text = TelegramManager.create_rating_answer(distribution_indicadors, ranking_indicator, top_indicators, setup_dict, indicators_dict_database,
                            #                                         save_setup, wallet_id, wallet_existent, wallets_df)
                            # print('\nanswer_text: \n', answer_text)
                        else:
                            answer_text = '💬 setup limit exceed... 🤨'
                        
                    else:
                        print('\nNÃO PODE SALVAR!!\n')
                    
                    answer_text = TelegramManager.create_rating_answer(distribution_indicadors, ranking_indicator, top_indicators, setup_dict, indicators_dict_database,
                                                                                        save_setup, wallet_id, wallet_existent, wallets_df)
                    
                    # create_pdf = bool(create_pdf)
                    print('create_pdf: ', create_pdf)
                    if create_pdf:
                        print('\nPODE CRIAR O PDF!!\n')
                    else:
                        print('\nNÃO PODE CRIAR O PDF!!\n')
                    
                else:
                    await update.message.reply_text("🚧 tente calcular os prêmios antes de avaliá-los.")

        if(decoded_command == 'rank_risk_premiuns' and all_indicators_existents):
            
            if message_type == 'supergroup':
                if answer_in_group:
                    await update.message.reply_text("Ok.")
            else:
                await update.message.reply_text("Ok.")

            rating_premiuns_file_name   = r'..\\PDFs\rating-INDICATORS.pdf'

            save_setup                  = False
            premiuns_to_dict            = [1]
            step_months_rank_list       = [12, 60]
            premiuns_to_show            = 3
            columns_rank_list           = ['anual_mean_acum_returns' , 'profit_perc']
            create_pdf                  = False
            initial_analysis_date       = '2012-01-31'
            final_analysis_date         = '2024-01-31'
            append_text = ''
            
            #verificar se as variaveis estão corretas

            decoded_variables_split_list = [(item.split('=')[0], item.split('=')[1]) for item in decoded_variables_list]
            print('\ndecoded_variables_split_list: \n', decoded_variables_split_list)

            for variable, value in decoded_variables_split_list:

                variable = str(variable)

                print(f"Variable: {variable}, Value: {value}")

                if variable == 'save_setup':
                    if value.lower() == 'true':
                        save_setup = True
                        print(f"variável é booleana = {save_setup}")
                    elif value.lower() == 'false':
                        save_setup = False
                        print(f"variável é booleana = {save_setup}")
                    else:
                        print(f"variável não é booleana = {save_setup}")
                        fail_to_execute = True
                elif variable == 'start_date':
                    initial_analysis_date = value
                    if TelegramManager.is_valid_date(value):
                        initial_analysis_date = pd.to_datetime(initial_analysis_date)
                        initial_analysis_date = initial_analysis_date.strftime('%Y-%m-%d')
                        print(f"{initial_analysis_date} DATA VÁLIDA.")
                    else:
                        validation_txt = f"({initial_analysis_date}) não é uma data válida no formato esperado."
                        print(validation_txt)
                        await update.message.reply_text(validation_txt)
                        fail_to_execute = True
                elif variable == 'end_date':
                    final_analysis_date = value
                    if TelegramManager.is_valid_date(value):
                        final_analysis_date = pd.to_datetime(final_analysis_date)
                        final_analysis_date = final_analysis_date.strftime('%Y-%m-%d')
                        print(f"{final_analysis_date} DATA VÁLIDA.")
                    else:
                        validation_txt = f"({final_analysis_date}) não é uma data válida no formato esperado."
                        print(validation_txt)
                        await update.message.reply_text(validation_txt)
                        fail_to_execute = True
                # elif variable == 'create_pdf':
                #     if value.lower() == 'true':
                #         create_pdf = True
                #     elif value.lower() == 'false':
                #         create_pdf = False
                #     else:
                #         fail_to_execute = True
                elif variable == 'premiuns_to_show':
                    possib_int = value
                    if TelegramManager.is_valid_integer(possib_int):
                        premiuns_to_show = int(possib_int)
                        print(f"{possib_int} integer.")
                    else:
                        print(f"{possib_int} não é integer.")
                        fail_to_execute = True
                elif variable == 'step_months_rank_list':
                    possib_list = value
                    # print('possib_list: \n', possib_list)
                    found_list, is_integer_list, is_string_list = TelegramManager.is_valid_list(possib_list)
                    
                    if is_integer_list:
                        all_selected_premiuns_range = all(max_window_size >= elemento for elemento in found_list)
                        
                        if all_selected_premiuns_range:
                            step_months_rank_list = found_list
                            print(f"a lista contém somente integer.")
                        else:
                            fail_to_execute = True
                    else:
                        print(f"a lista não contém somente integer.")
                        fail_to_execute = True
                elif variable == 'columns_rank_list':
                    possib_list = value
                    found_list, is_integer_list, is_string_list = TelegramManager.is_valid_list(possib_list)

                    all_variables_present = all(elem in columns_rank_database_list for elem in found_list)

                    if all_variables_present:
                        if is_string_list:
                            columns_rank_list = found_list
                            print(f"a lista contém somente strings.")
                        else:
                            print(f"a lista não contém somente strings.")
                            fail_to_execute = True
                    else:
                        fail_to_execute = True
                elif variable == 'premiuns_to_dict':
                    possib_list = value
                    found_list, is_integer_list, is_string_list = TelegramManager.is_valid_list(possib_list)

                    if is_integer_list:
                        all_selected_positions_range = all(premiuns_to_show >= elemento for elemento in found_list)
                        if all_selected_positions_range:
                            premiuns_to_dict = found_list
                            print(f"a lista contém somente integer.")
                        else:
                            fail_to_execute = True
                    else:
                        print(f"a lista não contém somente integer.")
                        fail_to_execute = True
                else:
                    fail_to_execute = True

            if fail_to_execute == False:

                indicators_dict = {chave: indicators_dict_database[chave] for chave in decoded_indicators_list if chave in indicators_dict_database}
                print('indicators_dict: \n', indicators_dict)

                premiuns_statistics_to_show, analyzed_windows_df, combined_min_data_inicial, data_inicial, combined_max_data_final, data_final, setup_dict, single_indicator_count, single_indicators_total_count, pairs_indicator_count, pair_indicators_total_count = TelegramManager.rank_risk_premiuns_command(indicators_dict, 
                                                                                    single_combinations=single_combinations, double_combinations=double_combinations, triple_combinations=triple_combinations, 
                                                                                    create_rating_pdf=create_pdf, 
                                                                                    initial_analysis_date = initial_analysis_date, final_analysis_date=final_analysis_date,
                                                                                    step_months_rank_list=step_months_rank_list, 
                                                                                    columns_rank_database_list=columns_rank_database_list, columns_rank_list=columns_rank_list, 
                                                                                    premiuns_to_dict=premiuns_to_dict, premiuns_to_show=premiuns_to_show)

                if fail_to_execute == False:

                    print('\ncombined_min_data_inicial: ', combined_min_data_inicial)
                    print('\ncombined_max_data_final: ', combined_max_data_final)
                    print('\ndata_inicial: ', data_inicial)
                    print('\ndata_final: ', data_final)
                    # print('\npremiuns_statistics_to_show: \n', premiuns_statistics_to_show)
                    # print('\nnumber_of_analysed_windows: \n', number_of_analysed_windows)
                    print('\nsetup_dict: \n', setup_dict)
                    print('\nsave_setup: ', save_setup)

                    wallet_id = None
                    wallet_existent = None 
                    wallets_df = None

                    if save_setup:
                        print('\nPODE SALVAR!!\n')

                        wallet_manager = wm.WalletManager()

                        file_not_found, wallets_df = wallet_manager.read_setups(username_existent)

                        print('\nwallets_df: \n', wallets_df)
                        
                        number_of_wallets = wallets_df['wallet_id'].nunique()
                        number_of_wallets = int(number_of_wallets)
                        
                        print('\nnumber_of_wallets: ', number_of_wallets)

                        if number_of_wallets < 5:
                            create_date_auto = datetime.now()
                            create_date_auto = create_date_auto.strftime('%Y-%m-%d')

                            # receber os parametros number_of_assets & rebalance_periods do comando!!!
                            new_setup_to_insert = wallet_manager.preparing_setup_data(setups_dict = setup_dict, number_of_assets = 5, rebalance_periods = 21, user_name = username_existent, create_date = create_date_auto)

                            wallet_id, wallet_existent, validation_df, setup_duplicated = wallet_manager.insert_setup(wallet_manager = wallet_manager, new_setup = new_setup_to_insert)
                            
                            append_text = TelegramManager.create_read_setups_answer(username_existent, validation_df)

                            print('\nappend_text: \n', append_text)
                        else:
                            append_text = '💬 setup limit exceed... 🤨'
                            print('\nappend_text: \n', append_text)
                        
                    else:
                        print('\nNÃO PODE SALVAR!!\n')
                    
                    ranking_header_answer = TelegramManager.create_ranking_header_answer(premiuns_statistics_to_show, step_months_rank_list, analyzed_windows_df, 
                                                                                    columns_rank_list, data_inicial, data_final)
                    await update.message.reply_text(ranking_header_answer)

                    ranking_text = TelegramManager.create_ranking_answer(premiuns_to_show, premiuns_to_dict, columns_rank_list, step_months_rank_list, 
                                                                        premiuns_statistics_to_show, setup_dict, 
                                                                        indicators_dict_database, save_setup, wallet_id, wallet_existent, wallets_df,
                                                                        analyzed_windows_df,
                                                                        append_text)
                    await update.message.reply_text(ranking_text)

                    indicator_count_answer = TelegramManager.create_indicator_count_answer(single_indicator_count, single_indicators_total_count, premiuns_statistics_to_show)
                    await update.message.reply_text(indicator_count_answer)

                    pair_indicator_count_answer = TelegramManager.create_pair_indicator_count_answer(pairs_indicator_count, pair_indicators_total_count)
                    await update.message.reply_text(pair_indicator_count_answer)
                    
                    answer_text = '🛫 obrigado.'
                    
                    # create_pdf = bool(create_pdf)
                    print('create_pdf: ', create_pdf)
                    if create_pdf:
                        print('\nPODE CRIAR O PDF!!\n')
                    else:
                        print('\nNÃO PODE CRIAR O PDF!!\n')
                    
                else:
                    await update.message.reply_text("🚧 tente calcular os prêmios antes de avaliá-los.")

        if(decoded_command == 'read_setups'):
            
            if message_type == 'supergroup':
                if answer_in_group:
                    await update.message.reply_text("Ok.")
            else:
                await update.message.reply_text("Ok.")

            wallets_df = TelegramManager.read_setups_command(username_existent)
            
            if wallets_df.empty:
                answer_text = '💬 inexistent wallets setup... 🤨'
            else:
                answer_text = TelegramManager.create_read_setups_answer(username_existent, wallets_df)

        if(decoded_command == 'rebalance_setup' and (len(decoded_indicators_list) == 0 and len(decoded_variables_list) == 1) ):
            fail_to_execute = False

            if message_type == 'supergroup':
                if answer_in_group:
                    await update.message.reply_text("Ok.")
            else:
                await update.message.reply_text("Ok.")

            rebalance_wallet_id = '0000'
            rebalance_calc_end_date = '2024-12-31'
            factor_calc_initial_date = '2019-12-31'
            liquidity_filter = 1
            wallet_to_database = pd.DataFrame()

            #verificar se as variaveis estão corretas
            decoded_variables_split_list = [(item.split('=')[0], item.split('=')[1]) for item in decoded_variables_list]
            # print(decoded_variables_split_list)

            for variable, value in decoded_variables_split_list:
                print(f"Variable: {variable}, Value: {value}")
                if variable == 'wallet_id':
                    possib_int = value
                    if TelegramManager.is_valid_integer(possib_int):
                        rebalance_wallet_id = str(possib_int)
                        print(f"{possib_int} integer.")
                    else:
                        print(f"{possib_int} não é integer.")
                        fail_to_execute = True
                else:
                    fail_to_execute = True

            if fail_to_execute == False: 
            
                wallet_to_database = TelegramManager.rebalance_setup_command(rebalance_wallet_id=rebalance_wallet_id, 
                                                        rebalance_calc_end_date=rebalance_calc_end_date, 
                                                        indicators_dict_database=indicators_dict_database,
                                                        factor_calc_initial_date=factor_calc_initial_date,
                                                        liquidity_filter=liquidity_filter)
                
                if wallet_to_database.empty:
                    answer_text = f"❌ Setup inexistente! ❌"
                else:
                    answer_text = TelegramManager.create_rebalance_setup_answer(username_existent, rebalance_wallet_id, wallet_to_database)

        if(decoded_command == 'nightvision' and (len(decoded_indicators_list) == 0 and len(decoded_variables_list) == 2) ):
            fail_to_execute = False

            if message_type == 'supergroup':
                if answer_in_group:
                    await update.message.reply_text("Ok.")
            else:
                await update.message.reply_text("Ok.")

            wallet_id = '0000'

            #verificar se as variaveis estão corretas
            decoded_variables_split_list = [(item.split('=')[0], item.split('=')[1]) for item in decoded_variables_list]
            # print(decoded_variables_split_list)

            for variable, value in decoded_variables_split_list:
                print(f"Variable: {variable}, Value: {value}")
                if variable == 'wallet_id':
                    possib_int = value
                    if TelegramManager.is_valid_integer(possib_int):
                        wallet_id = str(possib_int)
                        print(f"{possib_int} integer.")
                    else:
                        print(f"{possib_int} não é integer.")
                        fail_to_execute = True
                elif variable == 'rebalance_date':
                    rebalance_date = value
                    if TelegramManager.is_valid_date(value):
                        rebalance_date = pd.to_datetime(rebalance_date)
                        rebalance_date = rebalance_date.strftime('%Y-%m-%d')
                        print(f"{rebalance_date} DATA VÁLIDA.")
                    else:
                        validation_txt = f"({rebalance_date}) não é uma data válida no formato esperado."
                        print(validation_txt)
                        # await update.message.reply_text(validation_txt)
                        fail_to_execute = True
                else:
                    fail_to_execute = True

            if fail_to_execute:
                answer_text = ''
            else:

                final_analysis, next_rebalance_date, weighted_average_returns = TelegramManager.nightvision_command(wallet_id, rebalance_date)

                if final_analysis.empty:
                    answer_text = '⚠️ nenhuma composição para essa data de rebalanceamento! '
                else:

                    weighted_average_returns = round(weighted_average_returns,2)

                    next_rebalance_date = next_rebalance_date.strftime('%Y-%m-%d')
                    
                    answer_text = TelegramManager.create_nightvision_answer(wallet_id, final_analysis, next_rebalance_date, weighted_average_returns)

                    print('\nfinal_analysis: \n',final_analysis)
                    print('\nfinal_analysis.columns: \n',final_analysis.columns)
                    print('\nnext_rebalance_date: ',next_rebalance_date)
                    print('\nweighted_average_returns: ',weighted_average_returns)

        if(decoded_command == 'delete_setup' and (len(decoded_indicators_list) == 0 and len(decoded_variables_list) == 1) ):
            fail_to_execute = False

            if message_type == 'supergroup':
                if answer_in_group:
                    await update.message.reply_text("Ok.")
            else:
                await update.message.reply_text("Ok.")

            wallet_id = '0000'
            setup_to_delete = pd.DataFrame()

            #verificar se as variaveis estão corretas
            decoded_variables_split_list = [(item.split('=')[0], item.split('=')[1]) for item in decoded_variables_list]
            # print(decoded_variables_split_list)

            for variable, value in decoded_variables_split_list:
                print(f"Variable: {variable}, Value: {value}")
                if variable == 'wallet_id':
                    possib_int = value
                    if TelegramManager.is_valid_integer(possib_int):
                        wallet_id = str(possib_int)
                        print(f"{possib_int} integer.")
                    else:
                        print(f"{possib_int} não é integer.")
                        fail_to_execute = True
                else:
                    fail_to_execute = True

            setup_to_delete = TelegramManager.delete_setup_command(wallet_id, username_existent)

            answer_text = TelegramManager.create_delete_setup_answer(username_existent, setup_to_delete)

        if(decoded_command == 'read_portifolio' and (len(decoded_indicators_list) == 0 and len(decoded_variables_list) == 1) ):

            fail_to_execute = False

            if message_type == 'supergroup':
                if answer_in_group:
                    await update.message.reply_text("Ok.")
            else:
                await update.message.reply_text("Ok.")

            wallet_id = '0000'

            #verificar se as variaveis estão corretas
            decoded_variables_split_list = [(item.split('=')[0], item.split('=')[1]) for item in decoded_variables_list]
            # print(decoded_variables_split_list)

            for variable, value in decoded_variables_split_list:
                print(f"Variable: {variable}, Value: {value}")
                if variable == 'wallet_id':
                    possib_int = value
                    if TelegramManager.is_valid_integer(possib_int):
                        wallet_id = str(possib_int)
                        print(f"{possib_int} integer.")
                    else:
                        print(f"{possib_int} não é integer.")
                        fail_to_execute = True
                else:
                    fail_to_execute = True

            number_of_compositions, last_dates, compositions_df = TelegramManager.read_portifolio_command(wallet_id)

            answer_text = TelegramManager.create_read_portifolio_answer(username_existent, wallet_id, number_of_compositions, last_dates, compositions_df)

        if(decoded_command == 'execute_rebalance' and (len(decoded_indicators_list) == 0 and len(decoded_variables_list) == 2) ):

            fail_to_execute = False

            wallet_id = 0000
            rebalance_date = '1992-08-12'
            rebalance_date = pd.to_datetime(rebalance_date)
            rebalance_date = rebalance_date.strftime('%Y-%m-%d')

            #verificar se as variaveis estão corretas
            decoded_variables_split_list = [(item.split('=')[0], item.split('=')[1]) for item in decoded_variables_list]
            print('\ndecoded_variables_split_list: \n', decoded_variables_split_list)

            for variable, value in decoded_variables_split_list:

                variable = str(variable)

                print(f"Variable: {variable}, Value: {value}")

                if variable == 'rebalance_date':
                    rebalance_date = value
                    if TelegramManager.is_valid_date(value):
                        rebalance_date = pd.to_datetime(rebalance_date)
                        rebalance_date = rebalance_date.strftime('%Y-%m-%d')
                        print(f"{rebalance_date} DATA VÁLIDA.")
                    else:
                        validation_txt = f"({rebalance_date}) não é uma data válida no formato esperado."
                        print(validation_txt)
                        # await update.message.reply_text(validation_txt)
                        fail_to_execute = True
                elif variable == 'wallet_id':
                    possib_int = value
                    if TelegramManager.is_valid_integer(possib_int):
                        wallet_id = int(possib_int)
                        print(f"{wallet_id} integer.")
                    else:
                        print(f"{wallet_id} não é integer.")
                        fail_to_execute = True
                else:
                    fail_to_execute = True

            orders = pd.DataFrame()
            
            orders = TelegramManager.execute_rebalance_command(wallet_id, rebalance_date)
            print('orders: \n', orders)

            # answer_text = 'execute_rebalance default answer'
            answer_text = TelegramManager.create_execute_rebalance_answer(wallet_id, rebalance_date, orders)

        if(decoded_command == 'report_setup' and (len(decoded_indicators_list) == 0 and len(decoded_variables_list) == 1) ):
            fail_to_execute = False

            if message_type == 'supergroup':
                if answer_in_group:
                    await update.message.reply_text("Ok.")
            else:
                await update.message.reply_text("Ok.")

            wallet_id = '0000'

            #verificar se as variaveis estão corretas
            decoded_variables_split_list = [(item.split('=')[0], item.split('=')[1]) for item in decoded_variables_list]
            # print(decoded_variables_split_list)

            for variable, value in decoded_variables_split_list:
                print(f"Variable: {variable}, Value: {value}")
                if variable == 'wallet_id':
                    possib_int = value
                    if TelegramManager.is_valid_integer(possib_int):
                        wallet_id = str(possib_int)
                        print(f"{possib_int} integer.")
                    else:
                        print(f"{possib_int} não é integer.")
                        fail_to_execute = True
                else:
                    fail_to_execute = True

            if fail_to_execute:
                answer_text = ''
            else:
                pdf_name = TelegramManager.report_setup_command(wallet_id, username_existent, indicators_dict_database)
                print('\npdf_name: ', pdf_name)

                project_folder = os.getenv("PROJECT_FOLDER")
                path_to_pdf = os.getenv("INDICATORS_FOLDER")
                print('\npath_to_pdf: ', path_to_pdf)

                full_path = os.path.join(project_folder,path_to_pdf,pdf_name)
                print('\nfull_path: ', full_path)

                # Envie o PDF para o usuário ou grupo
                with open(full_path, 'rb') as pdf_file:
                    await update.message.reply_document(pdf_file)
                
                answer_text = '✅ arquivo enviado com sucesso.'

    # defining when bot aswer
    if old_message == False:
        if message_type == 'supergroup':
            if answer_in_group:
                response: str = TelegramManager.handle_responses(answer_text, user_text, username_existent, new_user, adm_interaction, fail_to_execute, enable_interaction, is_command)
            else:
                return
        else:
            response: str = TelegramManager.handle_responses(answer_text, text, username_existent, new_user, adm_interaction, fail_to_execute, enable_interaction, is_command)

        print('\n--> BOT responds: \n', response)

        await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error_txt = f'Execution caused error -> {context.error}'
    await update.message.reply_text(error_txt)
    print(f'Update {update} caused error {context.error}')


#
## MAIN
#
if __name__ == "__main__":

    telegram_manager = TelegramManager()

    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_token = str(telegram_token)

    telegram_adm_id = os.getenv("TELEGRAM_ADM_ID")
    telegram_adm_id = str(telegram_adm_id)

    app = Application.builder().token(telegram_token).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('indicators', indicators_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors°
    app.add_error_handler(error)

    # polls the bot
    print('polling...\n')
    # app.run_polling(poll_interval = 3)

    # Iniciar o bot em um thread separado
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(app.run_polling(poll_interval = 3))