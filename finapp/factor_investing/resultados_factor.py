import pandas as pd
import numpy as np
from itertools import groupby
from datetime import datetime
import mplcyberpunk 
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdate
import seaborn as sns
import warnings
from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
from report_pdf_carteiras import MakePDF
import os
from dotenv import load_dotenv

class MakeReportResult():

    def __init__(self, df_trades, df_carteiras, nome_arquivo = 'backtest.pdf'):

        load_dotenv()

        self.df_trades = df_trades
        self.carteiras = df_carteiras

        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.databse_folder = os.getenv("DATABASE_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.databse_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

        #diretorio_atual = os.getcwd()
        #print("Diretório atual para MakeReport:", diretorio_atual)

        self.ibov = pd.read_parquet(f'{self.full_desired_path}/ibov.parquet')
        self.cdi = pd.read_parquet(f'{self.full_desired_path}/cdi.parquet')
        self.cdi['cota'] = (1 + self.cdi['retorno']).cumprod() - 1
        self.ibov['retorno'] = self.ibov['fechamento'].pct_change()

        self.nome_arquivo = nome_arquivo

        self.cdi['data'] = pd.to_datetime(self.cdi['data'])
        self.ibov['data'] = pd.to_datetime(self.ibov['data'])
        self.df_trades['data'] = pd.to_datetime(self.df_trades['data'])

        self.df_trades['dinheiro'] = self.df_trades['dinheiro'].astype(float)
        self.df_trades['retorno'] = self.df_trades['retorno'].astype(float)

        self.cdi = self.cdi[(self.cdi['data'] >= self.df_trades['data'].iloc[0]) &
                            (self.cdi['data'] <= self.df_trades['data'].iloc[-1])]
        
        self.ibov = self.ibov[(self.ibov['data'] >= self.df_trades['data'].iloc[0]) &
                            (self.ibov['data'] <= self.df_trades['data'].iloc[-1])]
        
        plt.style.use('cyberpunk')

        self.make_report()
        
        #diretorio_atual = os.getcwd()
        #print("Diretório atual depois MakeReport:", diretorio_atual)

    def make_report(self):

        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.databse_folder = os.getenv("IMAGES_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.databse_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

        self.periodo_backtest()
        self.retorno_risco()
        self.turnover_carteira()
        self.drawdown()
        self.resultados_moveis()
        self.estatisticas_de_trade()
        self.eventos_de_estresse()
        self.grafico_retorno_acum()
        self.underwater()
        self.grafico_retorno_mes_a_mes()
        self.grafico_retorno_ano_a_ano()
        self.fazer_grafico_janelas_moveis()

        MakePDF(self.dd_all, self.dia_inicial, self.dia_final, self.dias_totais_backtest, 
            self.retorno_acum_modelo, self.retorno_acum_cdi, self.retorno_acum_ibov, self.turn_over_medio,
            self.retorno_aa_modelo, self.vol_ultimo_ano, self.sharpe, self.var_diario, 
            self.numero_trades, self.operacoes_vencedoras, self.operacoes_perdedoras, self.media_ganhos, self.media_perdas, 
            self.expectativa_matematica, self.percentual_cart_supera_ibov, self.maior_sequencia_vitorias, 
            self.maior_sequencia_derrotas, self.joesley_day, self.mar20, self.boasorteday, self.greve_caminhao, 
            self.crise_2008, self.precatorios, self.retorno_21_min, self.retorno_63_min, self.retorno_126_min, 
            self.retorno_252_min, self.retorno_504_min, self.retorno_756_min, nome_arquivo = self.nome_arquivo,
            )

    def periodo_backtest(self):

        self.dia_inicial = self.df_trades['data'].iat[0]
        self.dia_final = self.df_trades['data'].iat[-1]

        self.dias_totais_backtest = len(self.df_trades)

    def retorno_risco(self):

        self.retorno_acum_modelo = self.df_trades['dinheiro'].iat[-1]/self.df_trades['dinheiro'].iat[0] - 1 
        self.retorno_acum_cdi = ((self.cdi['retorno'] + 1).cumprod() - 1).iat[-1]
        self.retorno_acum_ibov = ((self.ibov['retorno'] + 1).cumprod() - 1).iat[-1] 

        self.retorno_aa_modelo = (1 + self.retorno_acum_modelo) ** (252/self.dias_totais_backtest) - 1 
        self.retorno_aa_cdi = (1 + self.retorno_acum_cdi) ** (252/self.dias_totais_backtest) - 1 
                
        self.vol_ultimo_ano = ((self.df_trades['retorno'].iloc[-253:-1]).std()) * np.sqrt(252)
        self.vol_periodo = (self.df_trades['retorno'].std()) * np.sqrt(252)

        self.sharpe = (self.retorno_aa_modelo - self.retorno_aa_cdi)/self.vol_periodo

        dia_95 = int(self.dias_totais_backtest * 0.05)
        self.var_diario = self.df_trades['retorno'].sort_values(ascending = True).iat[dia_95]      

    def turnover_carteira(self):
        # Cria um DataFrame com a data, ticker e um contador de empresas
        turnover_df = self.carteiras[['ticker']].copy()
        turnover_df['contador'] = 1

        # Transforma a data no índice e faz um 'shift' para comparar a presença de empresas em datas consecutivas
        #turnover_df.set_index('data', inplace=True)
        turnover_df = turnover_df.groupby(['data', 'ticker']).count().unstack(fill_value=0)

        turnover_anterior = turnover_df.shift()
        entrou = (turnover_df - turnover_anterior) > 0
        saiu = (turnover_df - turnover_anterior) < 0

        # Calcula o turnover, que é a soma das empresas que saem e entram, dividido pelo total de empresas
        total_anterior = turnover_anterior.sum(axis=1)
        total_atual = turnover_df.sum(axis=1)
        turnover_df = (saiu.sum(axis=1) + entrou.sum(axis=1)) / (total_anterior + total_atual)

        self.turn_over_medio = turnover_df.mean()

    def drawdown(self):

        self.dd_all = self.calcula_drawdown(len(self.df_trades))  # all time

    def calcula_drawdown(self, janela):

        df = self.df_trades.copy()

        df['maximo'] = df['dinheiro'].rolling(janela, min_periods=1).max()
        df['drawdown'] = (df['dinheiro'])/df['maximo'] - 1
        df['drawdown_max'] = df['drawdown'].rolling(janela, min_periods=1).min()

        self.drawdowns = df['drawdown']
        self.drawdowns.index = df['data']

        return min(df['drawdown_max'])
    
    def resultados_moveis(self):

        self.retorno_21 = self.calcula_retorno_movel(21) 
        self.retorno_21_min  = self.retorno_21['retorno_movel'].min()  
        self.retorno_63 = self.calcula_retorno_movel(63)
        self.retorno_63_min  = self.retorno_63['retorno_movel'].min()   
        self.retorno_126 = self.calcula_retorno_movel(126)  
        self.retorno_126_min  = self.retorno_126['retorno_movel'].min()
        self.retorno_252 = self.calcula_retorno_movel(252)  
        self.retorno_252_min  = self.retorno_252['retorno_movel'].min()
        self.retorno_504 = self.calcula_retorno_movel(504)  
        self.retorno_504_min  = self.retorno_504['retorno_movel'].min()
        self.retorno_756 = self.calcula_retorno_movel(756) 
        self.retorno_756_min  = self.retorno_756['retorno_movel'].min()
    
    def calcula_retorno_movel(self, janela):

        df = self.df_trades.copy()
        ibov_df = self.ibov.copy()

        df['retorno_movel'] = df['dinheiro'].pct_change(janela)
        ibov_df['retorno_movel_ibov'] = ibov_df['fechamento'].pct_change(janela)
        ibov_df = ibov_df[['data', 'retorno_movel_ibov']]
        df = pd.merge(df, ibov_df, on = 'data')
        df['alfa'] = (1 + df['retorno_movel'])/ (1 + df['retorno_movel_ibov']) - 1 
        df = df.dropna()
        df = df[['data', 'retorno_movel', 'alfa']]

        return df

    def estatisticas_de_trade(self):

        self.numero_trades = self.df_trades['numero_trade'].max()

        self.df_trades['retorno_plus_one'] = self.df_trades['retorno'] + 1

        self.df_trades['retorno_por_trade'] = self.df_trades.groupby('numero_trade')['retorno_plus_one'].cumprod() - 1

        trades_acum = (self.df_trades.groupby(['numero_trade']).tail(1))['retorno_por_trade']   

        trades = trades_acum.dropna().unique()

        self.operacoes_vencedoras = np.sum(np.where(trades > 0, True, False))/self.numero_trades

        self.operacoes_perdedoras = 1 - self.operacoes_vencedoras

        self.media_ganhos =  trades[trades > 0].mean()

        self.media_perdas =  trades[trades < 0].mean()

        self.expectativa_matematica = (self.operacoes_vencedoras * self.media_ganhos) - (self.operacoes_perdedoras * abs(self.media_perdas))

        self.maior_sequencia_vitorias = len(max((list(g) if k else [] for k, g in groupby(trades.tolist(), key=lambda i: i > 0)), key=len))
        self.maior_sequencia_derrotas = len(max((list(g) if k else [] for k, g in groupby(trades.tolist(), key=lambda i: i < 0)), key=len))

        ibov = self.ibov.copy()
        ibov.columns = ['data', 'fechamento', 'retorno_ibov']

        df_trades_ibov = pd.merge(self.df_trades, ibov, on='data', how='inner')

        df_trades_ibov['retorno_acum_ibov'] = (df_trades_ibov.groupby('numero_trade', group_keys=False)['retorno_ibov'].apply(lambda x: (1 + x).cumprod() - 1))
        df_trades_ibov['retorno_por_trade'] = (df_trades_ibov.groupby('numero_trade', group_keys=False)['retorno'].apply(lambda x: (1 + x).cumprod() - 1))

        retorno_ibov_por_trade = df_trades_ibov.groupby('numero_trade')['retorno_acum_ibov'].last() 
        retorno_por_trade = df_trades_ibov.groupby('numero_trade')['retorno_por_trade'].last()

        superou_trades = retorno_por_trade > retorno_ibov_por_trade
        self.percentual_cart_supera_ibov = superou_trades.mean()

    def eventos_de_estresse(self):

        if datetime(2017, 5, 18) in self.df_trades['data'].to_list():

            self.joesley_day = (self.df_trades[self.df_trades['data'] == datetime(2017, 5, 18)])['retorno'].iat[0]

        else:

            self.joesley_day = "-"

        if datetime(2020, 3, 2) in self.df_trades['data'].to_list() and datetime(2020, 3, 31) in self.df_trades['data'].to_list():

            
            auge_pandemia = self.df_trades[(self.df_trades['data'] >= datetime(2020, 3, 2)) &
                                           (self.df_trades['data'] <=  datetime(2020, 3, 31))]
            
            self.mar20 = auge_pandemia['dinheiro'].iloc[-1]/auge_pandemia['dinheiro'].iloc[0] - 1
            
        else:

            self.mar20 = "-"

        if datetime(2022, 11, 10) in self.df_trades['data'].to_list():

            self.boasorteday = (self.df_trades[self.df_trades['data'] == datetime(2022, 11, 10)])['retorno'].iat[0]

        else:

            self.boasorteday = "-"


        if datetime(2018, 4, 3) in self.df_trades['data'].to_list() and datetime(2018, 5, 30) in self.df_trades['data'].to_list(): #caminhao

            
            caminhoneiros = self.df_trades[(self.df_trades['data'] >= datetime(2018, 4, 3)) &
                                           (self.df_trades['data'] <=  datetime(2018, 5, 31))]
            
            self.greve_caminhao = caminhoneiros['dinheiro'].iloc[-1]/caminhoneiros['dinheiro'].iloc[0] - 1
            
        else:

            self.greve_caminhao = "-"

        if datetime(2008, 5, 2) in self.df_trades['data'].to_list() and datetime(2008, 10, 1) in self.df_trades['data'].to_list(): 

            
            crise_2008 = self.df_trades[(self.df_trades['data'] >= datetime(2008, 5, 2)) &
                                           (self.df_trades['data'] <=  datetime(2008, 10, 1))]
            
            self.crise_2008 = crise_2008['dinheiro'].iloc[-1]/crise_2008['dinheiro'].iloc[0] - 1
            
        else:

            self.crise_2008 = "-"

        if datetime(2021, 8, 3) in self.df_trades['data'].to_list() and datetime(2021, 11, 1) in self.df_trades['data'].to_list(): 

            
            precatorios = self.df_trades[(self.df_trades['data'] >= datetime(2021, 8, 3)) &
                                           (self.df_trades['data'] <=  datetime(2021, 11, 1))]
            
            self.precatorios = precatorios['dinheiro'].iloc[-1]/precatorios['dinheiro'].iloc[0] - 1
            
        else:

            self.precatorios = "-"

    def grafico_retorno_acum(self):

        fig, ax = plt.subplots(figsize = (7, 4))

        rent_modelo = (self.df_trades['retorno'] + 1).cumprod() - 1
        rent_cdi = (self.cdi['retorno'] + 1).cumprod() - 1
        rent_ibov = (self.ibov['retorno'] + 1).cumprod() - 1

        ax.plot(self.cdi['data'].values, rent_cdi.values, label = 'CDI')
        ax.plot(self.ibov['data'].values, rent_ibov.values, label = 'IBOV')
        ax.plot(self.df_trades['data'].values, rent_modelo.values, label = 'MODELO')

        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
        
        plt.legend()
        plt.title("Retorno acumulado")
        ax.grid(False)
        
        #diretorio_atual = os.getcwd()
        #print("Diretório atual para salvar figuras:", diretorio_atual)

        plt.savefig(f'{self.full_desired_path}/rent_acum.png', dpi = 300)

        plt.close()

    def grafico_retorno_mes_a_mes(self):

        mensal = self.df_trades

        mensal = self.df_trades.set_index('data')
        mensal = mensal.resample("M").last()
        rent_mes = mensal['dinheiro'].pct_change() 
        rent_mes = rent_mes.to_frame()
        rent_mes.columns = ['rent']
        rent_mes['mes'] = rent_mes.index.month_name()
        rent_mes['mes'] = rent_mes['mes'].apply(lambda x: x[0:3])
        rent_mes['ano'] = rent_mes.index.year    
        rent_mes = rent_mes.pivot(index='ano', columns='mes', values='rent')
        rent_mes = rent_mes[['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
        rent_mes = rent_mes.fillna(0)
        rent_mes = rent_mes * 100

        plt.style.use("default")

        fig = plt.figure(figsize = (8.75, 4))

        ax = sns.heatmap(rent_mes, cmap="YlGnBu", annot=True)
        plt.title("Retorno mês a mês")

        for t in ax.texts: 
             t.set_text(t.get_text() + "%")

        plt.savefig(f'{self.full_desired_path}/grafico_mes.png', dpi = 300)

        plt.close()

    def underwater(self):
        
        fig, ax = plt.subplots(figsize = (7, 4.5))

        ax.plot(self.drawdowns.index, self.drawdowns)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        if self.dias_totais_backtest > 1000:

            ax.xaxis.set_major_locator(mdate.YearLocator(2))

        else:

            ax.xaxis.set_major_locator(mdate.YearLocator(1))
        
        ax.xaxis.set_major_formatter(mdate.DateFormatter("%Y"))
        plt.title("Underwater")
        ax.grid(False)

        plt.savefig(f'{self.full_desired_path}/grafico_underwater.png', dpi = 300)

        plt.close()
        
    def grafico_retorno_ano_a_ano(self):

        lista_dfs = [self.df_trades, self.cdi, self.ibov]
        nomes = ['MODELO', 'CDI', 'IBOV']

        df_trades_copy = self.df_trades.copy()
        df_trades_copy = df_trades_copy.set_index('data')
        
        self.df_anual = pd.DataFrame(columns=['MODELO', 'CDI', 'IBOV'], index = np.unique(df_trades_copy.index.year).tolist())

        for i, df in enumerate(lista_dfs):

            self.transformando_em_anual(df = df, nome = nomes[i])

        fig = plt.figure(figsize = (8.75, 4))

        fig.patch.set_facecolor('white')

        ax = sns.heatmap(self.df_anual, cmap="YlGnBu", annot=True, fmt='.3g')
        plt.title("Retorno ano a ano")

        for t in ax.texts: 
             t.set_text(t.get_text() + "%")

        plt.savefig(f'{self.full_desired_path}/grafico_ano.png', dpi = 300)

        plt.close()

    def transformando_em_anual(self, df, nome):
        
        df_rent_anual = df
        
        df_rent_anual = df_rent_anual.set_index('data')

        df_rent_anual['cota'] = df_rent_anual['retorno'] + 1
        df_rent_anual['ano'] = df_rent_anual.index.year

        df_rent_anual["retorno_anual"] = df_rent_anual.groupby('ano')['cota'].cumprod() - 1

        df_rent_anual = (df_rent_anual.groupby(['ano']).tail(1))['retorno_anual']

        self.df_anual[nome] = df_rent_anual.values * 100

    def fazer_grafico_janelas_moveis(self):

        self.grafico_retorno_movel(self.retorno_252, "12M", 'retorno_movel')
        self.grafico_retorno_movel(self.retorno_252, "12M", 'alfa')
        self.grafico_retorno_movel(self.retorno_504, "24M", 'retorno_movel')
        self.grafico_retorno_movel(self.retorno_504, "24M", 'alfa')
        self.grafico_retorno_movel(self.retorno_756, "36M", 'retorno_movel')
        self.grafico_retorno_movel(self.retorno_756, "36M", 'alfa')
        
    def grafico_retorno_movel(self, df, periodo, coluna):

        plt.style.use('cyberpunk')
        
        #janela movel de retorno

        fig, ax = plt.subplots(figsize = (5, 4))

        ax.plot(df['data'], df[coluna])
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        if self.dias_totais_backtest > 1000:

            ax.xaxis.set_major_locator(mdate.YearLocator(2))

        else:

            ax.xaxis.set_major_locator(mdate.YearLocator(1))
        
        ax.xaxis.set_major_formatter(mdate.DateFormatter("%Y"))

        if coluna == 'alfa':

            plt.title(f"Janela móvel de alfa {periodo}")

        else:

            plt.title(f"Janela móvel de retorno {periodo}")

        ax.grid(False)

        plt.axhline(y=0, color = 'w')

        plt.savefig(f'{self.full_desired_path}/janela_movel_{periodo}_{coluna}.png', dpi = 300)

        plt.close()

if __name__ == "__main__":


    trades = pd.read_csv('./trades.csv')
    carteiras = pd.read_csv('./carteiras.csv', index_col='data')

    carteiras.index = pd.to_datetime(carteiras.index)

    report = MakeReportResult(df_trades=trades, df_carteiras=carteiras, nome_arquivo='./PDFs/backtest.pdf')

    # report.periodo_backtest()
    # report.retorno_risco()
    # report.turnover_carteira()
    # report.estatisticas_de_trade()
    # report.eventos_de_estresse()
    # report.drawdown()
    # report.resultados_moveis()
    # report.underwater()
    # report.grafico_retorno_acum()
    # report.grafico_retorno_mes_a_mes()
    # report.grafico_retorno_ano_a_ano()
    # report.fazer_grafico_janelas_moveis()

    # print(report.dia_inicial, report.dia_final, report.dias_totais_backtest)
    # print("-")
    # print(report.retorno_acum_modelo, report.retorno_acum_cdi ,
    #     report.retorno_acum_ibov,

    #     report.retorno_aa_modelo, 
    #     report.retorno_aa_cdi, 
                
    #     report.vol_ultimo_ano,
    #     report.vol_periodo, 

    #     report.sharpe,

        
    #     report.var_diario)

    # print(report.turn_over_medio)

    # print(report.numero_trades,

    #     report.operacoes_vencedoras, 

    #     report.operacoes_perdedoras, 

    #     report.media_ganhos,

    #     report.media_perdas,

    #     report.expectativa_matematica,

    #     report.maior_sequencia_vitorias ,
    #     report.maior_sequencia_derrotas,
    #     report.percentual_cart_supera_ibov)

    #print(report.joesley_day, report.mar20, report.boasorteday, report.crise_2008, report.greve_caminhao, report.precatorios)

    #print(report.dd_all)
    #print(report.retorno_21)
    #print(report.retorno_21_min, report.retorno_63_min, report.retorno_126_min, report.retorno_252_min, report.retorno_504_min)































