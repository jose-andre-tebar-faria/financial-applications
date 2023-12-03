import finapp_controller as fc
import telegram_user_manager as tum

import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from io import StringIO
from datetime import datetime
import time
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, CallbackContext, ContextTypes


class TelegramtManager:

    # responses
    def handle_responses(text: str, username: str):

        enable_interaction = False

        if(username == 'jandretebarf'):
            enable_interaction = True

        processed_text: str = text.lower()

        if(enable_interaction):
            if 'hello' in processed_text:
                return 'i see you!!'
        
            return 'no no no'

#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('HELP! \ntype: save_username - to start your journey')
    
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Custom command!')

async def update_database_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text('Database updated initializing...!')

    finapp = fc.FinappController()

    # enable database update
    update_database                 = True
    update_api_database             = False
    update_fintz_database           = True
    update_webscrapping_database    = False

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

    await update.message.reply_text('Database updated DONE!')



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    BOT_USERNAME = '@andretebar_bot'

    message_type: str = update.message.chat.type
    # print('message_type: ', message_type)
    username: str = update.message.from_user.username
    # print('username: ', username)

    text: str = update.message.text
    print(f'\n-> message from user ({username}) in {message_type}: "{text}"')

    if(text == 'save_username'):

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

        new_user = telegram_user_manager.verify_telegram_user(new_user_df)

        if(new_user):
            telegram_user_manager.insert_telegram_user(new_user_df)


    if message_type == 'supergroup':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = TelegramtManager.handle_responses(new_text, username)
        else:
            return
    else:
        response: str = TelegramtManager.handle_responses(text, username)

    print('--> BOT responds: ', response)

    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')



#
## MAIN
#
if __name__ == "__main__":
        
    print("\n\nInicializing Telegram Manager!\n.")

    load_dotenv()

    telegram_manager = TelegramtManager()

    current_folder = os.getcwd()

    project_folder = os.getenv("PROJECT_FOLDER")
    databse_folder = os.getenv("DATABASE_FOLDER")
    full_desired_path = os.path.join(project_folder,databse_folder)

    if(current_folder != full_desired_path):
        os.chdir(full_desired_path)

    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_token = str(telegram_token)

    app = Application.builder().token(telegram_token).build()

    # Adição do manipulador de comando
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('update_database', update_database_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    app.add_error_handler(error)

    # polls the bot
    print('polling...\n')

    app.run_polling(poll_interval = 3)