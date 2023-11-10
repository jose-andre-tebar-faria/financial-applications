from itertools import combinations

indicators_dict = {
                    'ValorDeMercado': {'file_name': 'TAMANHO_VALOR_DE_MERCADO', 'order': 'crescente'},
                    'ROIC': {'file_name': 'QUALITY_ROIC', 'order': 'decrescente'},
                    # 'ROE': {'file_name': 'QUALITY_ROE', 'order': 'decrescente'},
                    # 'EBIT_EV': {'file_name': 'VALOR_EBIT_EV', 'order': 'decrescente'},
                    # 'L_P': {'file_name': 'VALOR_L_P', 'order': 'decrescente'},
                    # 'vol_252': {'file_name': 'RISCO_VOL', 'order': 'crescente'},
                    # 'ebit_dl': {'file_name': 'ALAVANCAGEM_EBIT_DL', 'order': 'decrescente'},
                    # 'pl_db': {'file_name': 'ALAVANCAGEM_PL_DB', 'order': 'decrescente'},
                    'mm_7_40': {'file_name': 'MOMENTO_MM_7_40', 'order': 'descrescente'},
                    'momento_1_meses': {'file_name': 'MOMENTO_R1M', 'order': 'decrescente'},
                    'momento_6_meses': {'file_name': 'MOMENTO_R6M', 'order': 'decrescente'},
                    'momento_12_meses': {'file_name': 'MOMENTO_R12M', 'order': 'decrescente'},
                    }


desired_value = 'file_name'
premium_name = [file_name[desired_value] for file_name in indicators_dict.values()]
desired_value = 'order'
order = [order[desired_value] for order in indicators_dict.values()]

len_premium_name = len(premium_name)
all_combinations = []

if(len_premium_name >= 3):
    all_combinations = list(combinations(premium_name, 3))

    # Imprimir todas as combinações
    for combinacao in all_combinations:
        print(combinacao)
else:
    all_combinations = list(combinations(premium_name, len_premium_name))
    # Imprimir todas as combinações
    for combinacao in all_combinations:
        print(combinacao)


number_of_combinations = len(all_combinations)
#print(list_indicators)
#print(premium_name)
#print(order)
print(number_of_combinations)





combinations_list = []

remain_indicators_alpha = list(indicators_dict)
remain_indicators_beta = list(indicators_dict)
number_of_combinations = 0

list_indicators = list(indicators_dict)

















# for indicator_alfa in indicators_dict:

#     file_name_alfa = indicators_dict[indicator_alfa][0]
#     remain_indicators_beta = list(indicators_dict)

#     for indicator_beta in indicators_dict:
#         file_name_beta = indicators_dict[indicator_beta][0]

#         if(file_name_alfa != file_name_beta):

#             for indicator_gama in indicators_dict:
#                 file_name_gama = indicators_dict[indicator_gama][0]
                
#                 if((file_name_alfa != file_name_gama and file_name_beta != file_name_gama) and indicator_gama in remain_indicators_beta):
#                     file_name = file_name_alfa + '_' + file_name_beta + '_' + file_name_gama
#                     combinations_list.append(file_name)
#                     number_of_combinations+=1

#                     # print('remain_indicators_alpha = ', remain_indicators_alpha)
#                     # print('remain_indicators_beta = ', remain_indicators_beta)
#                     # print('indicator_alfa: ', indicator_alfa)
#                     # print('indicator_beta: ', indicator_beta)    
#                     # print('indicator_gama: ', indicator_gama)  
#                     print(file_name)

#         #if(len(remain_indicators_beta) > 0):
#         remain_indicators_beta.remove(indicator_beta)
#     remain_indicators_alpha.remove(indicator_alfa)

# print(combinations_list)
# print(number_of_combinations)