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
from report_pdf import MakePDF
import os


#depois colocar uma opção de otimização, que otimiza baseado em algum(s) parâmetros e exibe uma tabela no 
# final com a matriz de resultados e report inteiro apenas pro parâmetro ótimo escolhido.

class MakeReportResult():

    def __init__(self, df_trades, df_dados, nome_arquivo = 'backtest.pdf', 
                 otimizacao = False, df_otimizacao = None, lista_df_heatmap_parametros = None, parametro1_only = False, caminho_imagens = None,
                 caminho_benchmarks = None):
        
        self.df_trades = df_trades
        self.df_trades['cota'] = (self.df_trades['retorno'] + 1).cumprod() - 1
        self.dados = df_dados
        self.dados = self.dados.fillna(0)
        self.caminho_imagens = caminho_imagens

        if caminho_benchmarks == None:

            self.ibov = pd.read_parquet('./ibov.parquet')
            self.cdi = pd.read_parquet('./cdi.parquet')

        else:

            self.ibov = pd.read_parquet(f'{caminho_benchmarks}/ibov.parquet')
            self.cdi = pd.read_parquet(f'{caminho_benchmarks}/cdi.parquet')

        self.ibov['retorno'] = self.ibov['fechamento'].pct_change()
        self.otimizacao = otimizacao
        self.df_otimizacao = df_otimizacao
        self.lista_df_heatmap_parametros = lista_df_heatmap_parametros
        self.parametro1_only = parametro1_only

        self.nome_arquivo = nome_arquivo

        self.cdi['data'] = pd.to_datetime(self.cdi['data'])
        self.ibov['data'] = pd.to_datetime(self.ibov['data'])
        self.df_trades['data'] = pd.to_datetime(self.df_trades['data'])

        self.df_trades['cota'] = self.df_trades['cota'].astype(float)
        self.df_trades['retorno'] = self.df_trades['retorno'].astype(float)
        self.df_trades['numero_trade'] = self.df_trades['numero_trade'].astype(float)

        self.cdi = self.cdi[(self.cdi['data'] >= self.df_trades['data'].iloc[0]) &
                            (self.cdi['data'] <= self.df_trades['data'].iloc[-1])]
        
        self.ibov = self.ibov[(self.ibov['data'] >= self.df_trades['data'].iloc[0]) &
                            (self.ibov['data'] <= self.df_trades['data'].iloc[-1])]

        plt.style.use('cyberpunk')

        self.make_report()

    def make_report(self):

        self.periodo_backtest()
        self.retorno_risco()
        self.drawdown()
        self.estatisticas_de_trade()
        self.eventos_de_estresse()
        self.grafico_retorno_acum()
        self.grafico_preco_indicadores_e_sinais()
        self.underwater()
        self.grafico_retorno_mes_a_mes()
        self.grafico_retorno_ano_a_ano()

        if self.otimizacao:

            if self.parametro1_only:

                    self.grafico_otimizacao_1_parametro()
                    MakePDF(self.drawdown_maximo, self.dia_inicial, self.dia_final, self.dias_totais_backtest, 
                        self.retorno_acum_modelo, self.retorno_acum_acao, self.retorno_acum_cdi, self.retorno_acum_ibov, 
                        self.retorno_aa_modelo, self.vol_ultimo_ano, self.sharpe, self.var_diario, 
                        self.numero_trades, self.operacoes_vencedoras, self.operacoes_perdedoras, self.media_ganhos, self.media_perdas, 
                        self.expectativa_matematica, self.media_tempo_operacao, self.maior_sequencia_vitorias, 
                        self.maior_sequencia_derrotas, self.joesley_day, self.mar20, self.boasorteday, self.greve_caminhao, 
                        self.crise_2008, self.precatorios, self.df_otimizacao, otimizacao = True, nome_arquivo = self.nome_arquivo,
                        caminho_imagens = self.caminho_imagens)


            else:


                self.grafico_otimizacao()
                MakePDF(self.drawdown_maximo, self.dia_inicial, self.dia_final, self.dias_totais_backtest, 
                        self.retorno_acum_modelo, self.retorno_acum_acao, self.retorno_acum_cdi, self.retorno_acum_ibov, 
                        self.retorno_aa_modelo, self.vol_ultimo_ano, self.sharpe, self.var_diario, 
                        self.numero_trades, self.operacoes_vencedoras, self.operacoes_perdedoras, self.media_ganhos, self.media_perdas, 
                        self.expectativa_matematica, self.media_tempo_operacao, self.maior_sequencia_vitorias, 
                        self.maior_sequencia_derrotas, self.joesley_day, self.mar20, self.boasorteday, self.greve_caminhao, 
                        self.crise_2008, self.precatorios, self.df_otimizacao, otimizacao = True, nome_arquivo = self.nome_arquivo,
                        caminho_imagens = self.caminho_imagens)


        else: 

            MakePDF(self.drawdown_maximo, self.dia_inicial, self.dia_final, self.dias_totais_backtest, 
                    self.retorno_acum_modelo, self.retorno_acum_acao, self.retorno_acum_cdi, self.retorno_acum_ibov, 
                    self.retorno_aa_modelo, self.vol_ultimo_ano, self.sharpe, self.var_diario, 
                    self.numero_trades, self.operacoes_vencedoras, self.operacoes_perdedoras, self.media_ganhos, self.media_perdas, 
                    self.expectativa_matematica, self.media_tempo_operacao, self.maior_sequencia_vitorias, 
                    self.maior_sequencia_derrotas, self.joesley_day, self.mar20, self.boasorteday, self.greve_caminhao, 
                    self.crise_2008, self.precatorios, nome_arquivo = self.nome_arquivo, caminho_imagens = self.caminho_imagens)

        

    def periodo_backtest(self):

        self.dia_inicial = self.df_trades['data'].iat[0]
        self.dia_final = self.df_trades['data'].iat[-1]

        self.dias_totais_backtest = len(self.df_trades)

    def retorno_risco(self):

        self.retorno_acum_modelo = self.df_trades['cota'].iat[-1] 
        self.retorno_acum_acao = ((self.dados['retorno'] + 1).cumprod() - 1).iat[-1]
        self.retorno_acum_cdi = ((self.cdi['retorno'] + 1).cumprod() - 1).iat[-1]
        self.retorno_acum_ibov = ((self.ibov['retorno'] + 1).cumprod() - 1).iat[-1] 

        self.retorno_aa_modelo = (1 + self.retorno_acum_modelo) ** (252/self.dias_totais_backtest) - 1 
        self.retorno_aa_cdi = (1 + self.retorno_acum_cdi) ** (252/self.dias_totais_backtest) - 1 
                
        self.vol_ultimo_ano = ((self.df_trades['retorno'].iloc[-253:-1]).std()) * np.sqrt(252)
        self.vol_periodo = (self.df_trades['retorno'].std()) * np.sqrt(252)

        self.sharpe = (self.retorno_aa_modelo - self.retorno_aa_cdi)/self.vol_periodo

        dia_95 = int(self.dias_totais_backtest * 0.05)
        self.var_diario = self.df_trades['retorno'].sort_values(ascending = True).iat[dia_95]      

        

    def drawdown(self):

        maximo = (self.df_trades['cota'] + 1).cummax()
        self.drawdowns = (self.df_trades['cota'] + 1)/maximo - 1
        self.drawdowns.index = self.df_trades['data']
        self.drawdown_maximo = self.drawdowns.min()

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

        self.media_tempo_operacao = self.df_trades.groupby('numero_trade').size().mean()

        self.maior_sequencia_vitorias = len(max((list(g) if k else [] for k, g in groupby(trades.tolist(), key=lambda i: i > 0)), key=len))
        self.maior_sequencia_derrotas = len(max((list(g) if k else [] for k, g in groupby(trades.tolist(), key=lambda i: i < 0)), key=len))


    def eventos_de_estresse(self):

        if datetime(2017, 5, 18) in self.df_trades['data'].to_list():

            self.joesley_day = (self.df_trades[self.df_trades['data'] == datetime(2017, 5, 18)])['retorno'].iat[0]

        else:

            self.joesley_day = "-"

        if datetime(2020, 3, 2) in self.df_trades['data'].to_list() and datetime(2020, 3, 31) in self.df_trades['data'].to_list():

            
            auge_pandemia = self.df_trades[(self.df_trades['data'] >= datetime(2020, 3, 2)) &
                                           (self.df_trades['data'] <=  datetime(2020, 3, 31))]
            
            auge_pandemia['cota'] = auge_pandemia['cota'] + 1
            
            self.mar20 = auge_pandemia['cota'].iloc[-1]/auge_pandemia['cota'].iloc[0] - 1
            
        else:

            self.mar20 = "-"

        if datetime(2022, 11, 10) in self.df_trades['data'].to_list():

            self.boasorteday = (self.df_trades[self.df_trades['data'] == datetime(2022, 11, 10)])['retorno'].iat[0]

        else:

            self.boasorteday = "-"


        if datetime(2018, 4, 3) in self.df_trades['data'].to_list() and datetime(2018, 5, 30) in self.df_trades['data'].to_list(): #caminhao

            
            caminhoneiros = self.df_trades[(self.df_trades['data'] >= datetime(2018, 4, 3)) &
                                           (self.df_trades['data'] <=  datetime(2018, 5, 31))]
            
            caminhoneiros['cota'] = caminhoneiros['cota'] + 1
            
            self.greve_caminhao = caminhoneiros['cota'].iloc[-1]/caminhoneiros['cota'].iloc[0] - 1
            
        else:

            self.greve_caminhao = "-"

        if datetime(2008, 5, 2) in self.df_trades['data'].to_list() and datetime(2008, 10, 1) in self.df_trades['data'].to_list(): 

            
            crise_2008 = self.df_trades[(self.df_trades['data'] >= datetime(2008, 5, 2)) &
                                           (self.df_trades['data'] <=  datetime(2008, 10, 1))]
            
            crise_2008['cota'] = crise_2008['cota'] + 1
            
            self.crise_2008 = crise_2008['cota'].iloc[-1]/crise_2008['cota'].iloc[0] - 1
            
        else:

            self.crise_2008 = "-"

        if datetime(2021, 8, 3) in self.df_trades['data'].to_list() and datetime(2021, 11, 1) in self.df_trades['data'].to_list(): 

            
            precatorios = self.df_trades[(self.df_trades['data'] >= datetime(2021, 8, 3)) &
                                           (self.df_trades['data'] <=  datetime(2021, 11, 1))]
            
            precatorios['cota'] = precatorios['cota'] + 1
            
            self.precatorios = precatorios['cota'].iloc[-1]/precatorios['cota'].iloc[0] - 1
            
        else:

            self.precatorios = "-"


    def grafico_retorno_acum(self):

        fig, ax = plt.subplots(figsize = (7, 4))

        rent_acao = (self.dados['retorno'] + 1).cumprod() - 1
        rent_cdi = (self.cdi['retorno'] + 1).cumprod() - 1
        rent_ibov = (self.ibov['retorno'] + 1).cumprod() - 1

        ax.plot(self.dados.index.values, rent_acao.values, label = 'AÇÃO')
        ax.plot(self.cdi['data'].values, rent_cdi.values, label = 'CDI')
        ax.plot(self.ibov['data'].values, rent_ibov.values, label = 'IBOV')
        ax.plot(self.dados.index.values, self.df_trades['cota'].values, label = 'MODELO')

        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
        
        plt.legend()
        plt.title("Retorno acumulado")
        ax.grid(False)

        # Obtém o diretório atual
        diretorio_atual = os.getcwd()
        print("Diretório atual para salvar figuras:", diretorio_atual)

        if self.caminho_imagens == None:        

            plt.savefig('./rent_acum.png', dpi = 300)

        else:

            plt.savefig(f'{self.caminho_imagens}/rent_acum.png', dpi = 300)

        plt.close()

    def grafico_retorno_mes_a_mes(self):

        mensal = self.df_trades

        mensal['cota_plus_one'] = mensal['cota'] + 1

        mensal = self.df_trades.set_index('data')

        mensal = mensal.resample("M").last()

        rent_mes = mensal['cota_plus_one'].pct_change() 

        rent_mes.iloc[0] = mensal['cota_plus_one'].iloc[0] - 1

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

        if self.caminho_imagens == None:        

            plt.savefig('./grafico_mes.png', dpi = 300)

        else:

            plt.savefig(f'{self.caminho_imagens}/grafico_mes.png', dpi = 300)

        plt.close()

    def underwater(self):
        
        fig, ax = plt.subplots(figsize = (7, 3))

        ax.plot(self.drawdowns.index, self.drawdowns)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        if self.dias_totais_backtest > 1000:

            ax.xaxis.set_major_locator(mdate.YearLocator(2))

        else:

            ax.xaxis.set_major_locator(mdate.YearLocator(1))
        
        ax.xaxis.set_major_formatter(mdate.DateFormatter("%Y"))
        plt.title("Underwater")
        ax.grid(False)

        if self.caminho_imagens == None:        

            plt.savefig('./grafico_underwater.png', dpi = 300)

        else:

            plt.savefig(f'{self.caminho_imagens}/grafico_underwater.png', dpi = 300)

        plt.close()
        
    def grafico_retorno_ano_a_ano(self):

        lista_dfs = [self.df_trades, self.dados, self.cdi, self.ibov]
        nomes = ['MODELO', 'ACAO', 'CDI', 'IBOV']
        
        self.df_anual = pd.DataFrame(columns=['MODELO', 'ACAO', 'CDI', 'IBOV'], index = np.unique(self.dados.index.year).tolist())

        for i, df in enumerate(lista_dfs):

            self.transformando_em_anual(df = df, nome = nomes[i])

        fig = plt.figure(figsize = (8.75, 4))

        fig.patch.set_facecolor('white')

        ax = sns.heatmap(self.df_anual, cmap="YlGnBu", annot=True, fmt='.3g')
        plt.title("Retorno ano a ano")

        for t in ax.texts: 
             t.set_text(t.get_text() + "%")

        if self.caminho_imagens == None:        

            plt.savefig('./grafico_ano.png', dpi = 300)

        else:

            plt.savefig(f'{self.caminho_imagens}/grafico_ano.png', dpi = 300)

        plt.close()
        

    def transformando_em_anual(self, df, nome):
        
        df_rent_anual = df

        if nome != 'ACAO':
        
            df_rent_anual = df_rent_anual.set_index('data')

        df_rent_anual['cota'] = df_rent_anual['retorno'] + 1
        df_rent_anual['ano'] = df_rent_anual.index.year

        df_rent_anual["retorno_anual"] = df_rent_anual.groupby('ano')['cota'].cumprod() - 1

        df_rent_anual = (df_rent_anual.groupby(['ano']).tail(1))['retorno_anual']

        self.df_anual[nome] = df_rent_anual.values * 100


    def grafico_preco_indicadores_e_sinais(self):

        fig, ax = plt.subplots(figsize = (8.75, 4))
        
        ax.plot(self.dados.index, self.dados['fechamento'])
        
        compras = self.df_trades[self.df_trades['sinal'] == 'compra']
        preco_compra = self.dados[self.dados.index.isin(compras['data'].to_list())]['fechamento']

        vendas = self.df_trades[self.df_trades['sinal'] == 'venda']
        preco_vendas = self.dados[self.dados.index.isin(vendas['data'].to_list())]['fechamento']
        
        ax.scatter(compras['data'].values , preco_compra.values, label = 'Compra' , marker = '^', color = 'green', alpha = 1, s = 100)
        ax.scatter(vendas['data'].values , preco_vendas.values , label = 'Venda' , marker = 'v', color = 'red', alpha = 1, s = 100)

        plt.title("Sinais de trade no ativo")
        ax.grid(False)

        if self.caminho_imagens == None:        

            plt.savefig('./grafico_sinais.png', dpi = 300)

        else:

            plt.savefig(f'{self.caminho_imagens}/grafico_sinais.png', dpi = 300)

        plt.close()

    def grafico_otimizacao(self):

        for i, df in enumerate(self.lista_df_heatmap_parametros):

            df['parametro1'] = df['parametro1'].astype(float) 
            df['parametro2'] = df['parametro2'].astype(float) 
            df['retorno'] = df['retorno'].astype(float)

            df = df.pivot(index='parametro1', columns='parametro2', values='retorno')

            fig = plt.figure(figsize = (8.75, 4))

            fig.patch.set_facecolor('white')

            ax = sns.heatmap(df, cmap="YlGnBu", annot=False)
            
            plt.title(f"Parâmetros x Retorno {self.df_otimizacao['data_final_IS'].iloc[i]}")

            if self.caminho_imagens == None:        

                plt.savefig(f'./retorno_por_parametro_{i}.png', dpi = 300)

            else:

                plt.savefig(f'{self.caminho_imagens}/retorno_por_parametro_{i}.png', dpi = 300)


            plt.close()

    def grafico_otimizacao_1_parametro(self):

        plt.style.use("cyberpunk")

        for i, df in enumerate(self.lista_df_heatmap_parametros):

            df['parametro1'] = df['parametro1'].astype(int) 
            df['retorno'] = df['retorno'].astype(float)

            fig, ax = plt.subplots(figsize = (8.75, 4))

            ax.bar(df['parametro1'].values, df['retorno'].values)

            if len(df[df['retorno'] > 0]) > 0:

                plt.axhline(y=0, color = 'w')

            ax.grid(False)
            ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

            plt.title(f"Parâmetros x Retorno: {self.df_otimizacao['data_inicial_IS'].iloc[i]} - {self.df_otimizacao['data_final_IS'].iloc[i]}")

            if self.caminho_imagens == None:        

                plt.savefig(f'./retorno_por_parametro_{i}.png', dpi = 300)

            else:

                plt.savefig(f'{self.caminho_imagens}/retorno_por_parametro_{i}.png', dpi = 300)
            
        
            plt.close()
        
        
        pass


if __name__ == "__main__":


    trades = pd.read_csv('./galaxia_12_analise_tecnica/dados_csv/df_trades.csv')
    dados = pd.read_csv("./galaxia_12_analise_tecnica/dados_csv/dados.csv", index_col='data')

    dados.index = pd.to_datetime(dados.index)

    report = MakeReportResult(df_trades=trades, df_dados=dados, indicadores=[])

    # report.periodo_backtest()
    # report.retorno_risco()
    # report.estatisticas_de_trade()
    # report.eventos_de_estresse()

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

    # print(report.numero_trades,

    #     report.operacoes_vencedoras, 

    #     report.operacoes_perdedoras, 

    #     report.media_ganhos,

    #     report.media_perdas,

    #     report.expectativa_matematica,

    #     report.media_tempo_operacao ,

    #     report.maior_sequencia_vitorias ,
    #     report.maior_sequencia_derrotas)

    #print(report.joesley_day, report.mar20, report.boasorteday, report.crise_2008, report.greve_caminhao, report.precatorios)
    



