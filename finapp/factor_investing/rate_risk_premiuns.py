import pandas as pd
import numpy as np
import mplcyberpunk 
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from report_pdf_fatores import MakePDF
import os
import matplotlib
matplotlib.rcParams.update({'font.size': 9})
import datetime
from dotenv import load_dotenv

plt.style.use("cyberpunk")

class MakeResultsPremium:

    def __init__(self, factors_dict, final_analysis_date, file_name = 'premios_de_risco.pdf'):
                
        print("Inicializing MakeResultPremium!")

        load_dotenv()

        self.factors_dict = factors_dict
        self.lista_nome_fatores = []
        self.liquidez = []

        for key, item in factors_dict.items():
            self.lista_nome_fatores.append(key)
            self.liquidez.append(item)
            
        self.final_analysis_date = (datetime.datetime.strptime(final_analysis_date, '%Y-%m-%d')).date()
        self.file_name = file_name

        print("OK.")

    def getting_premiuns(self):

        lista_dfs = []
        data_inicial = []
        
        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.databse_folder = os.getenv("PREMIUNS_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.databse_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

        for i, nome_premio in enumerate(self.lista_nome_fatores):

            df = pd.read_parquet(f'{self.full_desired_path}/{nome_premio}_{self.liquidez[i]}.parquet')
            df['data'] = pd.to_datetime(df['data']).dt.date

            lista_dfs.append(df)
            data_inicial.append(min(df['data']))

        self.premios_de_risco = pd.concat(lista_dfs)
        data_inicial = max(data_inicial)

        self.premios_de_risco = self.premios_de_risco[(self.premios_de_risco['data'] >= data_inicial) &
                                                      (self.premios_de_risco['data'] <= self.final_analysis_date)]

        self.premios_de_risco = self.premios_de_risco.assign(premio_fator = 
                                                             (1 + self.premios_de_risco['primeiro_quartil'])/(1 + self.premios_de_risco['quarto_quartil'])) 
        
        self.premios_de_risco['primeiro_quartil'] = 1 + self.premios_de_risco['primeiro_quartil'] 
        self.premios_de_risco['segundo_quartil'] = 1 + self.premios_de_risco['segundo_quartil'] 
        self.premios_de_risco['terceiro_quartil'] = 1 + self.premios_de_risco['terceiro_quartil'] 
        self.premios_de_risco['quarto_quartil'] = 1 + self.premios_de_risco['quarto_quartil'] 
        self.premios_de_risco['universo'] = 1 + self.premios_de_risco['universo'] 

    def retorno_quartis(self):

        df_primeiro_quartis = pd.DataFrame(index = self.premios_de_risco['data'].unique())
        df_premios_de_risco = pd.DataFrame(index = self.premios_de_risco['data'].unique())

        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.databse_folder = os.getenv("IMAGES_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.databse_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

        dataframe_columns = ['acum_primeiro_quartil', 'acum_segundo_quartil', 'acum_terceiro_quartil', 'acum_quarto_quartil', 'nome_indicador']
        ranking_indicator = pd.DataFrame(columns=dataframe_columns)

        for i, nome_premio in enumerate(self.lista_nome_fatores):

            #print("lista_nome_fatores: ", self.lista_nome_fatores)
            #print("nome_premio; ", nome_premio)
            #print("i: ", i)
            #print("premio_de_risco: ", self.premios_de_risco)

            fator = self.premios_de_risco[(self.premios_de_risco['nome_premio'] == nome_premio) &
                                            (self.premios_de_risco['liquidez'] == self.liquidez[i])]

            tamanho_fator = len(fator['primeiro_quartil'])
            #print("tamanho_fator: ", tamanho_fator)
        
            if tamanho_fator != 0:

                acum_primeiro_quartil = (fator['primeiro_quartil'].cumprod() - 1).iloc[-1]
                acum_segundo_quartil = (fator['segundo_quartil'].cumprod() - 1).iloc[-1]
                acum_terceiro_quartil = (fator['terceiro_quartil'].cumprod() - 1).iloc[-1]
                acum_quarto_quartil = (fator['quarto_quartil'].cumprod() - 1).iloc[-1]
                
                factor_name = (fator['nome_premio']).iloc[-1]

                ranking_indicator.loc[i, 'nome_indicador'] = factor_name
                ranking_indicator.loc[i, 'acum_primeiro_quartil'] = acum_primeiro_quartil
                ranking_indicator.loc[i, 'acum_segundo_quartil'] = acum_segundo_quartil
                ranking_indicator.loc[i, 'acum_terceiro_quartil'] = acum_terceiro_quartil
                ranking_indicator.loc[i, 'acum_quarto_quartil'] = acum_quarto_quartil

                ranking_indicator['ranking_indicators'] = ranking_indicator['acum_primeiro_quartil'].rank(ascending=False)
                ranking_indicator.sort_values('ranking_indicators', ascending=True, inplace=True)

                fig, ax = plt.subplots(figsize = (4.75, 4))

                ax.bar(0, acum_primeiro_quartil)
                ax.bar(1, acum_segundo_quartil)
                ax.bar(2, acum_terceiro_quartil)
                ax.bar(3, acum_quarto_quartil)

                ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

                plt.xticks([0, 1, 2, 3], ['1º Quartil', '2º Quartil', '3º Quartil', '4º Quartil'])

                plt.title(nome_premio)
                        
                #diretorio_atual = os.getcwd()
                #print("Diretório atual:", diretorio_atual)

                plt.savefig(f'{self.full_desired_path}/barras_quartis_{nome_premio}_{self.liquidez[i]}')

                plt.close()

                fig, ax = plt.subplots(figsize = (4.75, 4))

                #print(fator['primeiro_quartil'].iloc[-1])

                ax.plot(fator['data'].values, (fator['primeiro_quartil'].cumprod() - 1), label = '1º Quartil')
                ax.plot(fator['data'].values, (fator['segundo_quartil'].cumprod() - 1), label = '2º Quartil')
                ax.plot(fator['data'].values, (fator['terceiro_quartil'].cumprod() - 1), label = '3º Quartil')
                ax.plot(fator['data'].values, (fator['quarto_quartil'].cumprod() - 1), label = '4º Quartil')
                ax.plot(fator['data'].values, (fator['universo'].cumprod() - 1), label = 'Universo')

                plt.legend()

                ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

                plt.title(nome_premio)

                plt.savefig(f'{self.full_desired_path}/linha_quartis_{nome_premio}_{self.liquidez[i]}')

                plt.close()

                #graifco de prêmio do fator

                fig, ax = plt.subplots(figsize = (4.75, 4))

                ax.plot(fator['data'].values, (fator['premio_fator'].cumprod() - 1))

                ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

                plt.title(nome_premio + " 1º Quartil minus 4º quartil")

                plt.savefig(f'{self.full_desired_path}/premio_de_risco_{nome_premio}_{self.liquidez[i]}')

                plt.close()

                #janela movel

                serie_movel = pd.Series(data = fator['premio_fator'].rolling(12).apply(np.prod, raw = True) - 1)

                serie_movel.index = fator['data'].values

                serie_movel = serie_movel.dropna()

                fig, ax = plt.subplots(figsize = (4.75, 4))

                ax.plot(serie_movel.index, serie_movel.values)

                ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

                plt.title(nome_premio + " Janela móvel 12M")

                plt.savefig(f'{self.full_desired_path}/movel_12m_premio_de_risco_{nome_premio}_{self.liquidez[i]}')

                plt.close()

                df_primeiro_quartis.loc[:, f"{nome_premio}"] = (fator['primeiro_quartil'].cumprod() - 1).values
                df_premios_de_risco.loc[:, f"{nome_premio}"] = (fator['premio_fator'].cumprod() - 1).values

        #print('fator: ', fator)

        matplotlib.rcParams.update({'font.size': 11})

        fig, ax = plt.subplots(figsize = (9, 4.5))

        for coluna in df_primeiro_quartis.columns:

            ax.plot(df_primeiro_quartis.index, df_primeiro_quartis[coluna].values, label = f'{coluna}')

        plt.legend()

        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        plt.title('Comparação entre 1º quartil')

        plt.savefig(f'{self.full_desired_path}/comparando_1Q')

        plt.close()

        fig, ax = plt.subplots(figsize = (9, 4.5))

        #print(df_premios_de_risco)

        for coluna in df_premios_de_risco.columns:

            ax.plot(df_premios_de_risco.index, df_premios_de_risco[coluna].values, label = f'{coluna}')

        plt.legend()

        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        plt.title('Comparação entre prêmios de risco')

        plt.savefig(f'{self.full_desired_path}/comparando_premios')

        plt.close()

        self.matriz_correl = df_premios_de_risco.corr()
        
        return ranking_indicator

    def fazer_pdf(self):

        MakePDF(fatores = self.lista_nome_fatores, liquidez = self.liquidez, matriz_correl = self.matriz_correl,
                nome_arquivo=self.file_name)
           
if __name__ == "__main__":

    factors_dict = {
                          'QUALITY_ROIC': 1000000,
                          #'QUALITY_ROE': 1000000,
                          #'VALOR_EBIT_EV': 1000000,
                          #'VALOR_L_P': 1000000,
                          #'ALAVANCAGEM_EBIT_DL': 1000000,
                          #'ALAVANCAGEM_PL_DB': 1000000,
                          #'MOMENTO_R6M': 1000000,
                          #'MOMENTO_R1M': 1000000,
                          #'MOMENTO_R12M': 1000000,
                          #'MOMENTO_MM_7_40': 1000000,
                          'TAMANHO_VALOR_DE_MERCADO': 1000000,
                          #'RISCO_VOL': 1000000,
                          'TAMANHO_VALOR_DE_MERCADO-QUALITY_ROIC': 1000000,
                          'TAMANHO_VALOR_DE_MERCADO_VALOR_EBIT_EV_MOMENTO_R6M': 1000000,
                           }

    premios = MakeResultsPremium(final_analysis_date="2021-12-31", factors_dict=factors_dict,
                                 file_name = r'..\\PDFs\avaliando-COMBINACOES.pdf')

    #diretorio_atual = os.getcwd()
    #print("Diretório atual antes puxar_dados:", diretorio_atual)

    premios.getting_premiuns()
    premios.retorno_quartis()
    premios.fazer_pdf()