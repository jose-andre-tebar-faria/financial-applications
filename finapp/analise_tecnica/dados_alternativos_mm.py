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

    import yfinance as yf

    dados_yf = yf.download(acao + ".SA")

    dados_yf['fator_ajuste'] = dados_yf['Close']/dados_yf['Adj Close']

    ajustar = ['Open', 'High', 'Low']

    for ajuste in ajustar:

        dados_yf[ajuste] = dados_yf[ajuste]/dados_yf['fator_ajuste'] 

    dados_yf = dados_yf.drop(['Close', 'fator_ajuste'], axis = 1)
    dados_yf = dados_yf.reset_index()

    dados_yf.to_parquet(fr'./finapp/files/cotacoes_{acao}.parquet')

    dados = ReadData(

        caminho_parquet = fr'./finapp/files/cotacoes_{acao}.parquet',
        data_inicial = "2000-01-01", 
        data_final = "2021-10-28", 
        
        formato_data = ('%Y-%m-%d'), 

        coluna_data = 0, 
        abertura = 1, 
        minima = 3, 
        maxima = 2, 
        fechamento = 4, 
        volume = 5
    )


    walk = WalkForwardAnalysis(estrategia = MM_estrategia(), class_dados = dados,
                               parametro1= range(7, 29, 7), parametro2= range(30, 46, 5), anos_otimizacao=2, anos_teste=1, 
                               nome_arquivo = rf"./finapp/files/PDFs/analise_tecnica/backtest_2pra1_{acao}_MM(dados_altern).pdf",
                               caminho_dados_benchmarks =r'./finapp/files',
                               caminho_imagens= r'./finapp/files/images')

    walk.run_walk()