import download_by_fintz as dbf
import download_by_api as dba
import download_by_webscrapping as dbw
import make_indicators as mi
import risk_premiuns as rp
import rate_risk_premiuns as rrp
import factor_calculator as fc
import market_premium as mp
import regression_model as rm
import update_asset_profile as uap
import create_bcg_matrix as cbm
import wallet_manager as wm

import os
from dotenv import load_dotenv
import pandas as pd
from itertools import combinations
import subprocess
import numpy as np
from dateutil.relativedelta  import relativedelta
from datetime import datetime

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

    def prepare_data_for_rate_premiuns_risks(self, indicators_dict):
        
        premium_name = indicators_dict.keys()
        len_premium_name = len(premium_name)

        list_combinations = finapp.calculate_combinations(premium_name, len_premium_name, single_combinations, double_combinations, triple_combinations)

        print('Number of combinations: ', len(list_combinations))

        list_combination_file_name = finapp.create_file_names(list_combinations, indicators_dict)

        premium_name_dict = dict.fromkeys(list_combination_file_name, 1000000)
        
        print('.\n.\nPremium names dictionary: \n\t', premium_name_dict, '\n.\n.')

        return premium_name_dict

    def create_automatic_wallet(self, ranking_indicator):
        
        best_indicators_list = []

        best_indicators_list = list(ranking_indicator['nome_indicador'].head(number_of_top_indicators))
        print(f'\nOs {number_of_top_indicators} primeiros indicadores: \n', best_indicators_list)

        marker = '-with-'
        auto_wallet_dict = {}
        number_of_wallets = number_of_top_indicators
        wallet_proportion = 1/number_of_wallets

        default_wallet = {
                        'wallet-1': {'indicadores': {}, 'peso': 1}, 
                        'wallet-2': {'indicadores': {}, 'peso': 1},
                        'wallet-3': {'indicadores': {}, 'peso': 1},
                        'wallet-4': {'indicadores': {}, 'peso': 1},
                        }

        wallet_number = 1
        existing_wallets_list = []
        
        for indicators_comb in best_indicators_list:
            split_indicator = indicators_comb.split(marker)
            # print(split_indicator)

            indicators_list = []

            for file_name in split_indicator:

                chave_encontrada = None

                for chave, subdicionario in indicators_dict.items():
                    if 'file_name' in subdicionario and subdicionario['file_name'] == file_name:
                        chave_encontrada = chave
                        indicators_list.append(chave)
                        break
            print(f'\nindicators_list for wallet-{wallet_number}: ', indicators_list)

            for file_name in indicators_list:
                # print(file_name)
                # print(indicators_dict)

                if file_name in indicators_dict:
                    
                    order_value = indicators_dict[file_name]['order']
                    # print(order_value)

                    wallet_name = 'wallet-' + str(wallet_number)
                    # print(wallet_name)
                    default_wallet[wallet_name]['indicadores'][file_name] = {'caracteristica': order_value}
                    default_wallet[wallet_name]['peso'] = wallet_proportion
                    # print(auto_wallet_dict)
                    # print('\nWallet dict to append: \n', default_wallet)

                auto_wallet_dict.update(default_wallet)
                # print('\nAutomatic wallet dict created: \n', auto_wallet_dict)

            existing_wallets_list.append(wallet_name)
            # print(existing_wallets_list)
            wallet_number+=1

        print('\nExisting wallets in dict created: ', existing_wallets_list)

        setup_dict = {wallet: auto_wallet_dict[wallet] for wallet in existing_wallets_list}
        # print('\nAutomatic wallet dict created: \n', setup_dict)

        return setup_dict

    def compose_last_wallet_with_bcg_matrix(self, last_wallet, bcg_dimensions_list):
        
        last_wallet['ticker'] = last_wallet['ticker'].str[:4]
        last_wallet = last_wallet.rename(columns={'ticker': 'asset'})

        last_wallet = last_wallet.set_index('asset', drop=True)
        # last_wallet = last_wallet.drop(columns = 'index')
        # print(last_wallet)

        bcg_matrix_acess = cbm.BcgMatrix(bcg_dimensions_list)
        bcg_matrix = bcg_matrix_acess.read_bcg_matrix_database()

        bcg_matrix_df = pd.DataFrame(bcg_matrix)

        bcg_matrix_df = bcg_matrix_df.set_index('asset', drop=True)
        bcg_matrix_df = bcg_matrix_df.drop(columns = 'index')
        # print(bcg_matrix_df)
        
        final_analysis = pd.merge(bcg_matrix_df, last_wallet, on='asset')
        print('\nNightvision: \n', final_analysis.sort_values(by=['sector', 'subsector']))
        

        analysis_assets_list = list(final_analysis.index)
        print('\nWallet assets list: \n', analysis_assets_list)

        analysis_assets_list = [element + '3' for element in analysis_assets_list]

        return analysis_assets_list

    def calculate_wallet_returns_since_last_rebalance(self, analysis_assets_list):
        
        current_folder = os.getcwd()

        project_folder = os.getenv("PROJECT_FOLDER")
        databse_folder = os.getenv("DATABASE_FOLDER")
        full_desired_path = os.path.join(project_folder,databse_folder)

        if(current_folder != full_desired_path):
            os.chdir(full_desired_path)

        quotations_database_parquet = pd.read_parquet(f'{full_desired_path}/cotacoes.parquet')
        
        quotations_database = pd.DataFrame(quotations_database_parquet[['data', 'ticker', 'preco_fechamento_ajustado']][quotations_database_parquet['ticker'].isin(analysis_assets_list)])
        quotations_database['data'] = pd.to_datetime(quotations_database['data'])
        quotations_database.sort_values(['ticker', 'data'], inplace=True)

        last_analysis_date = quotations_database.loc[quotations_database.index[-1], 'data']
        last_analysis_date = pd.to_datetime(last_analysis_date)
        print('\nLast analysis date: ', last_analysis_date)

        days_since_last_periods = (last_analysis_date - last_wallet_rebalance_date).days

        quotations_database['last_period_variation'] = quotations_database.groupby('ticker')['preco_fechamento_ajustado'].pct_change(periods = days_since_last_periods) * 100

        last_period_variation = quotations_database.groupby('ticker')['last_period_variation'].last()
        print('\nAssets perc_change in rebalance_periods: \n', last_period_variation)

        print('\nNumber of assets in final wallet: ', len(analysis_assets_list))

        mean_last_period_variation = last_period_variation.mean()
        print(f'\nAvarage wallet rentability past {days_since_last_periods} periods: ', round(mean_last_period_variation,2) , '%')


