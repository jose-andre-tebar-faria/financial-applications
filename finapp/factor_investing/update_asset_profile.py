import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np

class UpdateAssetProfile:

    def __init__(self):
        
        print("\nInicializing Asset Profile Updater!")

        load_dotenv()

        current_folder = os.getcwd()

        project_folder = os.getenv("PROJECT_FOLDER")
        databse_folder = os.getenv("DATABASE_FOLDER")
        self.full_desired_path = os.path.join(project_folder,databse_folder)

        if(current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

#
##
# LENDO ASSESTS NA BASE DE CADASTRO DE ASSETS
##
#
    def getting_assets_database(self):

        print('\n=== BUSCANDO ASSETS DA BASE DE CADASTRO! ==')

        self.assets_b3_database = pd.DataFrame()

        assets_database_parquet = pd.read_parquet(f'{self.full_desired_path}/sectors_assets_b3_webscraping.parquet')
        assets_database_df = pd.DataFrame(assets_database_parquet)
        assets_database_df.reset_index(inplace=True)
        # print(assets_database_df)

        self.assets_b3_database = assets_database_df.sort_values(by='asset', ascending= True)
        self.assets_b3_database.reset_index(inplace=True, drop=True)
        # print('primeiros 10 tickers em ordem alfabética: \n', assets_b3_database[:10], '\n')
        print('\tForam encontrados', len(self.assets_b3_database), 'tickers na base de webscraping!\n')

#
##
# LENDO ASSESTS DISTINTOS NA BASE DE COTAÇÕES
##
#
    def getting_assets_from_quotation(self):

        print('\n=== BUSCANDO ASSETS DA BASE DE COTAÇÕES! ==')

        assets_quotations_database = pd.DataFrame(columns=['asset', 'quotations_in_database'])

        quotations_database_parquet = pd.read_parquet(f'{self.full_desired_path}/cotacoes.parquet')

        quotations_database = pd.DataFrame(quotations_database_parquet)
        # print(quotations_database)
        print('\tForam encontrados', len(quotations_database), 'cotações!')

        assets_quotations_database['asset'] = quotations_database['ticker'].str[:4]
        # print(assets_quotations_database)

        assets_quotations_database['quotations_in_database'] = assets_quotations_database.groupby('asset')['asset'].transform('count')
        distint_tickers_in_quotations_database = assets_quotations_database.drop_duplicates('asset').sort_values(by=['asset'], ascending = True)
        distint_tickers_in_quotations_database.reset_index(inplace=True, drop=True)
        # print('primeiros 10 tickers em ordem alfabética: \n', distint_tickers_in_quotations_database[:10], '\n', '\n')
        print('\tForam encontrados', len(distint_tickers_in_quotations_database), 'tickers na base de cotações!\n')

        self.asset_profile_database = pd.merge(distint_tickers_in_quotations_database, self.assets_b3_database, on='asset')
        # print('\nAssets profile database: \n', asset_profile_database[asset_profile_database['sector'] == 'Saúde'])
        # print('\n\nAssets profile database: \n', asset_profile_database)
        # print('\nSize of profile database:', len(asset_profile_database))
        # print('\nColumns profile database: \n', asset_profile_database.columns)

        # sectors = asset_profile_database.drop_duplicates('sector')['sector'].sort_values(ascending = True)
        # sectors.reset_index(inplace=True, drop=True)
        # list_sectors = list(sectors)
        # # print(list_sectors)

        # subsectors = asset_profile_database.drop_duplicates('subsector')['subsector'].sort_values(ascending = True)
        # subsectors.reset_index(inplace=True, drop=True)
        # list_subsectors = list(subsectors)
        # # print(list_subsectors)

#
##
# CALCULANDO O GROWTH RATE -> OUTPUT(VARIAÇÃO PERCENTUAL ANUAL DE VALOR DE MERCADO + ÚLTIMA VARIAÇÃO PERCENTUAL)
##
#
    def calculationg_growth_rate(self):
        
        print('\n=== BUSCANDO VALORES DE MERCADO NA BASE DE ValorDeMercado! ==')

        marketvalue_database_parquet = pd.read_parquet(f'{self.full_desired_path}/ValorDeMercado.parquet')
        marketvalue_database_df = pd.DataFrame(marketvalue_database_parquet)
        marketvalue_database_df['data'] = pd.to_datetime(marketvalue_database_df['data'])
        marketvalue_database_df['ticker'] = marketvalue_database_df['ticker'].str[:4]
        marketvalue_database_df.rename(columns={'ticker': 'asset'}, inplace=True)
        marketvalue_database_df.rename(columns={'valor': 'market_value'}, inplace=True)
        marketvalue_database_df.rename(columns={'data': 'last_update_date'}, inplace=True)
        marketvalue_database_df = marketvalue_database_df.drop(columns=['indicador'])

        self.montly_marketvalue_database_df = marketvalue_database_df.sort_values(by='last_update_date').groupby(['asset', marketvalue_database_df['last_update_date'].dt.year]).tail(1)
        self.montly_marketvalue_database_df.reset_index(inplace=True, drop=True)
        # print(montly_marketvalue_database_df[montly_marketvalue_database_df['asset'] == 'AALR'])
        # print(montly_marketvalue_database_df)

        print('\n=== CALCULANDO GROWTH RATE! ==')

        growth_rate = pd.DataFrame()
        growth_rate = self.montly_marketvalue_database_df#['asset','last_update_date', 'market_value']
        growth_rate['growth_rate'] = self.montly_marketvalue_database_df.groupby('asset')['market_value'].pct_change(periods = 1)
        growth_rate.loc[growth_rate['growth_rate'] == 0, 'growth_rate'] = pd.NA
        growth_rate.loc[growth_rate['growth_rate'] == np.inf, 'growth_rate'] = pd.NA
        growth_rate = growth_rate.dropna()
        # print(growth_rate[growth_rate['asset'] == 'AALR'])
        # print(growth_rate)

        last_growth_rate = growth_rate.sort_values(by='last_update_date', ascending = True).groupby(['asset']).tail(1)
        last_growth_rate.reset_index(inplace=True, drop=True)
        last_growth_rate = last_growth_rate.sort_values(by='asset', ascending = True)
        # print(last_growth_rate[last_growth_rate['asset'] == 'AALR'])
        # print(last_growth_rate)

        self.asset_profile_database = pd.merge(self.asset_profile_database, last_growth_rate, on='asset')
        self.asset_profile_database.rename(columns={'growth_rate': 'last_growth_rate'}, inplace=True)
        # print('\nAssets profile database: \n', asset_profile_database[asset_profile_database['sector'] == 'Saúde'])
        # print('\n\nAssets profile database: \n', asset_profile_database)
        # print('\nSize of profile database:', len(asset_profile_database))
        # print('\nColumns profile database: \n', asset_profile_database.columns)

#
##
# CALCULANDO O MARKETSHARE ATUAL DE CADA ASSET
##
#
    def calculationg_marketshare(self):

        print('\n=== CALCULANDO MARKET SHARE! ==')

        self.asset_profile_database['sector_market_value'] = self.asset_profile_database.groupby('sector')['market_value'].transform('sum')
        self.asset_profile_database['subsector_market_value'] = self.asset_profile_database.groupby(['sector', 'subsector'])['market_value'].transform('sum')
        self.asset_profile_database['segment_market_value'] = self.asset_profile_database.groupby(['sector', 'subsector', 'segment'])['market_value'].transform('sum')
        self.asset_profile_database['sector_marketshare'] = self.asset_profile_database['market_value'] / self.asset_profile_database['sector_market_value']
        self.asset_profile_database['subsector_marketshare'] = self.asset_profile_database['market_value'] / self.asset_profile_database['subsector_market_value']
        self.asset_profile_database['segment_marketshare'] = self.asset_profile_database['market_value'] / self.asset_profile_database['segment_market_value']
        # print('\nAssets profile database: \n', self.asset_profile_database[self.asset_profile_database['sector'] == 'Saúde'])
        # print('\n\nAssets profile database: \n', self.asset_profile_database)
        # print('\nSize of profile database:', len(self.asset_profile_database))
        # print('\nColumns profile database: \n', self.asset_profile_database.columns)

    def save_profile_database(self):

        self.asset_profile_database = self.asset_profile_database.set_index('asset')
        print(self.asset_profile_database)

        self.asset_profile_database.to_parquet(f'{self.full_desired_path}/asset_database.parquet', index = True)
        print('\t=saving asset_database.parquet file.')

    def read_profile_database(self):
        
        assets_database_parquet = pd.read_parquet(f'{self.full_desired_path}/asset_database.parquet')
        assets_database_df = pd.DataFrame(assets_database_parquet)
        assets_database_df.reset_index(inplace=True)
        print(assets_database_df)
        print(assets_database_df.columns)

        return assets_database_df

if __name__ == "__main__":
    
    profile_updater = UpdateAssetProfile()

    # profile_updater.getting_assets_database()
    # profile_updater.getting_assets_from_quotation()
    # profile_updater.calculationg_growth_rate()
    # profile_updater.calculationg_marketshare()
    # profile_updater.save_profile_database()

    profile_updater.read_profile_database()
