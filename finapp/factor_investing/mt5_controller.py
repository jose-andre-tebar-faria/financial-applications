import pandas as pd
import MetaTrader5 as mt5
import pandas as pd
import datetime
import pytz

mt5.initialize()

# Exibe informações sobre a conta
account_info = mt5.account_info()
print("Account info:", account_info)

mt5.symbol_select('ABEV3')

symbols = mt5.symbols_get()
# print('\nsimbolos: ', simbolos)

tickers = [simbolo.name for simbolo in symbols]
tickers = sorted(tickers, reverse=True)
# print('\ntickers: ', tickers)

stock_list = []

for ticker in tickers:
    
    try:
        int(ticker[3]) #a quarta letra tem que ser uma string, não um número
        
    except:

        final_ticker = ticker[4:]

        if len(final_ticker) == 2:

            if final_ticker == "11":

                if (ticker[0:4] + "3") in stock_list or (ticker[0:4] + "4") in stock_list or (ticker[0:4] + "6") in stock_list:

                    stock_list.append(ticker)

        if len(final_ticker) == 1:  

            if final_ticker == "3" or final_ticker == "4" or final_ticker == "5" or final_ticker == "6":

                stock_list.append(ticker)

print('\nstock_list: ', stock_list)
print('\nlen(stock_list): ', len(stock_list))

for stock in stock_list:

    mt5.symbol_select(stock)

# while True:
#     ticker = 'WEGE3'

#     retorno = mt5.symbol_info(ticker).price_change
#     fechamento = mt5.symbol_info(ticker).last

#     print(retorno, fechamento)
#     time.sleep(1)

stock = 'WEGE3'

timezone = pytz.timezone("Brazil/West")

initial_date = (datetime.datetime.now(tz = timezone) - datetime.timedelta(days= 1095))
print('\ninitial_date: ', initial_date)

final_date = datetime.datetime.now(tz = timezone)
print('\nfinal_date: ', final_date)

quotations = mt5.copy_rates_range(stock, mt5.TIMEFRAME_D1, initial_date, final_date)
quotations = pd.DataFrame(quotations)
quotations = quotations[['time', 'open', 'high', 'low', 'close']]
quotations['time'] = pd.to_datetime(quotations['time'], unit='s')
quotations['ticker'] = stock
print('\nquotations: \n', quotations)




# Obtenha as posições abertas
positions = mt5.positions_get()

# Se não houver posições abertas, imprima uma mensagem
if not positions:
    print("Nenhuma posição aberta encontrada.")
else:
    # Exiba as informações de cada posição aberta
    for position in positions:
        print("Símbolo:", position.symbol)
        print("Tipo de ordem:", position.type)
        print("Volume:", position.volume)
        print("Preço de abertura:", position.price_open)
        print("Lucro não realizado:", position.profit)
        print("--------------------------------")
