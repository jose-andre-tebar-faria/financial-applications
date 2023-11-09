from itertools import product

indicators_dict = {
                    'ValorDeMercado': ['TAMANHO_VALOR_DE_MERCADO','crescente'],
                    'ROIC': ['QUALITY_ROIC', 'decrescente'],
                    'ROE': ['QUALITY_ROE', 'decrescente'],
                    'EBIT_EV': ['VALOR_EBIT_EV', 'decrescente'],
                    'L_P': ['VALOR_L_P', 'decrescente'],
                    'vol_252': ['RISCO_VOL', 'crescente'],
                    'ebit_dl': ['ALAVANCAGEM_EBIT_DL', 'decrescente'],
                    'pl_db': ['ALAVANCAGEM_PL_DB', 'decrescente'],
                    'mm_7_40': ['MOMENTO_MM_7_40', 'descrescente'],
                    'momento_1_meses': ['MOMENTO_R1M', 'decrescente'],
                    'momento_6_meses': ['MOMENTO_R6M', 'decrescente'],
                    'momento_12_meses': ['MOMENTO_R12M', 'decrescente']
                    }

# indicators_dict = {
#                         'ValorDeMercado': 'crescente',
#                         'ROIC': 'decrescente',
#                         'ROE': 'decrescente',
#                         'EBIT_EV': 'decrescente',
#                         'L_P': 'decrescente',
#                         'vol_252': 'crescente',
#                         'ebit_dl': 'decrescente',
#                         'pl_db': 'decrescente',
#                         'mm_7_40': 'descrescente',
#                         'momento_1_meses': 'decrescente',
#                         'momento_6_meses': 'decrescente',
#                         'momento_12_meses': 'decrescente'
#                         }

combinations_list = []

remain_indicators_alpha = list(indicators_dict)
remain_indicators_beta = list(indicators_dict)
number_of_combinations = 0

for indicator_alfa in indicators_dict:

    remain_indicators_beta = list(indicators_dict)

    for indicator_beta in indicators_dict:
        
        for indicator_gama in indicators_dict:
            file_name_alfa = indicators_dict[indicator_alfa][0]
            file_name_beta = indicators_dict[indicator_beta][0]
            file_name_gama = indicators_dict[indicator_gama][0]

            file_name = file_name_alfa + '_' + file_name_beta + '_' + file_name_gama
            combinations_list.append(file_name)
            number_of_combinations+=1
            #print(file_name)

        remain_indicators_beta.remove(indicator_beta)
        print(remain_indicators_beta)
        print(remain_indicators_alpha)

    remain_indicators_alpha.remove(indicator_alfa)

#print(combinations_list)
print(number_of_combinations)