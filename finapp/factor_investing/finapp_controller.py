import download_fintz_data as dfd
import make_indicators as mi
import risk_premiuns as rp
import rate_risk_premiuns as rrp
import factor_calculator as fc
import market_premium as mp

import pandas as pd
import subprocess
import os
from dotenv import load_dotenv

if __name__ == "__main__":

    load_dotenv()

    update_database = False
    update_indicators = False
    calculate_risk_premiuns = False
    rate_risk_premiuns = True
    generate_wallets = False

    update_requirements_txt = False

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
        
        print("=== UPDATE COMPLETE! ===")

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
        
        print("=== UPDATE COMPLETE! ===")



    #risk_premiuns
    ##
    ###
    indicators_dict = {
                        'ValorDeMercado': {'file_name': 'TAMANHO_VALOR_DE_MERCADO', 'order': 'crescente'},
                        # 'ROIC': {'file_name': 'QUALITY_ROIC', 'order': 'decrescente'},
                        # 'ROE': {'file_name': 'QUALITY_ROE', 'order': 'decrescente'},
                        'EBIT_EV': {'file_name': 'VALOR_EBIT_EV', 'order': 'decrescente'},
                        # 'L_P': {'file_name': 'VALOR_L_P', 'order': 'decrescente'},
                        # 'vol_252': {'file_name': 'RISCO_VOL', 'order': 'crescente'},
                        # 'ebit_dl': {'file_name': 'ALAVANCAGEM_EBIT_DL', 'order': 'decrescente'},
                        # 'pl_db': {'file_name': 'ALAVANCAGEM_PL_DB', 'order': 'decrescente'},
                        # 'mm_7_40': {'file_name': 'MOMENTO_MM_7_40', 'order': 'descrescente'},
                        # 'momento_1_meses': {'file_name': 'MOMENTO_R1M', 'order': 'decrescente'},
                         'momento_6_meses': {'file_name': 'MOMENTO_R6M', 'order': 'decrescente'},
                        # 'momento_12_meses': {'file_name': 'MOMENTO_R12M', 'order': 'decrescente'}
                        }

    if(calculate_risk_premiuns):

        print(".\n..\n...\nCalculating Risk Premiuns!\n...\n..\n.")
        beta = mp.MarketPremium()

        beta.calculate_market_premium()

        desired_value = 'file_name'
        premium_name = [file_name[desired_value] for file_name in indicators_dict.values()]
        premium_name = '_'.join(premium_name)

        premium = rp.RiskPremium(indicators_dict, premium_name, liquidity = 1000000)
        
        premium.getting_quotations()
        premium.getting_possible_dates()
        premium.filtering_volume()
        premium.getting_indicators()
        premium.discovering_initial_month()
        premium_dataframe = premium.calculating_premiuns()

        #print(premium_dataframe)
        # premium.saving_premiuns()
        
        print("=== CALCULATIONS COMPLETE! ===")

    ###
    ##
    #rate_risk_premiuns   
    ##
    ###
    factors_dict = {
                    'QUALITY_ROIC': 1000000,
                    'QUALITY_ROE': 1000000,
                    'VALOR_EBIT_EV': 1000000,
                    'VALOR_L_P': 1000000,
                    'ALAVANCAGEM_EBIT_DL': 1000000,
                    'ALAVANCAGEM_PL_DB': 1000000,
                    'MOMENTO_R6M': 1000000,
                    'MOMENTO_R1M': 1000000,
                    'MOMENTO_R12M': 1000000,
                    'MOMENTO_MM_7_40': 1000000,
                    'TAMANHO_VALOR_DE_MERCADO': 1000000,
                    'RISCO_VOL': 1000000,
                    'TAMANHO_VALOR_DE_MERCADO-QUALITY_ROIC': 1000000,
                    'TAMANHO_VALOR_DE_MERCADO_VALOR_EBIT_EV_MOMENTO_R6M': 1000000,
                    }

    if(rate_risk_premiuns):

        print(".\n..\n...\nRating Risk Premiuns!\n...\n..\n.")

        rating_premiuns = rrp.MakeResultsPremium(final_analysis_date = "2016-12-31", factors_dict = factors_dict,
                                            file_name = r'..\\PDFs\avaliando-MULTIPLE_INDICATORS.pdf')
        
        rating_premiuns.getting_premiuns()
        
        dataframe_columns = ['acum_primeiro_quartil', 'acum_segundo_quartil', 'acum_terceiro_quartil', 'acum_quarto_quartil', 'nome_indicador', 'ranking_indicators']
        ranking_indicator = pd.DataFrame(columns=dataframe_columns)

        ranking_indicator = rating_premiuns.retorno_quartis()
        print("Indicators ranking: ")
        print(ranking_indicator[['ranking_indicators', 'nome_indicador', 'acum_primeiro_quartil']])

        ranking_indicator = pd.DataFrame(ranking_indicator)
        best_indicator = ranking_indicator[ranking_indicator['ranking_indicators'] == 1]
        
        print('.\n.\nO melhor indicador até a data definida foi: ', str(best_indicator['nome_indicador'].iloc[-1]))
        print('\t rentabilidade acumulada do primeiro_quartil: ', int((best_indicator['acum_primeiro_quartil'].iloc[-1]) * 100), '%')
        print('\t rentabilidade acumulada do segundo_quartil: ', int((best_indicator['acum_segundo_quartil'].iloc[-1]) * 100), '%')
        print('\t rentabilidade acumulada do terceiro_quartil: ', int((best_indicator['acum_terceiro_quartil'].iloc[-1]) * 100), '%')
        print('\t rentabilidade acumulada do quarto_quartil: ', int((best_indicator['acum_quarto_quartil'].iloc[-1]) * 100), '%')
        
        #rating_premiuns.fazer_pdf()
        
        print("=== RATING COMPLETE! ===")

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
                    #'mm_7_40': {'caracteristica': 'decrescente'},
                    'ValorDeMercado': {'caracteristica': 'crescente'},
                    'EBIT_EV': {'caracteristica': 'decrescente'},
                    #'ebit_dl': {'caracteristica': 'decrescente'},
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
    asset_quantity = 5
    
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

        backtest = fc.MakeBacktest(data_final="2016-12-30", data_inicial= '2011-12-30', filtro_liquidez=(liquidity_filter * 1000000), balanceamento = rebalance_periods, 
                                    numero_ativos = asset_quantity, corretagem = 0.01, nome_arquivo = pdf_name, **wallets_dict)

        backtest.pegando_dados()
        backtest.filtrando_datas()
        backtest.criando_carteiras()
        wallets = backtest.calculando_retorno_diario()
        
        last_wallet = wallets.loc[wallets.index[-1]]
        last_wallet = last_wallet.reset_index()

        print('Last wallet defined below: \n', last_wallet)

        backtest.make_report()

        print("=== GENERATION COMPLETE! ===")

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
            #print("deveria salvar")
            arquivo.write(requirements_data)