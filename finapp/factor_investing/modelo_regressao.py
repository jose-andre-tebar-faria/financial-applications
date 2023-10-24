import pandas as pd
import statsmodels.api as sm

class linear_regression():

    def __init__(self, data_final_analise, dicionario_fatores, caminho_premios_de_risco = '.', caminho_cdi = "."):

        self.caminho_premios_de_risco = caminho_premios_de_risco
        self.caminho_cdi = caminho_cdi
        self.dicionario_fatores = dicionario_fatores
        self.data_final_analise = data_final_analise

        self.lista_nome_fatores = []
        self.liquidez = []

        for key, item in dicionario_fatores.items():
            
            self.lista_nome_fatores.append(key)
            self.liquidez.append(item)


    def puxando_dados_premios(self):

        df_premios = pd.read_parquet(f'{self.caminho_premios_de_risco}/market_premium.parquet')
        df_premios['data'] = pd.to_datetime(df_premios['data'])
        
        for i, nome_premio in enumerate(self.lista_nome_fatores):

            df = pd.read_parquet(f'{self.caminho_premios_de_risco}/{nome_premio}_{self.liquidez[i]}.parquet')
            df['data'] = pd.to_datetime(df['data'])

            df = df.assign(premio_fator = (1 + df['primeiro_quartil'])/ (1 + df['quarto_quartil']) - 1)
            universo_fator = df[['data', f'universo']]
            universo_fator.columns = ['data', f'universo_{nome_premio}']

            if i == 0:

                universo = universo_fator

            else:

                universo = pd.merge(universo, universo_fator, on = 'data')

            df = df[['data', 'premio_fator']]
            df.columns = ['data', nome_premio]

            df_premios = pd.merge(df, df_premios, how = 'inner', on = 'data')
         

        df_premios = df_premios.drop(df_premios.index[0], axis = 0) #tirando a primeira linha por um detalhe no calculo do universo
        df_premios = df_premios.set_index('data')
        df_premios = df_premios[df_premios.index < self.data_final_analise]
        universo = universo[universo['data'] < self.data_final_analise]

        self.df_premios = df_premios
        self.universo = universo


    def calculando_universo(self):

        universo = self.universo
        universo = universo.set_index('data')
        universo['universo_medio'] = universo.mean(axis = 1)
        universo = universo.reset_index()
        universo = universo[['data', 'universo_medio']]
        

        cdi = pd.read_parquet(f'{self.caminho_cdi}/cdi.parquet')
        cdi['data'] = pd.to_datetime(cdi['data'])
        cdi['cota'] = (1 + cdi['retorno']).cumprod() - 1
        cdi = cdi[cdi['data'].isin(universo['data'].to_list())]
        cdi['rf'] = cdi['cota'].pct_change()
        cdi = cdi.dropna()
        cdi = cdi[['data', 'rf']]

        universo = pd.merge(universo, cdi, how = 'inner', on = 'data')
        universo['U_RF'] = (1 + universo['universo_medio'])/ (1 + universo['rf']) - 1
        universo = universo.set_index('data')
        self.universo = universo

    def regressao(self):

        Y = self.universo['U_RF']
        X = self.df_premios

        X_C = sm.add_constant(X)
        
        model = sm.OLS(Y, X_C)
        resultado = model.fit()
        print(resultado.summary())


if __name__ == "__main__":

    dicionario_fatores = {
                          'MOMENTO_MM_7_40': 1000000,
                          'TAMANHO_VALOR_DE_MERCADO': 1000000,
                          'VALOR_EBIT_EV': 1000000,
                          #'ALAVANCAGEM_EBIT_DL': 1000000,
                           }

    fazendo_modelo = linear_regression(data_final_analise= "2020-12-31", dicionario_fatores = dicionario_fatores, 
                                       caminho_premios_de_risco=R'C:\Users\J.A.T.F\Desktop\codigo_py\Database\premios_risco',
                                       caminho_cdi = R'C:\Users\J.A.T.F\Desktop\codigo_py\Database')

    fazendo_modelo.puxando_dados_premios()
    fazendo_modelo.calculando_universo()
    fazendo_modelo.regressao()
    

    