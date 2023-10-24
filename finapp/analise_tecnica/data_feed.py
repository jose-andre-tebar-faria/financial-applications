import pandas as pd


class ReadData():

    def __init__(self, caminho_parquet, data_inicial, data_final, formato_data, 
                 coluna_data, abertura, minima, maxima, fechamento, volume, na_values = pd.NA, 
                 tem_multiplas_empresas = False, empresa_escolhida = None, nome_coluna_empresas = None):
        
        self.caminho_parquet = caminho_parquet
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.na_values = na_values
        self.formato_data = formato_data
        self.coluna_data = coluna_data
        self.abertura = abertura
        self.minima = minima
        self.maxima = maxima
        self.fechamento = fechamento
        self.volume = volume
        self.nome_coluna_empresas = nome_coluna_empresas

        self.dados = pd.read_parquet(self.caminho_parquet)

        if tem_multiplas_empresas:

            self.dados = self.dados[self.dados[nome_coluna_empresas] == empresa_escolhida]

        self.organizando_colunas()
        self.filtrando_data()
        self.colocando_data_index()

        
    

    def organizando_colunas(self):

        colunas_escolhidas = [self.coluna_data, self.abertura, self.minima, self.maxima, self.fechamento, self.volume]
        self.dados = self.dados.iloc[:, colunas_escolhidas]
        
        #mudando pra ordem padrão

        self.dados.columns = ['data', 'abertura', 'minima', 'maxima', 'fechamento', 'volume'] 


    def filtrando_data(self):

        self.dados['data'] = pd.to_datetime(self.dados['data'], format=self.formato_data)

        self.dados = self.dados[(self.dados['data'] >= self.data_inicial) & 
                                (self.dados['data'] <= self.data_final)]

    def colocando_data_index(self):

        self.dados = self.dados.set_index('data')

if __name__ == "__main__":

    dados_petr = ReadData(

        caminho_parquet = r'C:\Users\J.A.T.F\Desktop\codigo_py\Database\cotacoes.parquet',
        tem_multiplas_empresas=True,
        empresa_escolhida='WEGE3',
        nome_coluna_empresas = 'ticker',

        data_inicial = "2023-01-01", 
        data_final = "2023-04-30", 
        
        formato_data = ('%Y-%m-%d'), 

        coluna_data = 0, 
        abertura = 12, 
        minima = 15, 
        maxima = 13, 
        fechamento = 11, 
        volume = 9
    )