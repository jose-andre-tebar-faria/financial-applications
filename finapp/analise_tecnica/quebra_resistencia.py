from estrategia import BigStrategy
from indicadores import MakeIndicator
from data_feed import ReadData
from otimizacao_movel import WalkForwardAnalysis

class quebra_resistencia_estrategia(BigStrategy):

    def __init__(self):
        super().__init__()

    
    def fazendo_indicadores(self):

        self.quebra_resistencia_preco_maximo = MakeIndicator().quebra_resistencia_maximo(self.dados.fechamento, periodo = self.parametro1)                                                                                           
        self.quebra_resistencia_preco_minimo = MakeIndicator().quebra_resistencia_minimo(self.dados.fechamento, periodo = self.parametro1)
        self.quebra_resistencia_volume = MakeIndicator().quebra_resistencia_maximo(self.dados.volume, periodo = self.parametro1)

        self.lista_indicadores = [self.quebra_resistencia_preco_maximo, self.quebra_resistencia_preco_minimo, self.quebra_resistencia_volume]

    def evento(self, data, i):

        #if self.dados.fechamento[data] == self.quebra_resistencia_preco_maximo[data] and (i != (self.barra_executada + self.parametro2)): 
        if (self.dados.fechamento[data] == self.quebra_resistencia_preco_maximo[data] and (i != (self.barra_executada + self.parametro2)) and 
            self.dados.volume[data] == self.quebra_resistencia_volume[data]):

            if self.comprado:

                pass

            elif self.vendido:

                self.vender_cdi()
                self.compra(inverter=True)
                self.barra_executada = i 

            else:

                self.vender_cdi()
                self.compra()
                self.barra_executada = i
                
        #elif self.dados.fechamento[data] == self.quebra_resistencia_preco_minimo[data] and (i != (self.barra_executada + self.parametro2)):
        elif (self.dados.fechamento[data] == self.quebra_resistencia_preco_minimo[data] and (i != (self.barra_executada + self.parametro2)) and 
              self.dados.volume[data] == self.quebra_resistencia_volume[data]):

            if self.vendido:

                pass

            elif self.comprado:

                self.venda(inverter=True)
                self.comprar_cdi()
                self.barra_executada = i

            else:

                self.venda()
                self.comprar_cdi()
                self.barra_executada = i

        elif self.comprado and (i == (self.barra_executada + self.parametro2)):

                self.venda(zerar=True)
                self.comprar_cdi()

        elif self.vendido and (i == (self.barra_executada + self.parametro2)):

                self.compra(zerar=True)
                self.comprar_cdi()
  

if __name__ == '__main__':

    acao = "PETR4"

    dados = ReadData(

        caminho_parquet = r'C:\Users\J.A.T.F\Desktop\codigo_py\Database\cotacoes.parquet',
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
    

    walk = WalkForwardAnalysis(estrategia = quebra_resistencia_estrategia(), class_dados = dados,
                               parametro1= range(6, 20, 3), parametro2 = range(4, 33, 4),
                               anos_otimizacao=3, anos_teste=1, 
                               nome_arquivo = rf"C:\Users\J.A.T.F\Desktop\codigo_py\Database\PDFs\analise_tecnica\backtest_2pra1_{acao}_RESISTENCIA_S_VOLUME.pdf",
                               caminho_dados_benchmarks =r'C:\Users\J.A.T.F\Desktop\codigo_py\Database',
                               caminho_imagens= r'C:\Users\J.A.T.F\Desktop\codigo_py\Database\PDFs\images',
                               corretagem=0.00005)
    
    walk.run_walk()


    
    












    #