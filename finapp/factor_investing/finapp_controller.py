import download_fintz_data as dfd
import make_indicators as mi
import risk_premiuns as rp
import rate_risk_premiuns as rrp
import factor_calculator as fc
import market_premium as mp
import regression_model as rm

import os
from dotenv import load_dotenv
import pandas as pd
from itertools import combinations
import subprocess
from dateutil.relativedelta  import relativedelta

class FinappController:

    def __init__(self):
                
        print("Inicializing FinappController!")
        
        load_dotenv()

    def calculate_combinations(self, premium_name, len_premium_name, single_combinations = False, double_combinations = False, triple_combinations = False):

        self.premium_name = premium_name
        all_combinations = []
        self.list_combinations = []

        self.triple_combinations = triple_combinations
        self.double_combinations = double_combinations
        self.single_combinations = single_combinations

        if(len_premium_name >= 3 and triple_combinations):
            
            all_combinations = list(combinations(premium_name, 3))

            for combination in all_combinations:
                self.list_combinations.append(combination)

        if(len_premium_name >= 2 and double_combinations):

            all_combinations = list(combinations(premium_name, 2))

            for combination in all_combinations:
                self.list_combinations.append(combination)
        
        if(len_premium_name >= 1 and single_combinations):

            all_combinations = list(combinations(premium_name, 1))

            for combination in all_combinations:
                self.list_combinations.append(combination)

        return self.list_combinations

    def create_file_names(self, list_combinations, indicators_dict):

        self.list_combination_file_name = []

        self.list_combinations = list_combinations
        self.indicators_dict = indicators_dict

        for combination in self.list_combinations:
            indicators_dict_new = {key: self.indicators_dict[key] for key in combination} 

            desired_value = 'file_name'
            self.premium_name = [file_name[desired_value] for file_name in indicators_dict_new.values()]
            self.premium_name = '-with-'.join(self.premium_name)

            self.list_combination_file_name.append(self.premium_name)

        return self.list_combination_file_name

    def reading_folder_files(self):

        parsed_premium_files_name = []

        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.databse_folder = os.getenv("PREMIUNS_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.databse_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

        full_files_name = [file for file in os.listdir(self.full_desired_path) if os.path.isfile(os.path.join(self.full_desired_path, file))]

        # print(full_files_name)

        for file_name in full_files_name:
            last_underscore_location = file_name.rfind("_")
            if last_underscore_location != -1:
                parsed_premium_files_name.append(file_name[:last_underscore_location])

        # parsed_premium_files_name.remove('market_premium.parquet')

        # print(parsed_premium_files_name)

        return parsed_premium_files_name

if __name__ == "__main__":

    finapp = FinappController()

    # enable database update
    update_database             = False
    # enable indicators update
    update_indicators           = False
    # enable calculate risk premiuns database update
    calculate_risk_premiuns     = False
    # enable rating risks
    rate_risk_premiuns          = False
    # enable run a regression model
    execute_regression_model    = False
    # enable generation of wallet
    generate_wallets            = True
    # enable requirements.txt update
    update_requirements_txt     = False

    ###
    ##
    #download_fintz_data
    ##
    ###
    demonstration_list = [
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

    indicators_list = [
                        'L_P', 'ROE', 'ROIC', 'EV', 'LPA', 'P_L', 'EBIT_EV', 'ValorDeMercado'
                        ]
    
    if(update_database):

        print(".\n..\n...\nUpdating Database!\n...\n..\n.")

        reading_data = dfd.FintzData()

        for demonstration in demonstration_list:
           reading_data.download_accounting_files(demonstration=True, data_name = demonstration)

        for indicator in indicators_list:
           reading_data.download_accounting_files(indicator=True, data_name = indicator)

        reading_data.download_cdi(initial_date="2000-01-01")
        reading_data.download_ibov(initial_date="2000-01-01")
        reading_data.download_quotations()
        
        print(".\n.\n=== UPDATE COMPLETE! ===")

    ###
    ##
    #make_indicators
    ##
    ###
    if(update_indicators):

        print(".\n..\n...\nUpdating Indicators!\n...\n..\n.")

        indicator = mi.MakeIndicator()

        indicator.making_momentum(months = 1)
        indicator.making_momentum(months = 6)
        indicator.making_momentum(months = 12)
        indicator.ratio_moving_mean(mm_curta = 7, mm_longa = 40)
        indicator.median_volume(months = 1)
        indicator.beta(years = 1)
        indicator.volatility(years = 1)
        indicator.pl_divida_bruta()
        indicator.ebit_divida_liquida()
        
        print(".\n.\n=== UPDATE COMPLETE! ===")

    ###
    ##
    #risk_premiuns
    ##
    ###
    indicators_dict = {
                        'ValorDeMercado':     {'file_name': 'TAMANHO_VALOR_DE_MERCADO',   'order': 'crescente'},
                        # 'ROIC':               {'file_name': 'QUALITY_ROIC',               'order': 'decrescente'},
                        # 'ROE':                {'file_name': 'QUALITY_ROE',                'order': 'decrescente'},
                        'EBIT_EV':            {'file_name': 'VALOR_EBIT_EV',              'order': 'decrescente'},
                        # 'L_P':                {'file_name': 'VALOR_L_P',                  'order': 'decrescente'},
                        # 'vol_252':            {'file_name': 'RISCO_VOL',                  'order': 'crescente'},
                        'ebit_dl':            {'file_name': 'ALAVANCAGEM_EBIT_DL',        'order': 'decrescente'},
                        'pl_db':              {'file_name': 'ALAVANCAGEM_PL_DB',          'order': 'decrescente'},
                        'mm_7_40':            {'file_name': 'MOMENTO_MM_7_40',            'order': 'decrescente'},
                        # 'momento_1_meses':    {'file_name': 'MOMENTO_R1M',                'order': 'decrescente'},
                        'momento_6_meses':    {'file_name': 'MOMENTO_R6M',                'order': 'decrescente'},
                        # 'momento_12_meses':   {'file_name': 'MOMENTO_R12M',               'order': 'decrescente'},
                        }
    
    # choose de indicators combinations to rate
    single_combinations     = True
    double_combinations     = True
    triple_combinations     = False
    
    #True if you want to update a existing file
    update_existing_file    = False

    number_of_top_comb_indicators = 10
    number_of_top_single_indicators = 3

    if(calculate_risk_premiuns):

        print(".\n..\n...\nCalculating Risk Premiuns!\n...\n..\n.")
        beta = mp.MarketPremium()

        beta.calculate_market_premium()

        premium_name = indicators_dict.keys()
        len_premium_name = len(premium_name)

        list_combinations = finapp.calculate_combinations(premium_name, len_premium_name, single_combinations, double_combinations, triple_combinations)

        if(len(list_combinations) > 0):
            
            print('.\n.\nNumber of combinations: ', len(list_combinations), '\n.\n.')

            list_combination_file_name = finapp.create_file_names(list_combinations, indicators_dict)

            folder_files = finapp.reading_folder_files()

            combination_step = 1

            for combination, premium_name in zip(list_combinations, list_combination_file_name):

                indicators_dict_new = {key: indicators_dict[key] for key in combination} 

                print('<\nStep: ', combination_step)
                print('Premium dictionary: \n\t', indicators_dict_new)
                print('\tpremium_name: ' , premium_name)

                if((premium_name not in folder_files) or update_existing_file):

                    premium = rp.RiskPremium(indicators_dict_new, premium_name, liquidity = 1000000)
                    
                    print("Preparing Data....")
                    premium.getting_quotations()
                    premium.getting_possible_dates()
                    premium.filtering_volume()
                    premium.getting_indicators()
                    premium.discovering_initial_month()
                    print("OK.")
                    premium_dataframe = premium.calculating_premiuns()

                    # print(premium_dataframe)
                    # print(premium_name)
                    premium.saving_premiuns()
                    print("Premium saved.\n>")
                else:
                    print('[SKIP] Premium already in the database!')
                combination_step+=1
        else:
            print("Nothing to do.")
        
        print(".\n.\n=== CALCULATIONS COMPLETE! ===")

    ###
    ##
    #rate_risk_premiuns   
    ##
    ###
    if(rate_risk_premiuns):

        print(".\n..\n...\nRating Risk Premiuns!\n...\n..\n.")

        premium_name = indicators_dict.keys()
        len_premium_name = len(premium_name)

        list_combinations = finapp.calculate_combinations(premium_name, len_premium_name, single_combinations, double_combinations, triple_combinations)

        # if(len(list_combinations) > 0):

        print('Number of combinations: ', len(list_combinations))

        list_combination_file_name = finapp.create_file_names(list_combinations, indicators_dict)

        premium_name_dict = dict.fromkeys(list_combination_file_name, 1000000)
        
        print('.\n.\nPremium names dictionary: \n\t', premium_name_dict, '\n.\n.')

        rating_premiuns = rrp.MakeResultsPremium(final_analysis_date = "2021-12-31", factors_dict = premium_name_dict,
                                            file_name = r'..\\PDFs\avaliando-TOP10_INDICATORS.pdf')
        
        rating_premiuns.getting_premiuns()
        
        dataframe_columns = ['acum_primeiro_quartil', 'acum_segundo_quartil', 'acum_terceiro_quartil', 'acum_quarto_quartil', 'nome_indicador', 'ranking_indicators']
        ranking_indicator = pd.DataFrame(columns=dataframe_columns)

        ranking_indicator = rating_premiuns.retorno_quartis()
        print('.\n.\nIndicators ranking: ', ranking_indicator[['ranking_indicators', 'nome_indicador', 'acum_primeiro_quartil']])

        ranking_indicator = pd.DataFrame(ranking_indicator)

        list_premium_name = {especitif_key: valor['file_name'] for especitif_key, valor in indicators_dict.items() if 'file_name' in valor}
        list_premium_name = list(list_premium_name.values())

        top_indicators = ranking_indicator.head(number_of_top_comb_indicators)

        for premium_to_match in list_premium_name:

            for indicator in top_indicators['nome_indicador']:

                top_indicators[premium_to_match+'_Contido'] = top_indicators['nome_indicador'].apply(lambda x: premium_to_match in x)

        top_indicators['Pure'] = top_indicators['nome_indicador'].isin(list_premium_name)

        print('.\n.\ntop_indicators', number_of_top_comb_indicators, ': \n', top_indicators[['ranking_indicators', 'nome_indicador', 'acum_primeiro_quartil']])

        dataframe_columns = ['ranking_single_indicators', 'contagem', 'nome_indicador', 'acum_primeiro_quartil']
        distribution_indicadors = pd.DataFrame(columns = dataframe_columns)

        distribution_indicadors['nome_indicador'] = list_premium_name
        distribution_indicadors['contagem'] = 0

        ##corrigir abaixo para pegar o retorno acumulado do indicador puro
        distribution_indicadors['acum_primeiro_quartil'] = ranking_indicator['acum_primeiro_quartil']

        for i, indicator in enumerate(distribution_indicadors['nome_indicador']):
            indicator_presence = top_indicators[indicator+'_Contido'].sum()
            distribution_indicadors.loc[i, 'contagem'] = indicator_presence

        distribution_indicadors = distribution_indicadors.sort_values(by=['contagem','acum_primeiro_quartil'], ascending = [False, False])

        distribution_indicadors['ranking_single_indicators'] = distribution_indicadors['contagem'].rank(ascending=False)
        
        print('.\n.\ndistribution_indicadors: \n', distribution_indicadors)

        top_single_indicators = distribution_indicadors.head(number_of_top_single_indicators)

        print('.\n.\ntop_single_indicators', number_of_top_single_indicators, ': \n', top_single_indicators['nome_indicador'])

        best_indicator = ranking_indicator[ranking_indicator['ranking_indicators'] == 1]
        print('.\n.\nO melhor indicador até a data definida foi: ', str(best_indicator['nome_indicador'].iloc[-1]))
        print('\t rentabilidade acumulada do primeiro_quartil: ', int((best_indicator['acum_primeiro_quartil'].iloc[-1]) * 100), '%')
        print('\t rentabilidade acumulada do segundo_quartil: ', int((best_indicator['acum_segundo_quartil'].iloc[-1]) * 100), '%')
        print('\t rentabilidade acumulada do terceiro_quartil: ', int((best_indicator['acum_terceiro_quartil'].iloc[-1]) * 100), '%')
        print('\t rentabilidade acumulada do quarto_quartil: ', int((best_indicator['acum_quarto_quartil'].iloc[-1]) * 100), '%')

        list_premiuns_to_pdf = list(top_indicators['nome_indicador'])

        rating_premiuns.create_pdf_images(list_premiuns_to_pdf)
        rating_premiuns.fazer_pdf(list_premiuns_to_pdf)
        
        premiuns_to_regression_dict = dict.fromkeys(top_single_indicators['nome_indicador'], 1000000)

        print(".\n.\n=== RATING COMPLETE! ===")

    ###
    ##
    #regression_model
    ##
    ###
    if(execute_regression_model):

        print(".\n..\n...\nRunning Regression Model!\n...\n..\n.")

        fazendo_modelo = rm.linear_regression(data_final_analise= "2021-12-31", dicionario_fatores = premiuns_to_regression_dict, 
                                       caminho_premios_de_risco=R'./finapp/files/risk_premiuns',
                                       caminho_cdi = R'./finapp/files')

        fazendo_modelo.getting_premium_data()
        fazendo_modelo.calculating_universe()
        fazendo_modelo.execute_regression()
    ###
    ##
    #factor_calculator
    ##
    ###
    wallets_dict = {
        'carteira1': {
                'indicadores': {
                    #'momento_1_meses': {'caracteristica': 'decrescente'},
                    'momento_6_meses': {'caracteristica': 'decrescente'},
                    #'momento_12_meses': {'caracteristica': 'decrescente'},
                    # 'mm_7_40': {'caracteristica': 'decrescente'},
                    'ValorDeMercado': {'caracteristica': 'crescente'},
                    'EBIT_EV': {'caracteristica': 'decrescente'},
                    # 'ebit_dl': {'caracteristica': 'decrescente'},
                },
                'peso': 1
        },
        # 'carteira2': {
        #         'indicadores': {
        #             #'momento_1_meses': {'caracteristica': 'decrescente'},
        #             'momento_6_meses': {'caracteristica': 'decrescente'},
        #             #'momento_12_meses': {'caracteristica': 'decrescente'},
        #             #'mm_7_40': {'caracteristica': 'decrescente'},
        #             #'ValorDeMercado': {'caracteristica': 'crescente'},
        #             #'EBIT_EV': {'caracteristica': 'decrescente'},
        #             #'ebit_dl': {'caracteristica': 'decrescente'},
        #         },
        #         'peso': 0.3
        # }
        }
    
    rebalance_periods = 10
    liquidity_filter = 1
    asset_quantity = 10
    
    if(generate_wallets):

        print(".\n..\n...\nGenerating Wallet(s)!\n...\n..\n.")

        #before initialize class must define the name of the file
        pdf_name = ''

        print("Wallet(s) configuration:")

        for nome_carteira, carteira in wallets_dict.items():
                
                print("\t wallet: ", nome_carteira, '// peso: ', carteira['peso'] * 100, '%')

                pdf_name = pdf_name + nome_carteira + "_peso" + str(carteira['peso']).replace(".", "") + "_" 

                indicadores = carteira['indicadores']

                print("\t indicator(s): ")
                
                for indicador, ordem in indicadores.items():

                    print('\t\t', indicador)

                    pdf_name = pdf_name + indicador + "_"

        pdf_name = pdf_name + str(rebalance_periods) + '_' + str(liquidity_filter) + "M_" + str(asset_quantity) + "A.pdf"

        backtest = fc.MakeBacktest(data_final="2023-12-30", data_inicial= '2011-12-30', filtro_liquidez=(liquidity_filter * 1000000), balanceamento = rebalance_periods, 
                                    numero_ativos = asset_quantity, corretagem = 0.01, nome_arquivo = pdf_name, **wallets_dict)

        backtest.pegando_dados()
        backtest.filtrando_datas()
        backtest.criando_carteiras()
        wallets = backtest.calculando_retorno_diario()
        
        last_wallet = wallets.loc[wallets.index[-1]]
        last_wallet = last_wallet.reset_index()

        print('Last wallet defined below: \n', last_wallet)

        backtest.make_report()

        print(".\n.\n=== GENERATION COMPLETE! ===")

    ###
    ##
    #update requirements.txt file
    ##
    ###
    if(update_requirements_txt):

        print("initializing requirements update")
        requirements_update_command = "pip freeze"
        requirements_data = subprocess.check_output(requirements_update_command, shell=True, text=True)

        current_folder = os.getcwd()

        project_folder = os.getenv("PROJECT_FOLDER")

        if(current_folder != project_folder):
            os.chdir(project_folder)

        requirements_file_name = 'requirements.txt'
            
        full_desired_path = os.path.join(project_folder, requirements_file_name)

        with open(full_desired_path, "w") as arquivo:
            # print("deveria salvar")
            arquivo.write(requirements_data)