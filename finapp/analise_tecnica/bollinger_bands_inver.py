from estrategia import BigStrategy
from indicadores import MakeIndicator
from data_feed import ReadData
from otimizacao_movel import WalkForwardAnalysis
import os

class BB_estrategia(BigStrategy):

    def __init__(self):
        super().__init__()

    
    def fazendo_indicadores(self):

        self.media, self.borda_superior, self.borda_inferior = MakeIndicator().bollinger_bands(self.dados.fechamento, periodo_media = self.parametro1,
                                                                                                numero_desvios=self.parametro2)


        self.lista_indicadores = [self.media, self.borda_superior, self.borda_inferior]

    def evento(self, data, i):

        if self.dados.fechamento[data] > self.borda_superior[data]:

            if self.comprado:

                pass

            else:

                self.vender_cdi()
                self.compra(inverter = True)
                

        elif self.dados.fechamento[data] < self.borda_inferior[data]:

            if self.vendido:

                pass

            else:

                self.venda(inverter=True)
                self.comprar_cdi()
  

if __name__ == '__main__':

    import numpy as np

    acao = "WEGE3"

    # Obtém o diretório atual
    diretorio_atual = os.getcwd()
    print("Diretório atual _main_:", diretorio_atual)

    dados = ReadData(

        caminho_parquet = r'./finapp/files/cotacoes.parquet',
        tem_multiplas_empresas=True,
        empresa_escolhida=acao,
        nome_coluna_empresas = 'ticker',

        data_inicial = "2010-01-01", 
        data_final = "2021-04-18", 
        
        formato_data = ('%Y-%m-%d'), 

        coluna_data = 0, 
        abertura = 12, 
        minima = 15, 
        maxima = 13, 
        fechamento = 11, 
        volume = 9
    )
    

    walk = WalkForwardAnalysis(estrategia = BB_estrategia(), class_dados = dados,
                               parametro1= range(8, 37, 4), parametro2 = np.arange(0.5, 3.6, 0.5),
                               anos_otimizacao=3, anos_teste=1, 
                               nome_arquivo = rf"./finapp/files/PDFs/analise_tecnica/backtest_2pra1_{acao}_BB_INVERTIDO.pdf",
                               caminho_dados_benchmarks =r'./finapp/files',
                               caminho_imagens= r'./finapp/files/images')
    
    walk.run_walk()


    
    












    #