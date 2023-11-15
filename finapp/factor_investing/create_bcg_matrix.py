import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

current_folder = os.getcwd()

project_folder = os.getenv("PROJECT_FOLDER")
databse_folder = os.getenv("DATABASE_FOLDER")
full_desired_path = os.path.join(project_folder,databse_folder)

if(current_folder != full_desired_path):
    os.chdir(full_desired_path)

#
##
###
# LENDO ASSESTS NA BASE DE WEBSCRAPING (MÃE)
###
##
#
print('=== BUSCANDO ASSETS DA BASE DE WEBSRAPING! ==\n')

assets_b3_database = pd.DataFrame()
list_asset_b3_database = []

assets_database_parquet = pd.read_parquet(f'{full_desired_path}/assets_database.parquet')
assets_database_df = pd.DataFrame(assets_database_parquet)
assets_database_df.reset_index(inplace=True)

# print(assets_database_df)

assets_b3_database = assets_database_df.sort_values(by='asset', ascending= True)
assets_b3_database.reset_index(inplace=True, drop=True)

assets_b3_database = assets_b3_database
# print('primeiros 10 tickers em ordem alfabética: \n', assets_b3_database[:10], '\n')
print('Foram encontrados', len(assets_b3_database), 'tickers na base de webscraping!\n')

#
##
###
# LENDO ASSESTS DISTINTOS NA BASE DE COTAÇÕES
###
##
#
print('=== BUSCANDO ASSETS DA BASE DE COTAÇÕES! ==\n')

assets_quotations_database = pd.DataFrame(columns=['asset', 'quotations_in_database'])
list_asset_quotations_database = []

quotations_database_parquet = pd.read_parquet(f'{full_desired_path}/cotacoes.parquet')

quotations_database = pd.DataFrame(quotations_database_parquet)

# print(quotations_database)
print('Foram encontrados', len(quotations_database), 'cotações!')

assets_quotations_database['asset'] = quotations_database['ticker'].str[:4]

# print(assets_quotations_database)

assets_quotations_database['quotations_in_database'] = assets_quotations_database.groupby('asset')['asset'].transform('count')
distint_tickers_in_quotations_database = assets_quotations_database.drop_duplicates('asset').sort_values(by=['asset'], ascending = True)
distint_tickers_in_quotations_database.reset_index(inplace=True, drop=True)

distint_tickers_in_quotations_database = distint_tickers_in_quotations_database

# print('primeiros 10 tickers em ordem alfabética: \n', distint_tickers_in_quotations_database[:10], '\n', '\n')
print('Foram encontrados', len(distint_tickers_in_quotations_database), 'tickers na base de cotações!\n')

asset_profile_database = pd.merge(distint_tickers_in_quotations_database, assets_b3_database, on='asset')

print('Assets profile database: \n',asset_profile_database)
# print(len(iguais))
