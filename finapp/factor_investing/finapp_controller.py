import download_fintz_data as dfd
import make_indicators as mi
import risk_premiuns as rp
import rate_risk_premiuns as rrp
import factor_calculator as fc
import market_premium as mp

import subprocess
import os
from dotenv import load_dotenv

if __name__ == "__main__":

    load_dotenv()

    update_database = False
    update_indicators = False
    calculate_risk_premiuns = True
    rate_risk_premiuns = False
    generate_wallets = False

    update_requirements_txt = False

    ###
    ##
    #download_fintz_data
    ##
    ###
    demonstration_list = [
                         'AcoesEmCirculacao', 'TotalAcoes',
                         #'PatrimonioLiquido',
                         #'LucroLiquido12m', 'LucroLiquido',
                         #'ReceitaLiquida', 'ReceitaLiquida12m', 
                         #'DividaBruta', 'DividaLiquida',
                         #'Disponibilidades', 
                         #'Ebit', 'Ebit12m',
                         #'Impostos', 'Impostos12m',
                         #'LucroLiquidoSociosControladora',
                         #'LucroLiquidoSociosControladora12m'
                         ]

    indicators_list = [
                        'L_P']#, 'ROE', 'ROIC', 'EV', 'LPA', 'P_L', 'EBIT_EV', 'ValorDeMercado']
    
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
                        'ValorDeMercado': 'crescente'
                        # 'ROIC': 'decrescente',
                        # 'ROE': 'decrescente',
                        # 'EBIT_EV': 'decrescente',
                        # 'L_P': 'decrescente',
                        # 'vol_252': 'crescente',
                        # 'ebit_dl': 'decrescente',
                        # 'pl_db': 'decrescente',
                        # 'mm_7_40': 'descrescente',
                        # 'momento_1_meses': 'decrescente',
                        # 'momento_6_meses': 'decrescente',
                        # 'momento_12_meses': 'decrescente'
                        }
                        
    # nome_premio = 'TAMANHO_VALOR_DE_MERCADO', 
    #                 'QUALITY_ROIC', QUALITY_ROE,
    #                 'VALOR_EBIT_EV', 'VALOR_L_P, 
    #                 'RISCO_VOL', 
    #                 'ALAVANCAGEM_EBIT_DL', 'ALAVANCAGEM_PL_DB',
    #                 'MOMENTO_MM_7_40', 'MOMENTO_R6M'

    # indicators_dict = {
    #                     'ValorDeMercado': ['TAMANHO_VALOR_DE_MERCADO','crescente'],
    #                     'ROIC': ['QUALITY_ROIC', 'decrescente'],
    #                     'ROE': ['QUALITY_ROE', 'decrescente'],
    #                     'EBIT_EV': ['VALOR_EBIT_EV', 'decrescente'],
    #                     'L_P': ['VALOR_L_P', 'decrescente'],
    #                     'vol_252': ['RISCO_VOL', 'crescente'],
    #                     'ebit_dl': ['ALAVANCAGEM_EBIT_DL', 'decrescente'],
    #                     'pl_db': ['ALAVANCAGEM_PL_DB', 'decrescente'],
    #                     'mm_7_40': ['MOMENTO_MM_7_40', 'descrescente'],
    #                     'momento_1_meses': ['MOMENTO_R1M', 'decrescente'],
    #                     'momento_6_meses': ['MOMENTO_R6M', 'decrescente'],
    #                     'momento_12_meses': ['MOMENTO_R12M', 'decrescente']
    #                     }

    if(calculate_risk_premiuns):

        print(".\n..\n...\nCalculating Risk Premiuns!\n...\n..\n.")
        beta = mp.MarketPremium()

        beta.calculate_market_premium()

        # for indicator in indicators_dict:
        #     valor = indicators_dict[indicator]

        premium = rp.RiskPremium(indicators_dict,  liquidity = 1000000, premium_name = 'TAMANHO_VALOR_DE_MERCADO')
        
        premium.getting_quotations()
        premium.getting_possible_dates()
        premium.filtering_volume()
        premium.getting_indicators()
        premium.discovering_initial_month()
        premium.calculating_premiuns()
        premium.saving_premiuns()
        
        print("=== CALCULATIONS COMPLETE! ===")

    ###
    ##
    #rate_risk_premiuns   
    ##
    ###
    factors_dict = {
                    #'QUALITY_ROIC': 1000000,
                    #'QUALITY_ROE': 1000000,
                    'VALOR_EBIT_EV': 1000000,
                    #'VALOR_L_P': 1000000,
                    #'ALAVANCAGEM_EBIT_DL': 1000000,
                    #'ALAVANCAGEM_PL_DB': 1000000,
                    'MOMENTO_R6M': 1000000,
                    #'MOMENTO_R1M': 1000000,
                    #'MOMENTO_R12M': 1000000,
                    #'MOMENTO_MM_7_40': 1000000,
                    'TAMANHO_VALOR_DE_MERCADO': 1000000,
                    #'RISCO_VOL': 1000000,
                    }

    if(rate_risk_premiuns):

        print(".\n..\n...\nRating Risk Premiuns!\n...\n..\n.")

        rating_premiuns = rrp.MakeResultsPremium(final_analysis_date = "2021-12-31", factors_dict = factors_dict,
                                            file_name = r'..\\PDFs\avaliando-VALOR_EBIT_EV-MOMENTO_R6M-TAMANHO_VALOR_DE_MERCADO.pdf')
        
        #rating_premiuns.getting_premiuns()
        #rating_premiuns.retorno_quartis()
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
                    #'ebit_dl': {'caracteristica': 'decrescente'}
                },
                'peso': 1

        },
        }
    
    rebalance_periods = 21
    liquidity_filter = 1
    asset_quantity = 6
    
    if(generate_wallets):

        print(".\n..\n...\nGenerating Wallet(s)!\n...\n..\n.")

        #before initialize class must define the name of the file
        pdf_name = ''

        for nome_carteira, carteira in wallets_dict.items():
                
                pdf_name = pdf_name + nome_carteira + "_peso" + str(carteira['peso']).replace(".", "") + "_" 

                indicadores = carteira['indicadores']

                for indicador, ordem in indicadores.items():

                    pdf_name = pdf_name + indicador + "_"

        pdf_name = pdf_name + str(rebalance_periods) + '_' + str(liquidity_filter) + "M_" + str(asset_quantity) + "A.pdf"

        backtest = fc.MakeBacktest(data_final="2021-12-31", data_inicial= '2011-12-30', filtro_liquidez=(liquidity_filter * 1000000), balanceamento=rebalance_periods, 
                                    numero_ativos=asset_quantity, corretagem=0.01, nome_arquivo = pdf_name, **wallets_dict)

        #backtest.pegando_dados()
        #backtest.filtrando_datas()
        #backtest.criando_carteiras()
        #backtest.calculando_retorno_diario()
        #backtest.make_report()

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