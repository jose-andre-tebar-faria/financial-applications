from estrategia import BigStrategy
from indicadores import MakeIndicator
from data_feed import ReadData
from otimizacao_movel import WalkForwardAnalysis


class MM_estrategia(BigStrategy):

    def __init__(self):
        super().__init__()

    
    def fazendo_indicadores(self):

        self.sma_rapida = MakeIndicator().media_movel_simples(self.dados.fechamento, self.parametro1)
        self.sma_lenta = MakeIndicator().media_movel_simples(self.dados.fechamento, self.parametro2)

        self.lista_indicadores = [self.sma_lenta, self.sma_rapida]

    def evento(self, data, i):

        if self.sma_rapida[data] > self.sma_lenta[data]:

            if self.comprado:

                pass

            else:

                self.compra(inverter=True)

        elif self.sma_rapida[data] < self.sma_lenta[data]:

            if self.vendido:

                pass

            else:

                self.venda(inverter = True)



            
if __name__ == "__main__":

    acao = "WEGE3"

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

    walk = WalkForwardAnalysis(estrategia = MM_estrategia(), class_dados = dados,
                               parametro1= range(7, 29, 7), parametro2= range(30, 46, 5), anos_otimizacao=2, anos_teste=1, 
                               nome_arquivo = rf"./finapp/files/PDFs/analise_tecnica/backtest_2pra1_{acao}_MM.pdf",
                               caminho_dados_benchmarks =r'./finapp/files',
                               caminho_imagens= r'./finapp/files/images')

    walk.run_walk()