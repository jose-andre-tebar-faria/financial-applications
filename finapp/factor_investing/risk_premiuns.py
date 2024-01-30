import pandas as pd
import numpy as np
from dateutil.relativedelta  import relativedelta
import os
from dotenv import load_dotenv
# from datetime import date
from unidecode import unidecode
import datetime

class RiskPremium:

    def __init__(self, indicators_dict, premium_name, liquidity=0):

        print("Inicializing RiskPremium!")

        load_dotenv()
        
        self.indicators = list(indicators_dict.keys())
        #print(self.indicators)
        
        desired_value = 'order'
        self.indicators_order = [order[desired_value] for order in indicators_dict.values()]
        #print(self.indicators_order)

        self.liquidity = liquidity
        self.premium_name = premium_name

        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.databse_folder = os.getenv("DATABASE_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.databse_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)
        
        print("OK.")

    def filtering_tickers_by_sectors(self, sector=''):

        self.sector = sector
        self.tickers_database = pd.read_parquet("sectors_assets_b3_webscraping.parquet")
        # print(f'tickers_database: \n {self.tickers_database}')

        self.sectors = self.tickers_database.groupby('sector').count()
        # print(f'sectors: \n {self.sectors.index}')
        # self.subsectors = self.tickers_database.groupby('subsector').count()
        # print(self.subsectors)

        self.sectors_list = list(self.sectors.index)
        print(f'sectors_list: \n {self.sectors_list}')

        self.ticker_sector_df = pd.DataFrame({'ticker': self.tickers_database['ticker'], 'sector': self.tickers_database['sector']})
        # print(f'ticker_sector_df: \n {self.ticker_sector_df}')
        self.ticker_sector_df['ticker'].replace('', pd.NA, inplace=True)
        self.ticker_sector_df = self.ticker_sector_df.dropna(subset=['ticker'])
        # print(f'ticker_sector_df: \n {self.ticker_sector_df}')

    def getting_quotations(self):

        self.quotations = pd.read_parquet("cotacoes.parquet")
        # print(f'self.quotations 1: \n {str(self.quotations[["data", "ticker", "preco_fechamento"]])}')

        if self.sector != '':

            filtered_tickers = self.ticker_sector_df[self.ticker_sector_df['sector'] == self.sector]['ticker']
            # print(f'self.filtered_tickers: \n {filtered_tickers}')
            self.filtered_tickers_list = list(filtered_tickers)
            # print(f'self.filtered_tickers_list: \n {self.filtered_tickers_list}')

            self.quotations_by_sector = self.quotations[self.quotations['ticker'].isin(self.filtered_tickers_list)]
            # print(f'self.quotations_by_sector: \n {str(self.quotations_by_sector[["data", "ticker", "preco_fechamento"]])}')

            self.quotations_by_sector['id_dado'] = self.quotations_by_sector['ticker'].astype(str) + "_" + self.quotations_by_sector['data'].astype(str)
            self.quotations_by_sector['data'] = pd.to_datetime(self.quotations_by_sector['data']).dt.date
        else:
            self.quotations['id_dado'] = self.quotations['ticker'].astype(str) + "_" + self.quotations['data'].astype(str)
            self.quotations['data'] = pd.to_datetime(self.quotations['data']).dt.date

        
        # self.quotations['id_dado'] = self.quotations['ticker'].astype(str) + "_" + self.quotations['data'].astype(str)
        # self.quotations['data'] = pd.to_datetime(self.quotations['data']).dt.date

    def getting_possible_dates(self):

        petr_quotations = self.quotations[self.quotations['ticker'] == 'PETR4']

        petr_quotations = petr_quotations.sort_values('data', ascending = True)
        petr_quotations = petr_quotations.assign(year = pd.DatetimeIndex(petr_quotations['data']).year)
        petr_quotations = petr_quotations.assign(month = pd.DatetimeIndex(petr_quotations['data']).month)
        all_last_dates_each_month = petr_quotations.groupby(['year', 'month'])['data'].last()
        all_last_dates_each_month = all_last_dates_each_month.reset_index()

        all_last_dates_each_month['data'] = all_last_dates_each_month['data'].apply(lambda x: datetime.date(x.year, x.month, x.day))

        # print(f'all_last_dates_each_month: \n {all_last_dates_each_month}')

        self.all_last_dates_each_month = all_last_dates_each_month

        if self.sector != '':
            print('\nself.quotations_by_sector: \n', self.quotations_by_sector[['data','ticker', 'preco_fechamento_ajustado']])
            self.quotations = self.quotations_by_sector
            self.quotations['data'] = pd.to_datetime(self.quotations['data']).dt.date
        # print(f'self.quotations 2: \n {self.quotations}')

    def filtering_volume(self):

        median_volume_data = pd.read_parquet("volume_mediano.parquet")
        median_volume_data['id_dado'] = median_volume_data['ticker'].astype(str) + "_" + median_volume_data['data'].astype(str)
        median_volume_data = median_volume_data[['id_dado', 'valor']]
        median_volume_data.columns = ['id_dado', 'volumeMediano']
        self.quotations = pd.merge(self.quotations, median_volume_data, how = 'inner', on = 'id_dado')
        self.quotations = self.quotations[self.quotations['volumeMediano'] > self.liquidity]
        # print(f'self.quotations 3: \n {self.quotations}')

    def getting_indicators(self):
        
        self.indicators_dataframe = []
        for indicator in self.indicators:
            try:
               df = pd.read_parquet(f'{indicator}.parquet')
               df['data'] = pd.to_datetime(df['data']).dt.date
            except:
               df = None
               print("Indicator file not found.")
            self.indicators_dataframe.append(df)

        # print(f'self.quotations 4: \n {self.indicators_dataframe}')

    def discovering_initial_month(self):
        dates = []
        for df in self.indicators_dataframe:
            indicator_without_na = df.dropna()
            petr_indicator = indicator_without_na.query('ticker == "PETR4"') #eu usei a petro como parametro pra saber a primeira data de qlqr indicador.
            minimum_date = min(petr_indicator['data'])
            dates.append(minimum_date)
        general_minimum_date = max(dates)  #maximo porque queremos a MAIOR data mínima entre os indicadores.
        self.general_minimum_date = general_minimum_date + relativedelta(months=+2)
        #vou colocar 2 meses depois da primeira empresa ter o indicador. isso pq os indicadores fundamentalistas no 
        #1 mes da base podem ser muito escassos devido a maioria das empresas não terem soltado resultado ainda.
        self.list_all_last_dates_each_month = (self.all_last_dates_each_month.query('data >= @self.general_minimum_date'))['data'].to_list()
        self.filtered_quotations = self.quotations.query('data >= @self.general_minimum_date')

        # print(f'self.list_all_last_dates_each_month: \n {self.list_all_last_dates_each_month}')

        # print(f'self.filtered_quotations 5: \n {self.filtered_quotations}')

    def calculating_premiuns(self):

        print("Calculating Premium.")
        
        dataframe_columns = ['primeiro_quartil', 'segundo_quartil', 'terceiro_quartil', 'quarto_quartil', 'universo']
        premiuns_dataframe = pd.DataFrame(columns=dataframe_columns, index=self.list_all_last_dates_each_month)

        lista_dfs = [None] * 4  # inicializa lista para guardar dataframes de quartis

        for i, data in enumerate(self.list_all_last_dates_each_month):

            # print(f'data: \n {data}')
            df_info_pontuais = self.filtered_quotations[self.filtered_quotations['data'] == data][['ticker', 'preco_fechamento_ajustado', 'volume_negociado']]
            # print(f'df_info_pontuais: \n {df_info_pontuais}')

            #calculando rent da carteira anterior
            if i != 0:
                df_vendas = df_info_pontuais[['ticker', 'preco_fechamento_ajustado']]
                df_vendas.columns = ['ticker', 'preco_fechamento_ajustado_posterior']
                lista_retornos = []

                for zeta, df in enumerate(lista_dfs):
                    df_quartil = pd.merge(df, df_vendas, how='inner', on='ticker')
                    df_quartil['retorno'] = df_quartil['preco_fechamento_ajustado_posterior'] / df_quartil['preco_fechamento_ajustado'] - 1
                    retorno_quartil = df_quartil['retorno'].mean()
                    lista_retornos.append(retorno_quartil)
                    premiuns_dataframe.loc[data, dataframe_columns[zeta]] = retorno_quartil

                premiuns_dataframe.loc[data, 'universo'] = np.mean(np.array(lista_retornos))

            # print(f'premiuns_dataframe: \n{premiuns_dataframe}')

            #pegando as novas carteiras
            df_info_pontuais['ranking_final'] = 0

            for alfa, indicator in enumerate(self.indicators_dataframe):
           
                indicador_na_data = indicator.loc[indicator['data'] == data, ['ticker', 'valor']].dropna()
                
                indicador_na_data.columns = ['ticker', f'indicador_{self.indicators[alfa]}']
                df_info_pontuais = pd.merge(df_info_pontuais, indicador_na_data, how='inner', on='ticker')

            #filtrando empresas com varios tickers pro mais líquido
            df_info_pontuais['comeco_ticker'] = df_info_pontuais['ticker'].astype(str).str[0:4]
            df_info_pontuais.sort_values('volume_negociado', ascending=False, inplace=True)
            df_info_pontuais.drop_duplicates('comeco_ticker', inplace=True)
            df_info_pontuais.drop('comeco_ticker', axis=1, inplace=True)

            for alfa, ordem in enumerate(self.indicators_order): 
                crescente_condicao = ordem.lower() == 'crescente'
                df_info_pontuais[f'ranking_{alfa}'] = df_info_pontuais[f'indicador_{self.indicators[alfa]}'].rank(ascending=crescente_condicao)
                df_info_pontuais['ranking_final'] += df_info_pontuais[f'ranking_{alfa}']

            df_info_pontuais.sort_values('ranking_final', ascending=True, inplace=True)

            empresas_por_quartil = len(df_info_pontuais) // 4
            sobra_empresas = len(df_info_pontuais) % 4

            # dividindo o dataframe em quartis
            lista_dfs[0] = df_info_pontuais.iloc[0: empresas_por_quartil]
            lista_dfs[1] = df_info_pontuais.iloc[empresas_por_quartil: (empresas_por_quartil * 2)]
            lista_dfs[2] = df_info_pontuais.iloc[(empresas_por_quartil * 2): (empresas_por_quartil * 3)]
            lista_dfs[3] = df_info_pontuais.iloc[(empresas_por_quartil * 3): ((empresas_por_quartil * 4) + sobra_empresas)]
                
        # print("\ndf_info_pontuais: \n", df_info_pontuais)
    
        #print("primeiro_quartil",lista_dfs[0])

        premiuns_dataframe['nome_premio'] = self.premium_name
        premiuns_dataframe['liquidez'] = self.liquidity
        premiuns_dataframe.reset_index(names='data', inplace=True)
        premiuns_dataframe['id_premio'] = premiuns_dataframe['nome_premio'].astype(str) + "_" + premiuns_dataframe['liquidez'].astype(str) + "_" + premiuns_dataframe['data'].astype(str)
        premiuns_dataframe.dropna(inplace=True)
        self.premiuns_dataframe = premiuns_dataframe

        print("Ok.")
        
        return self.premiuns_dataframe

    def saving_premiuns(self):
        
        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.databse_folder = os.getenv("PREMIUNS_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.databse_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

        # print(self.premiuns_dataframe)
        # print(self.premium_name)

        self.premiuns_dataframe.to_parquet(f'{self.full_desired_path}/{self.premium_name}_{self.liquidity}.parquet', index = False) 