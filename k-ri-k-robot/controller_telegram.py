import controller_find_group as cfg

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

    # responses
    def handle_responses(username: str, answer_text: str):
        
        if(answer_text != '0'):
            created_answer = f'existem {answer_text} vagas no grupo!'
        else:
            created_answer = 'grupo cheio.'

        return created_answer

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

###
##
#HANDLE MESSAGE
##
###
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    BOT_USERNAME = '@movedude_bot'
    answer_in_group             = True
    old_message                 = True
    
    #ignoring old messages (older than 10 minutes)
    message_txt: str = update.message
    # print('message_txt: ', message_txt)
    date_txt: str = update.message.date
    # print('date_txt: ', date_txt)
    message_datetime = pd.to_datetime(date_txt)
    print('message_datetime: ', message_datetime)


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

    text: str = update.message.text
    print(f'\n-> message from user ({username}) in {message_type}: "{text}"')
    
    if(text == 'vai carai'):
        
        find_group = cfg.FindGroup()

        find_group.find_vacancy()
        
        time.sleep(5)

        find_group.printing_number()
        
        time.sleep(5)

        numero = find_group.recognize_number()

        answer_text = str(numero)

    # defining when bot aswer
    if message_type == 'supergroup':
        if answer_in_group:
            response: str = TelegramManager.handle_responses(username, answer_text)
        else:
            return
    else:
        response: str = TelegramManager.handle_responses(username, answer_text)

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

    telegram_token = '6658174273:AAHXq_56vToHz35M2hfj3sKV7eMViql2JNQ'
    telegram_token = str(telegram_token)

    app = Application.builder().token(telegram_token).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))

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