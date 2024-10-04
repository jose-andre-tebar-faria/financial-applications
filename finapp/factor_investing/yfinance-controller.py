import yfinance as yf 

ticker = yf.Ticker("VALE")
ticket_info = ticker.info

# Obtenha o número de ações em circulação
stock_quantity = ticket_info['sharesOutstanding']
print("\nstock_quantity: ", stock_quantity)

# Obtenha o valor patrimonial (book value) por ação
patrimonial_value_per_stock = ticket_info['bookValue']
patrimonial_value = patrimonial_value_per_stock * stock_quantity
print("\npatrimonial_value: [bilhões]", patrimonial_value/1000000000)

