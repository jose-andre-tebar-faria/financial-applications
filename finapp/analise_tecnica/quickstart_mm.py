from estrategia import BigStrategy
from indicadores import MakeIndicator
from data_feed import ReadData
from otimizacao_movel import WalkForwardAnalysis
import os


class MM_estrategia(BigStrategy):

    def __init__(self):
        super().__init__()

    def fazendo_indicadores(self):

        self.sma_rapida = MakeIndicator().media_movel_simples(self.dados.fechamento, 7)
        self.sma_lenta = MakeIndicator().media_movel_simples(self.dados.fechamento, 40)

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

    acao = "PETR4"

    dados = ReadData(

        caminho_parquet = r'./finapp/files/cotacoes.parquet',
        tem_multiplas_empresas=True,
        empresa_escolhida=acao,
        nome_coluna_empresas = 'ticker',

        data_inicial = "2010-01-01", 
        data_final = "2023-04-30", 
        
        formato_data = ('%Y-%m-%d'), 

        coluna_data = 0, 
        abertura = 12, 
        minima = 15, 
        maxima = 13, 
        fechamento = 11, 
        volume = 9
    )
    
    start_estrategia = MM_estrategia()

    start_estrategia.corretagem = 0.0005
    
    
    diretorio_atual = os.getcwd()
    print("Diretório atual _main_:", diretorio_atual)
    
    start_estrategia.add_caminhos(caminho_dados=r'./finapp/files',
                                  caminho_imagens=r'./finapp/files/images')

    start_estrategia.add_data(dados)
    start_estrategia.add_cdi()
    start_estrategia.run_strategy()

    start_estrategia.make_report(nome_arquivo = r'./finapp/files/PDFs/analise_tecnica/mm_teste.pdf')

    print(start_estrategia.df_trades)

































































