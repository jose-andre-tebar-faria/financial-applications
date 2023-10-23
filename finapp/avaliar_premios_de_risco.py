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

plt.style.use("cyberpunk")

class MakeResultsPremium:

    def __init__(self, dicionario_fatores, data_final_analise, caminho_imagens, nome_arquivo = 'premios_de_risco.pdf', 
                 caminho_premios_de_risco = '.'):
        
        
        self.dicionario_fatores = dicionario_fatores
        self.lista_nome_fatores = []
        self.liquidez = []
        self.caminho_premios_de_risco = caminho_premios_de_risco

        for key, item in dicionario_fatores.items():
            
            self.lista_nome_fatores.append(key)
            self.liquidez.append(item)
            

        self.data_final_analise = (datetime.datetime.strptime(data_final_analise, '%Y-%m-%d')).date()
        self.caminho_imagens = caminho_imagens
        self.nome_arquivo = nome_arquivo
        os.chdir(caminho_imagens)

    def puxando_dados(self):

        lista_dfs = []
        data_inicial = []
        
        for i, nome_premio in enumerate(self.lista_nome_fatores):

            df = pd.read_parquet(f'{self.caminho_premios_de_risco}/{nome_premio}_{self.liquidez[i]}.parquet')
            df['data'] = pd.to_datetime(df['data']).dt.date

            lista_dfs.append(df)
            data_inicial.append(min(df['data']))

        self.premios_de_risco = pd.concat(lista_dfs)
        data_inicial = max(data_inicial)

        self.premios_de_risco = self.premios_de_risco[(self.premios_de_risco['data'] >= data_inicial) &
                                                      (self.premios_de_risco['data'] <= self.data_final_analise)]

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

        for i, nome_premio in enumerate(self.lista_nome_fatores):

            fator = self.premios_de_risco[(self.premios_de_risco['nome_premio'] == nome_premio) &
                                            (self.premios_de_risco['liquidez'] == self.liquidez[i])]

            acum_primeiro_quartil = (fator['primeiro_quartil'].cumprod() - 1).iloc[-1]
            acum_segundo_quartil = (fator['segundo_quartil'].cumprod() - 1).iloc[-1]
            acum_terceiro_quartil = (fator['terceiro_quartil'].cumprod() - 1).iloc[-1]
            acum_quarto_quartil = (fator['quarto_quartil'].cumprod() - 1).iloc[-1]
            
            fig, ax = plt.subplots(figsize = (4.75, 4))

            ax.bar(0, acum_primeiro_quartil)
            ax.bar(1, acum_segundo_quartil)
            ax.bar(2, acum_terceiro_quartil)
            ax.bar(3, acum_quarto_quartil)

            ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

            plt.xticks([0, 1, 2, 3], ['1º Quartil', '2º Quartil', '3º Quartil', '4º Quartil'])

            plt.title(nome_premio)

            plt.savefig(f'{self.caminho_imagens}/barras_quartis_{nome_premio}_{self.liquidez[i]}')

            plt.close()

            fig, ax = plt.subplots(figsize = (4.75, 4))

            ax.plot(fator['data'].values, (fator['primeiro_quartil'].cumprod() - 1), label = '1º Quartil')
            ax.plot(fator['data'].values, (fator['segundo_quartil'].cumprod() - 1), label = '2º Quartil')
            ax.plot(fator['data'].values, (fator['terceiro_quartil'].cumprod() - 1), label = '3º Quartil')
            ax.plot(fator['data'].values, (fator['quarto_quartil'].cumprod() - 1), label = '4º Quartil')
            ax.plot(fator['data'].values, (fator['universo'].cumprod() - 1), label = 'Universo')

            plt.legend()

            ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

            plt.title(nome_premio)

            plt.savefig(f'{self.caminho_imagens}/linha_quartis_{nome_premio}_{self.liquidez[i]}')

            plt.close()

            #graifco de prêmio do fator

            fig, ax = plt.subplots(figsize = (4.75, 4))

            ax.plot(fator['data'].values, (fator['premio_fator'].cumprod() - 1))

            ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

            plt.title(nome_premio + " 1º Quartil minus 4º quartil")

            plt.savefig(f'{self.caminho_imagens}/premio_de_risco_{nome_premio}_{self.liquidez[i]}')

            plt.close()

            #janela movel

            serie_movel = pd.Series(data = fator['premio_fator'].rolling(12).apply(np.prod, raw = True) - 1)

            serie_movel.index = fator['data'].values

            serie_movel = serie_movel.dropna()

            fig, ax = plt.subplots(figsize = (4.75, 4))

            ax.plot(serie_movel.index, serie_movel.values)

            ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

            plt.title(nome_premio + " Janela móvel 12M")

            plt.savefig(f'{self.caminho_imagens}/movel_12m_premio_de_risco_{nome_premio}_{self.liquidez[i]}')

            plt.close()

            df_primeiro_quartis.loc[:, f"{nome_premio}"] = (fator['primeiro_quartil'].cumprod() - 1).values
            df_premios_de_risco.loc[:, f"{nome_premio}"] = (fator['premio_fator'].cumprod() - 1).values

        matplotlib.rcParams.update({'font.size': 11})

        fig, ax = plt.subplots(figsize = (9, 4.5))

        for coluna in df_primeiro_quartis.columns:

            ax.plot(df_primeiro_quartis.index, df_primeiro_quartis[coluna].values, label = f'{coluna}')

        plt.legend()

        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        plt.title('Comparação entre 1º quartil')

        plt.savefig(f'{self.caminho_imagens}/comparando_1Q')

        plt.close()

        fig, ax = plt.subplots(figsize = (9, 4.5))

        for coluna in df_premios_de_risco.columns:

            ax.plot(df_premios_de_risco.index, df_premios_de_risco[coluna].values, label = f'{coluna}')

        plt.legend()

        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        plt.title('Comparação entre prêmios de risco')

        plt.savefig(f'{self.caminho_imagens}/comparando_premios')

        plt.close()

        self.matriz_correl = df_premios_de_risco.corr()

    
    def fazer_pdf(self):

        MakePDF(fatores = self.lista_nome_fatores, liquidez = self.liquidez, matriz_correl = self.matriz_correl,
                caminho_imagens=self.caminho_imagens, nome_arquivo=self.nome_arquivo)
           

        


if __name__ == "__main__":

    dicionario_fatores = {
                          #'QUALITY_ROIC': 1000000,
                          'QUALITY_ROE': 1000000,
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

    premios = MakeResultsPremium(data_final_analise="2020-12-31", dicionario_fatores=dicionario_fatores,
                                 caminho_imagens = r'C:\Users\J.A.T.F\Desktop\codigo_py\Database\PDFs\images', 
                                 nome_arquivo = r'C:\Users\J.A.T.F\Desktop\codigo_py\Database\PDFs\avaliando_alguns_premios.pdf',
                                 caminho_premios_de_risco=r'C:\Users\J.A.T.F\Desktop\codigo_py\Database\premios_risco')

    
    premios.puxando_dados()
    premios.retorno_quartis()
    premios.fazer_pdf()


