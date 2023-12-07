import finapp_controller as fc
import telegram_user_manager as tum
import wallet_manager as wm

import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from io import StringIO
from datetime import datetime
import time
import re
import ast
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
                
            if adm_interaction:
                if 'update_database' in processed_text:
                    return '📥 database updated! 📥'
                if 'read_setups' in processed_text:
                    return '😶😶😶'
                if 'calculate_risk_premiuns' in processed_text:
                    return '✏ calculation complete! ✏'
                if 'rate_risk_premiuns' in processed_text:
                    return f'🏆 rating complete! 🏆\n\n {answer_text}'
                if 'rebalance_setup' in processed_text:
                    return '🤠🤠🤠'
            else:
                return '🍰 command only for adms! 🍰'
            
            return 'invalid command'
        elif(is_command and fail_to_execute == True):
            return '💬 execution error! verify command... 🤨'

        if 'hello' in processed_text:
            return 'i see you!!'
        else:
            return 'Use o comando /help para te guiar quais os tipos de mensagens eu respondo.'
    
    ###
    ##
    #update_database
    ##
    ###   
    def update_database_command():
        
        finapp = fc.FinappController()
        
        # enable database update
        update_database                 = True
        update_api_database             = False
        update_fintz_database           = True
        update_webscrapping_database    = False


        fintz_demonstration_list = [
                                    'AcoesEmCirculacao', 'TotalAcoes',
                                    'PatrimonioLiquido',
                                    'LucroLiquido12m', 'LucroLiquido',
                                    'ReceitaLiquida', 'ReceitaLiquida12m', 
                                    'DividaBruta', 'DividaLiquida',
                                    'Disponibilidades', 
                                    'Ebit', 'Ebit12m',
                                    'Impostos', 'Impostos12m',
                                    'LucroLiquidoSociosControladora',
                                    'LucroLiquidoSociosControladora12m'
                                    ]

        fintz_indicators_list = [
                                'L_P', 'ROE', 'ROIC', 'EV', 'LPA', 'P_L', 'EBIT_EV', 'ValorDeMercado'
                                ]
        
        bc_dict = {
                    'selic':    {'bc_code': '432'},
                    'ipca':     {'bc_code': '433'},
                    'dolar':    {'bc_code': '1'},
                    }

        if(update_database):

            finapp.run_update_database(update_fintz_database = update_fintz_database, update_api_database = update_api_database, update_webscrapping_database = update_webscrapping_database,
                                    fintz_indicators_list = fintz_indicators_list, fintz_demonstration_list = fintz_demonstration_list,
                                    bc_dict = bc_dict)
   
    ###
    ##
    #calculate_risk_premiuns   
    ##
    ###
    def calculate_risk_premiuns_command(indicators_dict, single_combinations, double_combinations, triple_combinations, update_existing_file):
        
        list_combinations = []
        premium_dataframe = pd.DataFrame()

        finapp = fc.FinappController()
        
        list_combinations, premium_dataframe = finapp.run_calculate_risk_premiuns(indicators_dict=indicators_dict, 
                                                    single_combinations=single_combinations, double_combinations=double_combinations, triple_combinations=triple_combinations, 
                                                    update_existing_file=update_existing_file)
        
        return list_combinations, premium_dataframe

    ###
    ##
    # rate_risk_premiuns   
    ##
    ###
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

    ###
    ##
    # rebalance_setups
    ##
    ###
    def rebalance_setup_command(rebalance_wallet_id, rebalance_calc_end_date, indicators_dict_database, factor_calc_initial_date, liquidity_filter):
        
        finapp = fc.FinappController()

        wallet_to_database = pd.DataFrame()

        print(rebalance_wallet_id)
        print(rebalance_calc_end_date)
        print(indicators_dict_database)
        print(factor_calc_initial_date)
        print(liquidity_filter)
        print(wallet_to_database)

        wallet_to_database = finapp.run_rebalance_setups(rebalance_wallet_id=rebalance_wallet_id, 
                                                         rebalance_calc_end_date=rebalance_calc_end_date, 
                                                         indicators_dict_database=indicators_dict_database,
                                                         factor_calc_initial_date=factor_calc_initial_date,
                                                         liquidity_filter=liquidity_filter)
        
        print(wallet_to_database)

        return wallet_to_database
                
    ###
    ##
    # tools
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
            else:
                indicators_list = decoded_elements_list

        return indicators_list, variables_list
        
    def decode_command(command_string):

        indicators_list = []
        variables_list = []

        save_username_pattern = re.compile(r'save_username')
        update_fintz_database_pattern = re.compile(r'update_database')
        read_setups_pattern = re.compile(r'read_setups')
        calculate_risk_premiuns_pattern = re.compile(r'calculate_risk_premiuns\s*\(([^)]+)\)')
        rate_risk_premiuns_pattern = re.compile(r'rate_risk_premiuns\s*\(([^)]+)\)')
        rebalance_setup_pattern = re.compile(r'rebalance_setup\s*\(([^)]+)\)')

        if save_username_pattern.match(command_string):

            return {'command': 'save_username'}, indicators_list, variables_list
        elif update_fintz_database_pattern.match(command_string):

            return {'command': 'update_database'}, indicators_list, variables_list
        elif rebalance_setup_pattern.match(command_string):

            match = rebalance_setup_pattern.match(command_string)

            indicators_list, variables_list = TelegramManager.extract_elements_from_command(match)

            return {'command': 'rebalance_setup'}, indicators_list, variables_list
        elif calculate_risk_premiuns_pattern.match(command_string):

            match = calculate_risk_premiuns_pattern.match(command_string)

            indicators_list, variables_list = TelegramManager.extract_elements_from_command(match)

            return {'command': 'calculate_risk_premiuns'}, indicators_list, variables_list
        elif rate_risk_premiuns_pattern.match(command_string):

            match = rate_risk_premiuns_pattern.match(command_string)

            indicators_list, variables_list = TelegramManager.extract_elements_from_command(match)
            
            return {'command': 'rate_risk_premiuns'}, indicators_list, variables_list
        elif read_setups_pattern.match(command_string):
            
            return {'command': 'read_setups'}, indicators_list, variables_list
        else:
            return {'command': 'unknown'}, indicators_list, variables_list

    def create_rating_answer(distribution_indicadors, ranking_indicator, top_indicators, setup_dict, indicators_dict_database, save_setup, wallet_id, wallet_existent, wallets_df):


        distribution_indicadors['acum_primeiro_quartil'] = distribution_indicadors['acum_primeiro_quartil'].astype(float)
        distribution_indicadors['acum_primeiro_quartil'] = distribution_indicadors['acum_primeiro_quartil'] * 100
        distribution_indicadors['acum_primeiro_quartil'] = round(distribution_indicadors['acum_primeiro_quartil'], 1)

        top_indicators['acum_primeiro_quartil'] = top_indicators['acum_primeiro_quartil'].astype(float)
        top_indicators['acum_primeiro_quartil'] = top_indicators['acum_primeiro_quartil'] * 100
        top_indicators['acum_primeiro_quartil'] = round(top_indicators['acum_primeiro_quartil'], 1)

        len_top_indicators = len(top_indicators)
        len_ranking_indicator = len(ranking_indicator)

        markdown_text = f"Foram avaliados {len_ranking_indicator} combinações dos prêmios de risco atrelado aos indicadores e a está abaixo o rank{len_top_indicators}!! O ranking final foi feito por percentual de rentabilidade, no final é mostrado o ranking dos indicadores puros mostrando o número de vezes que o indicador apareceu no rank final.\n"
        markdown_text += f"\ntop_indicators: \n\n"

        # print(indicators_dict_database)
        
        for _, row in top_indicators.iterrows():
            
            file_names = []
            keys = []

            indicator = row['nome_indicador'].split('-with-')
            file_names.extend(indicator)
            file_names =list(file_names)
            # print(file_names)
            
            keys = [key for key, value in indicators_dict_database.items() if value['file_name'] in file_names]
            # print(keys)

            markdown_text += f"----------------------------\n"
            for indicator in keys:
                markdown_text += f"\t{indicator}\n"
            markdown_text += f"----------------------------\n"
            
            markdown_text += f"Rentabilidade -> {row['acum_primeiro_quartil']}% / pure: {row['Pure']}\n\n"
        
        markdown_text += f"\ndistribution_indicadors: \n\n"

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


