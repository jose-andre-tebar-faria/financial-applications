from otimizacao import Optimize
import pandas as pd
from resultados import MakeReportResult
import os


class WalkForwardAnalysis():

    def __init__(self, estrategia, class_dados, anos_otimizacao, anos_teste, nome_arquivo, parametro1, parametro2 = (), corretagem = 0, 
                 caminho_imagens = None, caminho_dados_benchmarks = None):
        
        self.otimizacao = Optimize(estrategia = estrategia, parametro1= parametro1, parametro2= parametro2, class_dados = class_dados)
        self.parametro1 = parametro1
        self.parametro2 = parametro2
        self.dados = class_dados.dados
        self.anos_otimizacao = anos_otimizacao
        self.anos_teste = anos_teste
        self.nome_arquivo = nome_arquivo
        self.otimizacao.estrategia.corretagem = corretagem

        self.otimizacao.estrategia.caminho_imagens = caminho_imagens
        self.otimizacao.estrategia.caminho_benchmarks = caminho_dados_benchmarks

        # Obtém o diretório atual
        diretorio_atual = os.getcwd()
        print("Diretório atual WalkForwardAnalysis:", diretorio_atual)

        os.chdir(caminho_imagens)

        self.otimizacao.estrategia.add_cdi()

        self.buscando_data_inicial()


    def buscando_data_inicial(self):
        
        parametro1_maximo = max(self.parametro1)
        parametro1_minimo = min(self.parametro1)

        datas_maximas = []

        if self.parametro2 != ():

            parametro2_maximo = max(self.parametro2)
            parametro2_minimo = min(self.parametro2)

            lista_parametros = [parametro1_maximo, parametro1_minimo]
            lista_parametro2 = [parametro2_minimo, parametro2_maximo]

        else:

            lista_parametros = [parametro1_maximo, parametro1_minimo]

        
        for parametro in lista_parametros:

            self.otimizacao.estrategia.parametro1 = parametro
            
            if self.parametro2 != ():
            
                self.otimizacao.estrategia.parametro2 = parametro2_maximo

            self.otimizacao.estrategia.fazendo_indicadores()

            lista = [create_indicador.index[0] for create_indicador in self.otimizacao.estrategia.lista_indicadores]

            datas_maximas = datas_maximas + lista

        if self.parametro2 != ():
        
            for parametro in lista_parametro2:

                self.otimizacao.estrategia.parametro1 = parametro1_maximo
                self.otimizacao.estrategia.parametro2 = parametro

                self.otimizacao.estrategia.fazendo_indicadores()

                datas_parametro2 = [create_indicador.index[0] for create_indicador in self.otimizacao.estrategia.lista_indicadores]
            
                datas_maximas = datas_maximas + datas_parametro2

        data_mais_recente = max(datas_maximas)
        
        self.data_inicial = data_mais_recente
        
    def run_walk(self):

        self.otimizacao.estrategia.escolher_data = True

        datas_disponiveis = (self.otimizacao.estrategia.dados[self.otimizacao.estrategia.dados.index >= self.data_inicial]).index

        otimizacoes_possiveis = (len(datas_disponiveis) - 252 * self.anos_otimizacao)//int(252 * self.anos_teste)

        lista_df_otimizacao_por_periodo =[]
        lista_df_trades_oos = []

        df_analise_is_oos = pd.DataFrame(columns=['data_inicial_IS', 'data_final_IS', 'retorno_IS_am', 'data_inicial_OOS',
                                                'data_final_OOS', 'retorno_OOS_am', 'parametro1', 'parametro2'])

        soma_datas = 0

        for i in range(0, otimizacoes_possiveis + 1):

            self.otimizacao.estrategia.data_inicial = datas_disponiveis[int(0 + soma_datas)]
            self.otimizacao.estrategia.data_final = datas_disponiveis[int((252 * self.anos_otimizacao) + soma_datas)]

            self.otimizacao.run_optimize()

            #isso aqui tem que ser uma lista pra fazer os heatmaps
            lista_df_otimizacao_por_periodo.append(self.otimizacao.df_retorno_acum)

            #rodar o melhor modelo pra extrair os parametros e o df trade in sample

            melhor_modelo = self.otimizacao.df_retorno_acum[self.otimizacao.df_retorno_acum['retorno'] == self.otimizacao.df_retorno_acum['retorno'].max()]

            parametro_otimo1 = melhor_modelo['parametro1'].iat[0]
            parametro_otimo2 = melhor_modelo['parametro2'].iat[0]

            df_analise_is_oos.loc[i, 'data_inicial_IS'] = datas_disponiveis[int(0 + soma_datas)].date()
            df_analise_is_oos.loc[i, 'data_final_IS'] = datas_disponiveis[int((252 * self.anos_otimizacao) + soma_datas)].date()
            df_analise_is_oos.loc[i, 'parametro1'] = parametro_otimo1
            df_analise_is_oos.loc[i, 'parametro2'] = parametro_otimo2

            self.otimizacao.estrategia.parametro1 = parametro_otimo1
            self.otimizacao.estrategia.parametro2 = parametro_otimo2

            self.otimizacao.estrategia.run_strategy()

            trades_in_sample = self.otimizacao.estrategia.df_trades

            dias_backtest = len(trades_in_sample)

            retorno_acum = ((trades_in_sample['retorno'] + 1).cumprod() - 1).iat[-1]
            retorno_am = (1 + retorno_acum) ** (21/dias_backtest) - 1 

            df_analise_is_oos.loc[i, 'retorno_IS_am'] = retorno_am

            #OUT OF SAMPLE

            self.otimizacao.estrategia.data_inicial = datas_disponiveis[int((252 * self.anos_otimizacao + 1) + soma_datas)]

            try:

                self.otimizacao.estrategia.data_final = datas_disponiveis[int((252 * (self.anos_otimizacao + self.anos_teste)) + soma_datas)]

            except:

                self.otimizacao.estrategia.data_final = datas_disponiveis[-1]

            if i != 0:

                self.otimizacao.estrategia.numero_do_trade = numero_do_trade
                self.otimizacao.estrategia.comprado = comprado
                self.otimizacao.estrategia.vendido = vendido
                self.otimizacao.estrategia.cdi = comprado_cdi
                self.otimizacao.estrategia.fechamento = fechamento
                self.otimizacao.estrategia.zerou_compra = zerou_compra
                self.otimizacao.estrategia.zerou_venda = zerou_venda

                self.otimizacao.estrategia.run_strategy(reset = False)

            else:

                self.otimizacao.estrategia.run_strategy()

            numero_do_trade = self.otimizacao.estrategia.numero_do_trade
            comprado = self.otimizacao.estrategia.comprado 
            vendido = self.otimizacao.estrategia.vendido
            comprado_cdi = self.otimizacao.estrategia.cdi
            fechamento = self.otimizacao.estrategia.dados_filtrados_data.fechamento[-1]
            zerou_compra = self.otimizacao.estrategia.zerou_compra
            zerou_venda = self.otimizacao.estrategia.zerou_venda

            trades_outof_sample = self.otimizacao.estrategia.df_trades

            for z, indicador in enumerate(self.otimizacao.estrategia.lista_indicadores):

               trades_outof_sample[f'indicador{z}'] = indicador.values

            trades_outof_sample['data'] = pd.to_datetime(trades_outof_sample['data'])

            trades_outof_sample = pd.merge(trades_outof_sample, self.otimizacao.estrategia.dados, left_on = 'data', right_index = True)

            lista_df_trades_oos.append(trades_outof_sample)

            dias_backtest = len(trades_outof_sample)

            retorno_acum_oss = ((trades_outof_sample['retorno'] + 1).cumprod() - 1).iat[-1]
            retorno_am_oos = (1 + retorno_acum_oss) ** (21/dias_backtest) - 1

            df_analise_is_oos.loc[i, 'retorno_OOS_am'] = retorno_am_oos
            df_analise_is_oos.loc[i, 'data_inicial_OOS'] = datas_disponiveis[int((252 * self.anos_otimizacao + 1) + soma_datas)].date()
            
            try:

                df_analise_is_oos.loc[i, 'data_final_OOS'] = datas_disponiveis[int((252 * (self.anos_otimizacao + self.anos_teste)) + soma_datas)].date()

            except:

                df_analise_is_oos.loc[i, 'data_final_OOS'] = datas_disponiveis[-1].date()

            soma_datas = soma_datas + (252 * self.anos_teste)

        df_trades_out_of_sample = pd.concat(lista_df_trades_oos)

        #filtrando dados pra report (onde começa o df trades e termina)

        data_filtro = pd.to_datetime(df_trades_out_of_sample['data'].iloc[0])

        dados_filtrados_out_of_sample = self.dados[self.dados.index >= data_filtro]

        dados_filtrados_out_of_sample['retorno'] = dados_filtrados_out_of_sample['fechamento'].pct_change()

        df_trades_out_of_sample['cota'] = (df_trades_out_of_sample['retorno'] + 1).cumprod() - 1


        if self.parametro2 != ():
        

            MakeReportResult(df_trades=df_trades_out_of_sample, df_dados = dados_filtrados_out_of_sample, otimizacao=True,
                            df_otimizacao = df_analise_is_oos, lista_df_heatmap_parametros = lista_df_otimizacao_por_periodo,
                            nome_arquivo = self.nome_arquivo, caminho_benchmarks=self.otimizacao.estrategia.caminho_benchmarks,
                            caminho_imagens=self.otimizacao.estrategia.caminho_imagens)
            
        else:

            MakeReportResult(df_trades=df_trades_out_of_sample, df_dados = dados_filtrados_out_of_sample, otimizacao=True,
                            df_otimizacao = df_analise_is_oos, lista_df_heatmap_parametros = lista_df_otimizacao_por_periodo, 
                            parametro1_only = True, nome_arquivo = self.nome_arquivo, 
                            caminho_benchmarks=self.otimizacao.estrategia.caminho_benchmarks,
                            caminho_imagens=self.otimizacao.estrategia.caminho_imagens)