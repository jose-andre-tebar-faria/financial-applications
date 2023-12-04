import finapp_controller as fc
import telegram_user_manager as tum

import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from io import StringIO
from datetime import datetime
import time
import re
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
    def handle_responses(text: str, username: str, new_user: bool, adm_interaction: bool, fail_to_execute: bool):

        processed_text: str = text.lower()

        print('\nadm_interaction: ', adm_interaction)
        print('\nfail_to_execute: ', fail_to_execute)

        if(adm_interaction and fail_to_execute == False):
            if 'save_username' in processed_text:
                if new_user:
                    return f'📊 thanks to setup your user!!\n.\n😄 username: {username}'
                else:
                    return f'📊 setup done!!\n.\n😄 username: {username}'
            if 'update_database' in processed_text:
                return 'database updated!'
            if 'calculate_risk_premiuns' in processed_text:
                return 'calculation complete!'
            if 'rate_risk_premiuns' in processed_text:
                return 'rating complete!'
            return 'invalid command'
        elif(adm_interaction and fail_to_execute == True):
            return 'execution error! verify command... 🤨'


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
        
        finapp = fc.FinappController()
        
        finapp.run_calculate_risk_premius(indicators_dict=indicators_dict, 
                                          single_combinations=single_combinations, double_combinations=double_combinations, triple_combinations=triple_combinations, 
                                          update_existing_file=update_existing_file)

    ###
    ##
    #rate_risk_premiuns   
    ##
    ###
    def rate_risk_premiuns_command(indicators_dict):
                
        final_analysis_date             = '2022-12-31'
        rating_premiuns_file_name       = r'..\\PDFs\rating-BEST_INDICATORS.pdf'
        create_rating_pdf               = False
        
        number_of_top_comb_indicators = 5
    
        finapp = fc.FinappController()
        
        # ranking_indicator = finapp.run_rate_risk_premius(
        #                                                 indicators_dict=indicators_dict,
        #                                                 final_analysis_date=final_analysis_date, 
        #                                                 rating_premiuns_file_name=rating_premiuns_file_name,
        #                                                 number_of_top_comb_indicators=number_of_top_comb_indicators,
        #                                                 create_rating_pdf=create_rating_pdf
        #                                                 )

        ##
        # CREATE AUTOMATIC PONDERATED WALLET
        ##
        # setup_dict = finapp.create_automatic_wallet(ranking_indicator)

        # return setup_dict
    
    def decode_command(command_string):

        save_username_pattern = re.compile(r'save_username')
        update_fintz_database_pattern = re.compile(r'update_database')
        calculate_risk_premiuns_pattern = re.compile(r'calculate_risk_premiuns\s*\(([^)]+)\)')
        rate_risk_premiuns_pattern = re.compile(r'rate_risk_premiuns\s*\(([^)]+)\)')

        if save_username_pattern.match(command_string):
            return {'command': 'save_username'}
        elif update_fintz_database_pattern.match(command_string):
            return {'command': 'update_database'}
        elif calculate_risk_premiuns_pattern.match(command_string):
            match = calculate_risk_premiuns_pattern.match(command_string)
            indicators = match.group(1)
            return {'command': 'calculate_risk_premiuns', 'indicators': indicators}
        elif rate_risk_premiuns_pattern.match(command_string):
            match = rate_risk_premiuns_pattern.match(command_string)
            indicators = match.group(1)
            return {'command': 'rate_risk_premiuns', 'indicators': indicators}
        else:
            return {'command': 'unknown'}

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
    💾 `save_username`: To start your journey.

    **Admin Commands:**
    📦 `update_database`: To update_database fintz.
    📖 `calculate_risk_premiuns()`: Calculate premiuns risks of indicators alone, 2/2, and 3/3.
    🏗 `rate_risk_premiuns()`: Rank selected indicators.
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




async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    BOT_USERNAME = '@andretebar_bot'
    new_user = True
    adm_interaction = False
    answer_in_group = False
    fail_to_execute = True
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
    # print('username: ', username)
    id: str = update.message.from_user.id
    # print('id: ', id)
    first_name: str = update.message.from_user.first_name
    last_name: str = update.message.from_user.last_name
    # print(f'name: {first_name} {last_name}')
    user_is_bot: str = update.message.from_user.is_bot
    # print('user_is_bot: ', user_is_bot)

    telegram_user_manager = tum.TelegramUserManager()
    new_user_df = telegram_user_manager.prepare_telegram_user(user_id=id,username=username,first_name=first_name, last_name=last_name, is_bot=user_is_bot, is_adm=False)
    # print('new_user_df: \n', new_user_df)

    new_user, verifying_presence, username_existent, user_id_existent = telegram_user_manager.verify_telegram_user(new_user_df)
    print(user_id_existent)
    print(username_existent)

    text: str = update.message.text
    print(f'\n-> message from user ({username}) in {message_type}: "{text}"')

    new_text = text
    
    # parse text from groups
    if message_type == 'supergroup':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            answer_in_group = True
    else:
        new_text = text

    # decode commands
    decoded_command_dict = TelegramManager.decode_command(new_text)
    print('\ndecoded_command_dict: ', decoded_command_dict)
    decoded_command = decoded_command_dict['command']
    print('\ndecoded_command: ', decoded_command)
    
    # capture indicators
    decoded_indicators = decoded_command_dict.get('indicators')
    if decoded_indicators is not None:
        decoded_indicators_list = decoded_indicators.split(',')
        decoded_indicators_list = [indicator.strip() for indicator in decoded_indicators_list]
        print('\ndecoded_indicators: ', decoded_indicators_list)

        indicators_database_list = list(indicators_dict_database.keys())
        print('\nindicators_database_list: ', indicators_database_list)

        all_indicators_existents = all(elemento in indicators_database_list for elemento in decoded_indicators_list)
        print(all_indicators_existents)

        if(all_indicators_existents):
            fail_to_execute = False

    #defining adm user
    if(decoded_command != 'unknown' and user_id_existent == '6013346178'):
        adm_interaction = True
    
    # verifying commands
    if(decoded_command == 'save_username'):
        fail_to_execute = False
        adm_interaction = True
        if(new_user):
            telegram_user_manager.insert_telegram_user(new_user_df)

    if(decoded_command == 'update_database' and adm_interaction and all_indicators_existents):
        TelegramManager.update_database_command()
    
    if(decoded_command == 'calculate_risk_premiuns' and adm_interaction and all_indicators_existents):
        
        single_combinations     = True
        double_combinations     = True
        triple_combinations     = True

        update_existing_file    = False

        indicators_dict = {chave: indicators_dict_database[chave] for chave in decoded_indicators_list if chave in indicators_dict_database}
        # print(indicators_dict)

        TelegramManager.calculate_risk_premiuns_command(indicators_dict, single_combinations, double_combinations, triple_combinations, 
                                                        update_existing_file)

    if(decoded_command == 'rate_risk_premiuns' and adm_interaction and all_indicators_existents):

        TelegramManager.rate_risk_premiuns_command(indicators_dict_database)

    # defining when bot aswer
    if message_type == 'supergroup':
        if answer_in_group:
            response: str = TelegramManager.handle_responses(new_text, username, new_user, adm_interaction,fail_to_execute)
        else:
            return
    else:
        response: str = TelegramManager.handle_responses(text, username, new_user, adm_interaction, fail_to_execute)

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
    app.run_polling(poll_interval = 3)