#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    response_text = '''
    **BORA COMEÇAR ???**

    📣 
    Este BOT está conectado a aplicação FINAPP e eu sou seu intelocutor.
    
    📈 
    Será aqui que realizaremos avaliações de indicadores fundamentalistas para aplicar a técnica de Factor Investing para construir uma carteira de renda variável rentável!

    🐭 
    Resumidamente com esse BOT será possível avaliar e comparar a performance de rentabilidade de diferentes indicadores usando dados do mercado de ações brasileiro. 
    Definindo bons indicadores a serem seguidos, será também disponibilizado um comando para geração de carteira atualizada para possível acompanhamento de evolução.
    
    💰💰💰
    '''
    response_text = response_text.replace('_', r'\_')
    response_text = response_text.replace('!', r'\!')
    response_text = response_text.replace('?', r'\?')
    response_text = response_text.replace(':', r'\:')
    response_text = response_text.replace('.', r'\.')
    response_text = response_text.replace('-', r'\-')
    response_text = response_text.strip()
    
    await update.message.reply_text(response_text, parse_mode='MarkdownV2')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    response_text = '''
    🧭 **HELP PAGE** 🧭

    **Acceptable Commands:**
    😃 `hello`: I can respond this!
    💾 `save_username`: To start your journey you must configure your First Name, Last Name and username at Telegram Settings.

    **Admin Commands:**
    📦 `update_database`: To update_database fintz.
    📖 `calculate_risk_premiuns()`: Calculate premiuns risks of indicators alone, 2/2, and 3/3.
    🏗 `rate_risk_premiuns()`: Rank selected indicators.
    ⚖ `rebalance_setup(wallet_id=XXX)`: Rank selected indicators.
    '''
    response_text = response_text.replace('_', r'\_')
    response_text = response_text.replace('!', r'\!')
    response_text = response_text.replace(':', r'\:')
    response_text = response_text.replace('.', r'\.')
    response_text = response_text.replace('-', r'\-')
    response_text = response_text.strip()

    await update.message.reply_text(response_text, parse_mode='MarkdownV2')
    
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Custom command!')



#handle_message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    telegram_adm_id = os.getenv("TELEGRAM_ADM_ID")
    telegram_adm_id = str(telegram_adm_id)
    
    BOT_USERNAME = '@andretebar_bot'
    new_user = True
    adm_interaction     = False
    answer_in_group     = False
    fail_to_execute     = False
    enable_interaction  = True
    is_command          = False
    all_indicators_existents = False
    answer_text         = []
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
    if(user_id_existent == telegram_adm_id):
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

    # verifying commands
    if(decoded_command == 'save_username'):
        fail_to_execute = False
        await update.message.reply_text("Ok.")
        if(new_user and enable_interaction):
            username_existent = username
            telegram_user_manager.insert_telegram_user(new_user_df)

    if(decoded_command == 'update_database' and adm_interaction):
        fail_to_execute = False
        await update.message.reply_text("Ok.")
        TelegramManager.update_database_command()    
    
    if(decoded_command == 'rebalance_setup' and adm_interaction and (len(decoded_indicators_list) == 0 and len(decoded_variables_list) == 1) ):
        fail_to_execute = False
        await update.message.reply_text("Ok.")

        rebalance_wallet_id = '5879'
        rebalance_calc_end_date = '2023-12-02'
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
                assets_txt = f""
                fail_to_execute = True
            else:
                assets_txt = f"{wallet_to_database}"
                print(assets_txt)

                await update.message.reply_text(assets_txt)
    
    single_combinations     = True
    double_combinations     = True
    triple_combinations     = True
    list_combinations = []
    premium_dataframe = pd.DataFrame()

    if(decoded_command == 'calculate_risk_premiuns' and adm_interaction and all_indicators_existents):

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

    print('\nall_indicators_existents: ', all_indicators_existents)
    if(decoded_command == 'rate_risk_premiuns' and adm_interaction and all_indicators_existents):
        
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

                    create_date_auto = datetime.now()
                    create_date_auto = create_date_auto.strftime('%Y-%m-%d')

                    new_setup_to_insert = wallet_manager.preparing_setup_data(setups_dict = setup_dict, number_of_assets = 3, rebalance_periods = 33, user_name = username_existent, create_date = create_date_auto)

                    wallet_id, wallet_existent = wallet_manager.insert_setup(wallet_manager = wallet_manager, new_setup = new_setup_to_insert)
                else:
                    print('\nNÃO PODE SALVAR!!\n')
                
                # create_pdf = bool(create_pdf)
                print('\ncreate_pdf: ', create_pdf)
                if create_pdf:
                    print('\nPODE CRIAR O PDF!!\n')
                else:
                    print('\nNÃO PODE CRIAR O PDF!!\n')
                

                # answer_text = str(setup_dict)
                answer_text = TelegramManager.create_rating_answer(distribution_indicadors, ranking_indicator, top_indicators, setup_dict, indicators_dict_database,
                                                                save_setup, wallet_id, wallet_existent, wallets_df)
                # print('\nanswer_text: \n', answer_text)
            else:
                await update.message.reply_text("🚧 tente calcular os prêmios antes de avaliá-los.")

    if(decoded_command == 'read_setups' and adm_interaction):

        await update.message.reply_text("Ok.")

        wallet_manager = wm.WalletManager()
        file_not_found, wallets_df = wallet_manager.read_setups(username_existent)


        
    # defining when bot aswer
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
    app.add_handler(CommandHandler('custom', custom_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    app.add_error_handler(error)

    # polls the bot
    print('polling...\n')
    # app.run_polling(poll_interval = 3)

    # Iniciar o bot em um thread separado
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(app.run_polling(poll_interval = 3))