if __name__ == "__main__":

    finapp = FinappController()

    # enable database update
    update_database                 = False
    update_api_database             = False
    update_fintz_database           = False
    update_webscrapping_database    = False


    # enable asset profile update
    update_asset_profile            = False


    # enable create BCG Matrix
    update_bcg_matrix               = False


    # enable indicators update
    update_indicators               = False


    # enable calculate risk premiuns database update
    calculate_risk_premiuns         = True
    # choose de indicators combinations to rate
    single_combinations             = True
    double_combinations             = True
    triple_combinations             = True
    # true if you want to update a existing file
    update_existing_file            = False


    # enable rating risks
    rate_risk_premiuns              = True
    final_analysis_date             = '2022-12-31'
    rating_premiuns_file_name       = r'..\\PDFs\avaliando-TOP10_INDICATORS.pdf'
    number_of_top_indicators        = 2
    # enable run a regression model
    execute_regression_model        = False


    # enable configure setup database
    config_setups                   = True
    read_setup                      = False
    save_setup                      = True
    close_setup                     = False
    delete_setup                    = False
    # setup configurations
    rebalance_periods               = 21
    liquidity_filter                = 1
    asset_quantity                  = 5
    user_name_adm                   = 'andre-tebar'


    # enable generation of wallet
    generate_wallets                = True
    factor_calc_initial_date        = '2019-12-31'
    factor_calc_end_date            = '2023-12-31'
    

    # enable configure wallet composition database
    config_wallet_composition       = True
    read_wallet_composition         = False
    save_wallet_composion           = True


    # enable requirements.txt update
    update_requirements_txt         = False

    ###
    ##
    #update_database
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

    fintz_indicators_list = [
                            'L_P', 'ROE', 'ROIC', 'EV', 'LPA', 'P_L', 'EBIT_EV', 'ValorDeMercado'
                            ]
    
    bc_dict = {
                'selic':    {'bc_code': '432'},
                'ipca':     {'bc_code': '433'},
                'dolar':    {'bc_code': '1'},
                }

    if(update_database):

        print(".\n..\n...\nUpdating Database!\n...\n..\n.")

        if(update_fintz_database):

            data_from_fintz = dbf.FintzData()

            for demonstration in demonstration_list:
                data_from_fintz.download_accounting_files(demonstration=True, data_name = demonstration)

            for indicator in fintz_indicators_list:
                data_from_fintz.download_accounting_files(indicator=True, data_name = indicator)

            data_from_fintz.download_cdi(initial_date="2000-01-01")
            data_from_fintz.download_ibov(initial_date="2000-01-01")
            data_from_fintz.download_quotations()
        
        if(update_api_database):

            data_from_api = dba.DownloadByApi()

            bc_data = data_from_api.getting_bc_data(bc_dict)

        if(update_webscrapping_database):

            data_from_webscrapping = dbw.DownloadByWebscrapping()

            b3_sectors = data_from_webscrapping.getting_b3_assets_sector_by_site()

        print(".\n.\n=== UPDATE COMPLETE! ===")

    ###
    ##
    #update_asset_profile
    ##
    ###
    if(update_asset_profile):

        print(".\n..\n...\nUpdating Asset Profile!\n...\n..\n.")

        profile_updater = uap.UpdateAssetProfile()

        profile_updater.getting_assets_database()
        profile_updater.getting_assets_from_quotation()
        profile_updater.calculationg_growth_rate()
        profile_updater.calculationg_marketshare()
        profile_updater.save_profile_database()

        profile_updater.read_profile_database()
   
    ###
    ##
    #bcg_matrix
    ##
    ###
    bcg_dimensions_list = [
                        'sector', 
                        'subsector',
                    ]

    if(update_bcg_matrix):

        print(".\n..\n...\nCreating BCG Matrix!\n...\n..\n.")

        bcg_matrix = cbm.BcgMatrix(bcg_dimensions_list)

        bcg_matrix.create_bcg_matrix()

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
                        'L_P':                {'file_name': 'VALOR_L_P',                  'order': 'decrescente'},
                        'vol_252':            {'file_name': 'RISCO_VOL',                  'order': 'crescente'},
                        # 'ebit_dl':            {'file_name': 'ALAVANCAGEM_EBIT_DL',        'order': 'decrescente'},
                        # 'pl_db':              {'file_name': 'ALAVANCAGEM_PL_DB',          'order': 'decrescente'},
                        # 'mm_7_40':            {'file_name': 'MOMENTO_MM_7_40',            'order': 'decrescente'},
                        # 'momento_1_meses':    {'file_name': 'MOMENTO_R1M',                'order': 'decrescente'},
                        'momento_6_meses':    {'file_name': 'MOMENTO_R6M',                'order': 'decrescente'},
                        # 'momento_12_meses':   {'file_name': 'MOMENTO_R12M',               'order': 'decrescente'},
                        }

    number_of_top_comb_indicators = 10

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

        premium_name_dict = finapp.prepare_data_for_rate_premiuns_risks(indicators_dict)

        rating_premiuns = rrp.MakeResultsPremium(final_analysis_date = final_analysis_date, factors_dict = premium_name_dict, file_name = rating_premiuns_file_name)
        
        rating_premiuns.getting_premiuns()
        
        dataframe_columns = ['acum_primeiro_quartil', 'acum_segundo_quartil', 'acum_terceiro_quartil', 'acum_quarto_quartil', 'nome_indicador', 'ranking_indicators']
        ranking_indicator = pd.DataFrame(columns=dataframe_columns)

        ranking_indicator = rating_premiuns.retorno_quartis()
        print('.\n.\nIndicators ranking: \n', ranking_indicator[['ranking_indicators', 'nome_indicador', 'acum_primeiro_quartil']])

        ranking_indicator = pd.DataFrame(ranking_indicator)

        list_premium_name = {especitif_key: valor['file_name'] for especitif_key, valor in indicators_dict.items() if 'file_name' in valor}
        list_premium_name = list(list_premium_name.values())

        top_indicators = ranking_indicator.head(number_of_top_comb_indicators)

        for premium_to_match in list_premium_name:

            for indicator in top_indicators['nome_indicador']:

                top_indicators[premium_to_match+'_Contido'] = top_indicators['nome_indicador'].apply(lambda x: premium_to_match in x)

        top_indicators['Pure'] = top_indicators['nome_indicador'].isin(list_premium_name)

        print('.\n.\ntop_indicators', number_of_top_comb_indicators, 'combinated: \n', top_indicators[['ranking_indicators', 'nome_indicador', 'acum_primeiro_quartil']])


        dataframe_columns = ['ranking_single_indicators', 'contagem', 'nome_indicador']
        distribution_indicadors = pd.DataFrame(columns = dataframe_columns)

        distribution_indicadors['nome_indicador'] = list_premium_name
        distribution_indicadors['contagem'] = 0

        distribution_indicadors = pd.merge(distribution_indicadors, ranking_indicator, on = 'nome_indicador', how = 'left')
        distribution_indicadors = distribution_indicadors.drop(columns=['acum_segundo_quartil', 'acum_terceiro_quartil', 'acum_quarto_quartil',  'ranking_indicators'])
        # print(distribution_indicadors)

        for i, indicator in enumerate(distribution_indicadors['nome_indicador']):
            indicator_presence = top_indicators[indicator+'_Contido'].sum()
            distribution_indicadors.loc[i, 'contagem'] = indicator_presence

        distribution_indicadors = distribution_indicadors.sort_values(by=['contagem','acum_primeiro_quartil'], ascending = [False, False])

        distribution_indicadors['ranking_single_indicators'] = distribution_indicadors['contagem'].rank(ascending=False)
        
        print('.\n.\ndistribution_indicadors: \n', distribution_indicadors)




        ##
        # CREATE AUTOMATIC PONDERATED WALLET
        ##
        setup_dict = finapp.create_automatic_wallet(ranking_indicator)


        ##
        # exibindo resultado do melhor indicador combinado
        ##
        best_indicator = ranking_indicator[ranking_indicator['ranking_indicators'] == 1]
        print('.\n.\nO melhor indicador até a data definida foi: ', str(best_indicator['nome_indicador'].iloc[-1]))
        print('\t rentabilidade acumulada do primeiro_quartil: ', int((best_indicator['acum_primeiro_quartil'].iloc[-1]) * 100), '%')
        print('\t rentabilidade acumulada do segundo_quartil: ', int((best_indicator['acum_segundo_quartil'].iloc[-1]) * 100), '%')
        print('\t rentabilidade acumulada do terceiro_quartil: ', int((best_indicator['acum_terceiro_quartil'].iloc[-1]) * 100), '%')
        print('\t rentabilidade acumulada do quarto_quartil: ', int((best_indicator['acum_quarto_quartil'].iloc[-1]) * 100), '%')



        #
        ##
        # CREATING PDF
        ##
        #
        # list_premiuns_to_pdf = list(top_indicators['nome_indicador'])
        # rating_premiuns.create_pdf_images(list_premiuns_to_pdf)
        # rating_premiuns.fazer_pdf(list_premiuns_to_pdf)




        #
        ##
        # PREPARING DATA FOR REGRESSION
        number_of_top_single_indicators = 3
        top_single_indicators = distribution_indicadors.head(number_of_top_single_indicators)
        # print('.\n.\ntop_single_indicators', number_of_top_single_indicators, ': \n', top_single_indicators['nome_indicador'])

        premiuns_to_regression_dict = dict.fromkeys(top_single_indicators['nome_indicador'], 1000000)




        print('\nAutomatic wallet dict created: \n', setup_dict)


        print(".\n.\n=== RATING COMPLETE! ===")

    ###
    ##
    #regression_model
    ##
    ###
    if(execute_regression_model):

        print(".\n..\n...\nRunning Regression Model!\n...\n..\n.")

        print('\nPremius to regression: \n', premiuns_to_regression_dict)

        fazendo_modelo = rm.linear_regression(data_final_analise= "2021-12-31", dicionario_fatores = premiuns_to_regression_dict, 
                                       caminho_premios_de_risco=R'./finapp/files/risk_premiuns',
                                       caminho_cdi = R'./finapp/files')

        fazendo_modelo.getting_premium_data()
        fazendo_modelo.calculating_universe()
        fazendo_modelo.execute_regression()

    ###
    ##
    # save setup in database
    ##
    ###

    create_date_auto = datetime.now()
    create_date_auto = create_date_auto.strftime('%Y-%m-%d')

    if(config_setups):

        wallet_manager = wm.WalletManager()
        
        wallet_id_existent = None
        new_wallet_id = None
        wallet_existent = False

        if(read_setup):

            wallet_manager.read_setups()

        if(save_setup):
            
            new_setup_to_insert = wallet_manager.preparing_setup_data(setups_dict = setup_dict, number_of_assets = asset_quantity, rebalance_periods = rebalance_periods, user_name = user_name_adm, create_date = create_date_auto)

            wallet_id, wallet_existent = wallet_manager.insert_setup(wallet_manager = wallet_manager, new_setup = new_setup_to_insert)
            # print('wallet_id_existent', wallet_id_existent)
            # print('new_wallet_id', new_wallet_id)

        if(close_setup):

            wallet_manager.close_setup(wallet_id='first-shot', user_name='pacient-zero', close_date = '2023-11-22')

        if(delete_setup):

            wallet_manager.delete_setup(wallet_manager = wallet_manager, wallet_id='227', user_name='andre-tebar')
    
    ###
    ##
    #factor_calculator
    ##
    ###
    if(generate_wallets):

        print(".\n..\n...\nGenerating Wallet(s)!\n...\n..\n.")

        #before initialize class must define the name of the file
        pdf_name = ''

        print("Setup configuration =")

        for nome_carteira, carteira in setup_dict.items():
                
                print("\n\t", nome_carteira, '\n\t\t peso: ', carteira['peso'] * 100, '%')

                pdf_name = pdf_name + nome_carteira + "_peso" + str(carteira['peso']).replace(".", "") + "_" 

                indicadores = carteira['indicadores']

                print("\t\t indicator(s): ")
                
                for indicador, ordem in indicadores.items():

                    print('\t\t\t', indicador)

                    pdf_name = pdf_name + indicador + "_"

        print('\n\tAssets per wallet: ', asset_quantity)
        print('\n\tRebalance periods: ', rebalance_periods)

        pdf_name = pdf_name + str(rebalance_periods) + '_' + str(liquidity_filter) + "M_" + str(asset_quantity) + "A.pdf"

        backtest = fc.MakeBacktest(data_final = factor_calc_end_date, data_inicial = factor_calc_initial_date, 
                                   filtro_liquidez=(liquidity_filter * 1000000), balanceamento = rebalance_periods, 
                                   numero_ativos = asset_quantity, corretagem = 0.01, nome_arquivo = pdf_name, **setup_dict)

        backtest.pegando_dados()
        backtest.filtrando_datas()
        backtest.criando_carteiras()
        wallets = backtest.calculando_retorno_diario()
        
        last_wallet = wallets.loc[wallets.index[-1]]
        last_wallet = last_wallet.reset_index()
        print('\nLast wallet defined below: \n', last_wallet)
        
        last_wallet_rebalance_date = last_wallet.loc[last_wallet.index[-1], 'data']
        last_wallet_rebalance_date = pd.to_datetime(last_wallet_rebalance_date)
        print('\nLast wallet rebalance_date: ', last_wallet_rebalance_date)
        
        #
        ##
        ###
        # CREATE PDF REPORT
        ###
        ##
        #
        # backtest.make_report()


        #
        ## prepara a última carteira definida para salvar
        #
        wallet_to_database = last_wallet
        wallet_to_database = wallet_to_database.reset_index(drop=True)
        wallet_to_database.rename(columns={'asset': 'ticker', 'data': 'rebalance_date', 'peso': 'wallet_proportion'}, inplace=True)
        wallet_to_database['rebalance_date'] = pd.to_datetime(wallet_to_database['rebalance_date'])
        # print('\nwallet_to_database:\n', wallet_to_database)

        #
        ## [OPTIONAL] une a matrix BCG (bcg_matrix) aos últimos resultados da carteira
        #
        # analysis_assets_list = finapp.compose_last_wallet_with_bcg_matrix(last_wallet, bcg_dimensions_list)
        
        #
        ## [OPTIONAL] calcula o rendimento de cada ativo e médio desde o último rebalanciamento da carteira
        #
        # finapp.calculate_wallet_returns_since_last_rebalance(analysis_assets_list)

        print(".\n.\n=== GENERATION COMPLETE! ===")

    ###
    ##
    # configure wallet composition
    ##
    ###
    if(config_wallet_composition):

        wallet_manager = wm.WalletManager()

        if wallet_existent is False:
            print('\n ---no wallet defined or found! forcing save_wallet_composion to FALSE...\n')
            wallet_id = str(wallet_id)
            save_wallet_composion = False

        if(read_wallet_composition):
            
            file_not_found, compositions_df = wallet_manager.read_portifolios_composition()
        
        if(save_wallet_composion):

            print('\nWallet to database: \n', wallet_to_database)

            wallet_manager.update_portifolio_composition(wallet_manager = wallet_manager, wallet_id = wallet_id, wallet_defined = wallet_to_database)

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
            arquivo.write(requirements_data)