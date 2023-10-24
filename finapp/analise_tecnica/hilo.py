from estrategia import BigStrategy
from indicadores import MakeIndicator
from data_feed import ReadData
from otimizacao_movel import WalkForwardAnalysis

class hilo_estrategia(BigStrategy):

    def __init__(self):
        super().__init__()

    
    def fazendo_indicadores(self):

        self.media_maxima = MakeIndicator().media_movel_simples(self.dados.maxima, self.parametro1)
        self.media_minima = MakeIndicator().media_movel_simples(self.dados.minima, self.parametro1)

        self.lista_indicadores = [self.media_maxima, self.media_minima]

    def evento(self, data, i):

        if self.dados.fechamento[data] > self.media_maxima[data]:

            if self.comprado:

                pass

            else:
                self.vender_cdi()
                self.compra(inverter=True)

        elif self.dados.fechamento[data] < self.media_minima[data]:

            if self.vendido:

                pass

            else:

                self.venda(inverter = True)
                self.comprar_cdi()

  

if __name__ == '__main__':

    acao = "CSNA3"

    dados = ReadData(

        caminho_parquet = r'C:\Users\J.A.T.F\Desktop\codigo_py\Database\cotacoes.parquet',
        tem_multiplas_empresas=True,
        empresa_escolhida=acao,
        nome_coluna_empresas = 'ticker',

        data_inicial = "2010-01-01", 
        data_final = "2023-04-18", 
        
        formato_data = ('%Y-%m-%d'), 

        coluna_data = 0, 
        abertura = 12, 
        minima = 15, 
        maxima = 13, 
        fechamento = 11, 
        volume = 9
    )

    #mostrar na aula o exemplo da gol pra investigar mais a fundo no trading view
    #mostrar que empresas de beta baixo nao funciona
    

    walk = WalkForwardAnalysis(estrategia = hilo_estrategia(), class_dados = dados,
                               parametro1= range(15, 50, 3), anos_otimizacao=2, anos_teste=1, 
                               nome_arquivo = rf"C:\Users\J.A.T.F\Desktop\codigo_py\Database\PDFs\analise_tecnica\backtest_2pra1_{acao}_HILO.pdf",
                               caminho_dados_benchmarks =r'C:\Users\J.A.T.F\Desktop\codigo_py\Database',
                               caminho_imagens= r'C:\Users\J.A.T.F\Desktop\codigo_py\Database\PDFs\images')

    
    

    walk.run_walk()