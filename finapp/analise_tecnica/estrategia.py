import pandas as pd
from resultados import MakeReportResult
import warnings
from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
import numpy as np
import os

class BigStrategy():

    def __init__(self):
        
        self.novo_trade = False
        self.df_trades = pd.DataFrame(columns = ['data', 'retorno', 'numero_trade', 'sinal'])
        self.numero_do_trade = 0
        self.comprado = False
        self.vendido = False
        self.lista_indicadores = []
        self.dados = None
        self.zerou_venda = False
        self.zerou_compra = False
        self.barra_executada = 9999999999999999999999999
        self.cdi = False
        self.fechamento = None

        self.dados_cdi = None
        
        self.escolher_data = False
        self.data_inicial = None
        self.data_final = None
        self.parametro1 = None
        self.parametro2 = None
        self.corretagem = 0

        self.caminho_imagens = None
        self.caminho_benchmarks = None


    def add_data(self, class_data):

        self.dados = class_data.dados

    def add_cdi(self):

        if self.caminho_benchmarks == None:

            self.dados_cdi = pd.read_parquet('./cdi.parquet')

        else:

            self.dados_cdi = pd.read_parquet(f'{self.caminho_benchmarks}/cdi.parquet')

        self.dados_cdi['data'] = pd.to_datetime(self.dados_cdi['data'])
        self.dados_cdi = self.dados_cdi.set_index('data')

    def add_caminhos(self, caminho_imagens, caminho_dados):

        self.caminho_imagens = caminho_imagens
        self.caminho_benchmarks = caminho_dados

        os.chdir(caminho_imagens)

    def run_strategy(self, reset = True):

        if reset:

            self.numero_do_trade = 0
            self.comprado = False
            self.vendido = False
            self.cdi = False
            self.zerou_venda = False
            self.zerou_compra = False
            self.barra_executada = 9999999999999999999999999

        else:

            pass
        
        
        self.df_trades = pd.DataFrame(columns = ['data', 'retorno', 'numero_trade', 'sinal'])

        self.fazendo_indicadores()
        self._organizando_datas()
        self._calculando_retorno()
        self._iteracao()

    def fazendo_indicadores(self):

        pass
        
    def _organizando_datas(self):

        if self.escolher_data:

            self.dados_filtrados_data = self.dados[(self.dados.index >= self.data_inicial) &
                                                   (self.dados.index <= self.data_final)]      

            indicadores_filtrados = []

            for indicador in self.lista_indicadores:

                indicador = indicador[(indicador.index >= self.data_inicial) &
                                      (indicador.index <= self.data_final)]
                
                indicadores_filtrados.append(indicador)

            self.lista_indicadores = indicadores_filtrados

        else:

            datas_maximas = [create_indicador.index[0] for create_indicador in self.lista_indicadores]
        
            data_mais_recente = max(datas_maximas) #o maximo porque precisamos do mais recente

            self.dados_filtrados_data = self.dados[self.dados.index >= data_mais_recente]

            indicadores_filtrados = []

            for indicador in self.lista_indicadores:

                indicador = indicador[indicador.index >= data_mais_recente]
                indicadores_filtrados.append(indicador)

            self.lista_indicadores = indicadores_filtrados

    def _calculando_retorno(self):

        self.dados_filtrados_data.loc[:, 'retorno'] = self.dados_filtrados_data.fechamento.pct_change().copy()

        if self.fechamento != None:

            retorno_primeiro_dia = self.dados_filtrados_data.fechamento[0]/self.fechamento - 1
            self.dados_filtrados_data.retorno[0] = retorno_primeiro_dia

    def _iteracao(self):

        datas = []
        retornos = []
        numero_trades = []
        sinais = []

        i = 0

        

        for data, linhas in self.dados_filtrados_data.iterrows(): 
            

            if self.novo_trade:

                self.numero_do_trade = self.numero_do_trade + 1
                
            if self.comprado: #contabilizar a rent do dia

                datas.append(data.date())
                numero_trades.append(self.numero_do_trade)
                
                if self.novo_trade:

                    if sinais != []:

                    
                        sinais[-1] = 'compra'
                    
                        sinais.append(np.nan)

                    else:

                        sinais.append('compra')


                    retornos.append(linhas['retorno'] - self.corretagem)

                else:
                    retornos.append(linhas['retorno'])
                    sinais.append(np.nan)

            elif self.vendido:

                datas.append(data.date())
                numero_trades.append(self.numero_do_trade)
                
                if self.novo_trade:

                    if sinais != []:

                    
                        sinais[-1] = 'venda'
                    
                        sinais.append(np.nan)

                    else:

                        sinais.append('venda')


                    retornos.append((linhas['retorno'] * -1) - self.corretagem)

                else:

                    sinais.append(np.nan)
                    retornos.append(linhas['retorno'] * -1)

            elif self.zerou_venda:

                datas.append(data.date())
                

                try:

                    retorno_ontem = retornos[-1]

                    retornos[-1] = (retorno_ontem - self.corretagem)

                    retornos.append(0)

                    sinais[-1] = 'compra'

                    sinais.append(np.nan)

                except IndexError:

                    retornos.append(- self.corretagem)
                    sinais.append('compra')


                numero_trades.append(np.nan)
                
                self.zerou_venda = False

            elif self.zerou_compra:

                datas.append(data.date())

                try:
                    
                    retorno_ontem = retornos[-1]

                    retornos[-1] = (retorno_ontem - self.corretagem)

                    retornos.append(0)

                    sinais[-1] = 'venda'

                    sinais.append(np.nan)

                except IndexError:

                    retornos.append(- self.corretagem)
                    sinais.append('venda')
                
                numero_trades.append(np.nan)
                self.zerou_compra = False
            
            
            else:

                datas.append(data.date())
                retornos.append(0)
                numero_trades.append(np.nan)
                sinais.append(np.nan)


            if self.cdi:

                try:

                    retornos[-1] = retornos[-1] + self.dados_cdi.retorno[data]

                except KeyError:

                    pass

            self.novo_trade = False

            self.evento(data = data, i = i)

            i = i + 1

        self.df_trades['data'] = datas
        self.df_trades['retorno'] = retornos
        self.df_trades['numero_trade'] = numero_trades
        self.df_trades['sinal'] = sinais


            

    def evento(self, data, i = None):

        pass

    def compra(self, inverter = False, zerar = False):
        
        if inverter:

            self.vendido = False
            self.novo_trade = True
            self.comprado = True

        elif zerar:

            self.vendido = False
            self.zerou_venda = True

        else: #vou comprar

            self.comprado = True
            self.novo_trade = True

    def venda(self, inverter = False, zerar = False):   

        if inverter:

            self.comprado = False
            self.novo_trade = True
            self.vendido = True

        elif zerar:

            self.comprado = False
            self.zerou_compra = True

        else:

            self.vendido = True
            self.novo_trade = True

    def comprar_cdi(self):

        self.cdi = True
    
    def vender_cdi(self):

        self.cdi = False

    def make_report(self, nome_arquivo = 'backtest.pdf'):

        MakeReportResult(df_trades=self.df_trades, df_dados = self.dados_filtrados_data, caminho_imagens=self.caminho_imagens,
                         caminho_benchmarks=self.caminho_benchmarks, nome_arquivo=nome_arquivo) 
                          