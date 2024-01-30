import pandas as pd
import os
import numpy as np
from statsmodels.regression.rolling import RollingOLS
import statsmodels.api as sm
from dotenv import load_dotenv

#A COLUNA COM O INDICADOR TEM QUE SE CHAMAR "valor"

class MakeIndicator():

    def __init__(self):

        print("Inicializing MakeIndicator!")

        load_dotenv()

        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.databse_folder = os.getenv("DATABASE_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.databse_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)
        
        print("OK.")

    def making_momentum(self, months):

        print("Making Momentum " + str(months) + " month(s).")

        output_df = pd.DataFrame()
        quotations = pd.read_parquet('cotacoes.parquet')
        quotations['data'] = pd.to_datetime(quotations['data']).dt.date
        quotations = quotations[['data', 'ticker', 'preco_fechamento_ajustado']]

        quotations['valor'] = quotations.groupby('ticker')['preco_fechamento_ajustado'].pct_change(periods = (months * 21))
        quotations.loc[quotations['valor'] == 0, 'valor'] = pd.NA
        quotations.loc[quotations['valor'] == np.inf, 'valor'] = pd.NA
        quotations = quotations.dropna()
        output_df = quotations[['data', 'ticker', 'valor']]

        #print(output_df[output_df['ticker'] == 'WEGE3'])

        output_df.to_parquet(f'momento_{months}_meses.parquet', index = False)
        
        print("OK.")

    def median_volume(self,months):

        print("Making Median Volume " + str(months) + " month(s).")

        output_df = pd.DataFrame()
        quotations = pd.read_parquet('cotacoes.parquet')
        quotations['data'] = pd.to_datetime(quotations['data']).dt.date

        quotations = quotations[['data', 'ticker', 'volume_negociado']]
        quotations['volume_negociado'] = quotations.groupby('ticker')['volume_negociado'].fillna(0)
        quotations['valor'] = quotations.groupby('ticker')['volume_negociado'].rolling(months * 21).median().reset_index(0,drop=True)
        quotations = quotations.dropna()
        output_df = quotations[['data', 'ticker', 'valor']]

        #print(output_df[output_df['ticker'] == 'WEGE3'])

        output_df.to_parquet(f'volume_mediano.parquet', index = False)
        
        print("OK.")

    def ebit_divida_liquida(self):

        print("Making EBIT / Dívida_Líquida.")

        df_ebit = pd.read_parquet('Ebit12m.parquet')
        df_ebit = df_ebit.assign(id_dado = df_ebit['ticker'].astype(str) + "_" + df_ebit['data'].astype(str))
        df_ebit['valor'] = df_ebit['valor'].astype(float)
        df_ebit = df_ebit[['ticker', 'data', 'id_dado', 'valor']]
        df_ebit.columns = ['ticker', 'data', 'id_dado', 'ebit']

        df_divida_liquida = pd.read_parquet('DividaLiquida.parquet')
        df_divida_liquida = df_divida_liquida.assign(id_dado = df_divida_liquida['ticker'].astype(str) + "_" + df_divida_liquida['data'].astype(str))
        df_divida_liquida['valor'] = df_divida_liquida['valor'].astype(float)
        df_divida_liquida = df_divida_liquida[['id_dado', 'valor']]
        df_divida_liquida.columns = ['id_dado', 'divida']

        output_df = pd.DataFrame()
        output_df = pd.merge(df_ebit, df_divida_liquida, how = 'inner', on = 'id_dado')
        output_df['ebit_DL'] = pd.NA
        output_df.loc[output_df['divida'] <= 0, 'ebit_DL'] = 999
        output_df.loc[output_df['ebit'] <= 0, 'ebit_DL'] = -999
        output_df.loc[output_df['ebit_DL'].isna(), 'ebit_DL'] = (output_df[output_df['ebit_DL'].isna()]['ebit']/
                                                                output_df[output_df['ebit_DL'].isna()]['divida'])
        output_df = output_df[['data', 'ticker', 'ebit_DL']]
        output_df.columns = ['data', 'ticker', 'valor'] 

        #print(output_df[output_df['ticker'] == 'WEGE3'])

        output_df.to_parquet(f'ebit_dl.parquet', index = False)

        print("OK.")

    def pl_divida_bruta(self):

        print("Making Patrimônio_Líquido / Dívida_Bruta.")

        df_pl = pd.read_parquet('PatrimonioLiquido.parquet')
        df_pl = df_pl.dropna()
        df_pl = df_pl.assign(id_dado = df_pl['ticker'].astype(str) + "_" + df_pl['data'].astype(str))
        df_pl['valor'] = df_pl['valor'].astype(float)
        df_pl = df_pl[['data', 'ticker', 'valor', 'id_dado']]
        df_pl.columns = ['data', 'ticker', 'patrimonio_liquido', 'id_dado']

        df_divida_bruta = pd.read_parquet('DividaBruta.parquet')
        df_divida_bruta[df_divida_bruta['valor'] == '0.0'] = pd.NA
        df_divida_bruta = df_divida_bruta.dropna()
        df_divida_bruta = df_divida_bruta.assign(id_dado = df_divida_bruta['ticker'].astype(str) + "_" + df_divida_bruta['data'].astype(str))
        df_divida_bruta['valor'] = df_divida_bruta['valor'].astype(float)
        df_divida_bruta = df_divida_bruta[['id_dado', 'valor']]
        df_divida_bruta.columns = ['id_dado', 'divida']

        output_df = pd.DataFrame()
        output_df = pd.merge(df_pl, df_divida_bruta, how = 'inner', on = 'id_dado')
        output_df['PL_DB'] = pd.NA
        output_df.loc[output_df['patrimonio_liquido'] <= 0, 'PL_DB'] = 0
        output_df.loc[output_df['PL_DB'].isna(), 'PL_DB'] = (output_df[output_df['PL_DB'].isna()]['patrimonio_liquido']/
                                                                output_df[output_df['PL_DB'].isna()]['divida'])
        output_df = output_df[['data', 'ticker', 'PL_DB']]
        output_df.columns = ['data', 'ticker', 'valor'] 

        #print(output_df[output_df['ticker'] == 'WEGE3'])

        output_df.to_parquet('pl_db.parquet', index = False)

        print("OK.")

    def volatility(self, years):

        print("Making Volatility " + str(years) + " year(s).")

        output_df = pd.DataFrame()
        quotations = pd.read_parquet('cotacoes.parquet')
        quotations['data'] = pd.to_datetime(quotations['data']).dt.date
        quotations = quotations[['data', 'ticker', 'preco_fechamento_ajustado']]
        quotations['retorno'] = quotations.groupby('ticker')['preco_fechamento_ajustado'].pct_change()
        quotations.loc[quotations['retorno'] == 0, 'retorno'] = pd.NA
        quotations.loc[quotations['retorno'] == np.inf, 'retorno'] = pd.NA
        quotations['valor'] = quotations.groupby('ticker')['retorno'].rolling(window=int(252 * years), min_periods=int(252 * years * 0.8)).std().reset_index(0,drop=True)
        quotations = quotations.dropna()
        quotations['valor'] = quotations['valor'] * np.sqrt(252) 
        output_df = quotations[['data', 'ticker', 'valor']]

        #print(output_df[output_df['ticker'] == 'WEGE3'])

        output_df.to_parquet(f'vol_{int(252 * years)}.parquet', index = False)
        
        print("OK.")

    def beta(self, years):

        print("Making Beta " + str(years) + " year(s).")

        quotations = pd.read_parquet('cotacoes.parquet')
        cotaoces_ibov = pd.read_parquet('ibov.parquet')

        cotaoces_ibov.loc['5846'] = ['2023-08-10', 118349.60]

        cotaoces_ibov['retorno_ibov'] = cotaoces_ibov['fechamento'].pct_change()
        cotaoces_ibov = cotaoces_ibov[['data', 'retorno_ibov']]
        cotaoces_ibov['data'] = pd.to_datetime(cotaoces_ibov['data']).dt.date

        quotations['data'] = pd.to_datetime(quotations['data']).dt.date
        quotations = quotations[['data', 'ticker', 'preco_fechamento_ajustado']]
        quotations['retorno'] = quotations.groupby('ticker')['preco_fechamento_ajustado'].pct_change()
        quotations.loc[quotations['retorno'] == 0, 'retorno'] = pd.NA
        quotations.loc[quotations['retorno'] == np.inf, 'retorno'] = pd.NA

        dados_totais = pd.merge(quotations, cotaoces_ibov, on='data', how='inner')

        empresas = dados_totais['ticker'].unique()
        dados_totais = dados_totais.set_index('ticker')
        lista_df_betas = []

        for empresa in empresas:

            dado_empresa = dados_totais.loc[empresa]

            if dado_empresa.dropna().empty == False:

                if len(dado_empresa) > int(252 * years):

                    datas = dado_empresa.data.values
                    exog = sm.add_constant(dado_empresa.retorno_ibov)
                    model = RollingOLS(endog=dado_empresa.retorno.values, exog=exog, 
                                    window=int(252 * years), min_nobs = int(252 * years * 0.8))
                    betas = model.fit()
                    betas = betas.params
                    dado_empresa = betas.reset_index()
                    dado_empresa['data'] = datas
                    dado_empresa.columns = ['ticker', 'const', 'valor', 'data']
                    dado_empresa = dado_empresa[['data', 'ticker', 'valor']]
                    dado_empresa = dado_empresa.dropna()
                    lista_df_betas.append(dado_empresa)

        betas = pd.concat(lista_df_betas)
        
        #print(betas[betas['ticker'] == 'WEGE3'])

        betas.to_parquet(f'beta_{int(252 * years)}.parquet', index = False)
        
        print("OK.")

    def ratio_moving_mean(self, mm_curta, mm_longa):

        print("Making Ratio Moving Mean. Média curta: " + str(mm_curta) + " períodos. Média longa: " + str(mm_longa) + " períodos.")
        output_df = pd.DataFrame()
        quotations = pd.read_parquet('cotacoes.parquet')
        quotations['data'] = pd.to_datetime(quotations['data']).dt.date
        quotations = quotations[['data', 'ticker', 'preco_fechamento_ajustado']]
        quotations['media_curta'] = quotations.groupby('ticker')['preco_fechamento_ajustado'].rolling(window=mm_curta, min_periods=int(mm_curta * 0.8)).mean().reset_index(0,drop=True)
        quotations['media_longa'] = quotations.groupby('ticker')['preco_fechamento_ajustado'].rolling(window=mm_longa, min_periods=int(mm_longa * 0.8)).mean().reset_index(0,drop=True)
        quotations['valor'] = quotations['media_curta']/quotations['media_longa']
        output_df = quotations[['data', 'ticker', 'valor']]
        output_df = output_df.dropna()

        #print(output_df[output_df['ticker'] == 'WEGE3'])

        print(f'mm_{mm_curta}_{mm_longa}.parquet', output_df)
        output_df.to_parquet(f'mm_{mm_curta}_{mm_longa}.parquet', index = False)

        print("OK.")

    def peg_ratio(self):

        print("Making PEG Ration")

        #FAZER O CÁLCULO DO LUCRO POR AÇÃO
        net_profit = pd.read_parquet('LucroLiquido.parquet')
        net_profit = net_profit[['ticker', 'data', 'valor']]
        net_profit = net_profit.rename(columns={'valor': 'valor_np'})
        net_profit['data'] = pd.to_datetime(net_profit['data'])
        net_profit['ticker'] = net_profit['ticker'].astype(str)
        net_profit['valor_np'] = net_profit['valor_np'].astype(float)
        net_profit = net_profit.sort_values(['data', 'ticker'])
        # print('net_profit: \n', net_profit)

        total_number_of_stocks = pd.read_parquet('TotalAcoes.parquet')
        total_number_of_stocks = total_number_of_stocks[['ticker', 'data', 'valor']]
        total_number_of_stocks = total_number_of_stocks.rename(columns={'valor': 'valor_nos'})
        total_number_of_stocks['data'] = pd.to_datetime(total_number_of_stocks['data'])
        total_number_of_stocks['ticker'] = total_number_of_stocks['ticker'].astype(str)
        total_number_of_stocks['valor_nos'] = total_number_of_stocks['valor_nos'].astype(float)
        total_number_of_stocks = total_number_of_stocks.sort_values(['data', 'ticker'])
        # print('total_number_of_stocks: \n', total_number_of_stocks)

        peg_ratio = pd.merge(net_profit, total_number_of_stocks, on=['ticker', 'data'], suffixes=('_np', '_nos'))

        peg_ratio['valor_lpa'] = peg_ratio['valor_np'] / peg_ratio['valor_nos']

        # LPA base fintz
        # lpa_data = pd.read_parquet('LPA.parquet')
        # lpa_data = lpa_data[['ticker', 'data', 'valor']]
        # lpa_data = lpa_data.rename(columns={'valor': 'valor_lpa'})
        # lpa_data['data'] = pd.to_datetime(lpa_data['data'])
        # lpa_data['ticker'] = lpa_data['ticker'].astype(str)
        # lpa_data['valor_lpa'] = lpa_data['valor_lpa'].astype(float)
        # lpa_data = lpa_data.dropna()
        # print('lpa_data: \n', lpa_data)

        pl_data = pd.read_parquet('L_P.parquet')
        pl_data = pl_data[['ticker', 'data', 'valor']]
        pl_data = pl_data.rename(columns={'valor': 'valor_pl'})
        pl_data['data'] = pd.to_datetime(pl_data['data'])
        pl_data['ticker'] = pl_data['ticker'].astype(str)
        pl_data['valor_pl'] = pl_data['valor_pl'].astype(float)
        pl_data = pl_data.dropna()
        # print('pl_data: \n', pl_data)
        
        peg_ratio = pd.merge(peg_ratio, pl_data[['ticker', 'data', 'valor_pl']], on=['ticker', 'data'])
        # print('merged_data: \n', peg_ratio)#.groupby(['ticker', 'data']).mean())

        # Ordenar os dados por 'ticker' e 'data' para garantir a ordem correta
        peg_ratio = peg_ratio.sort_values(['data', 'ticker'])

        # Calcular variação percentual do LPA entre períodos
        peg_ratio['lpa_variation'] = peg_ratio.groupby('ticker')['valor_lpa'].pct_change()
        peg_ratio = peg_ratio.dropna()
        # print('peg_ratio: \n', peg_ratio)

        # Calcular PEG Ratio com tratamento para divisão por zero
        try:
            peg_ratio['peg_ratio'] = peg_ratio['valor_pl'] / (peg_ratio['lpa_variation'] - 1)
            peg_ratio['peg_ratio_invert'] = 1 / peg_ratio['peg_ratio']
        except ZeroDivisionError:
            # Tratamento para evitar divisão por zero
            print("Erro: Variação percentual do LPA não pode ser zero.")
            return None
        except pd.errors.OverflowError:
            # Tratamento para evitar overflow (inf ou -inf)
            print("Erro: Divisão resultou em infinito.")
            return None

        # Substituir infinitos (inf e -inf) por NaN
        peg_ratio.replace([np.inf, -np.inf], np.nan, inplace=True)
        peg_ratio = peg_ratio.sort_values(['data', 'ticker'])
        # print('peg_ratio: \n', peg_ratio)

        peg_ratio_to_parquet = peg_ratio[['ticker', 'data', 'peg_ratio_invert']]
        peg_ratio_to_parquet = peg_ratio_to_parquet.rename(columns={'peg_ratio_invert': 'valor'})

        peg_ratio_to_parquet.to_parquet('peg_ratio_invert.parquet', index = False)
        # print('peg_ratio_to_parquet: \n', peg_ratio_to_parquet)

        print("OK.")

        return peg_ratio[['ticker', 'data', 'peg_ratio']]
    
    def p_vp(self):

        print("Making P_VP")

        quotations = pd.read_parquet('cotacoes.parquet')
        quotations = quotations[['ticker', 'data', 'preco_fechamento_ajustado']]
        quotations = quotations.rename(columns={'preco_fechamento_ajustado': 'valor_quo'})
        quotations['data'] = pd.to_datetime(quotations['data'])
        quotations['ticker'] = quotations['ticker'].astype(str)
        quotations['valor_quo'] = quotations['valor_quo'].astype(float)
        print('quotations: \n', quotations)

        max_quotation_date = quotations['data'].max()

        patrimonial_value = pd.read_parquet('PatrimonioLiquido.parquet')
        patrimonial_value = patrimonial_value[['ticker', 'data', 'valor']]
        patrimonial_value = patrimonial_value.rename(columns={'valor': 'valor_pl'})
        patrimonial_value['data'] = pd.to_datetime(patrimonial_value['data'])
        patrimonial_value['ticker'] = patrimonial_value['ticker'].astype(str)
        patrimonial_value['valor_pl'] = patrimonial_value['valor_pl'].astype(float)
        patrimonial_value = patrimonial_value.sort_values(['data', 'ticker'])
        print('patrimonial_value: \n', patrimonial_value)

        new_patrimonial_value_records = pd.DataFrame()
        new_records = pd.DataFrame()
        for i in range(20):
            next_date = patrimonial_value['data'].max() + pd.DateOffset(days=i+1)
            next_date = next_date.strftime('%Y-%m-%d')
            new_records = patrimonial_value[patrimonial_value['data'] == patrimonial_value['data'].max()].copy()
            new_records['data'] = next_date
            new_patrimonial_value_records = pd.concat([new_patrimonial_value_records, new_records])
        
        # new_records['ticker'] = new_records.index

        print('new_patrimonial_value_records: \n', new_patrimonial_value_records)

        # Concatenar os DataFrames original e resultante
        sync_patrimonial_value = pd.concat([patrimonial_value, new_patrimonial_value_records], ignore_index=True)

        # Classificar o DataFrame por 'ticker' e 'data'
        sync_patrimonial_value['data'] = pd.to_datetime(sync_patrimonial_value['data']).dt.strftime('%Y-%m-%d')
        sync_patrimonial_value = sync_patrimonial_value.sort_values(['data']).reset_index(drop=True)
        print('sync_patrimonial_value: \n', sync_patrimonial_value)
        # print('sync_patrimonial_value WEGE3: \n', sync_patrimonial_value[sync_patrimonial_value['ticker'] == 'WEGE3'].tail(25))

        total_number_of_stocks = pd.read_parquet('TotalAcoes.parquet')
        total_number_of_stocks = total_number_of_stocks[['ticker', 'data', 'valor']]
        total_number_of_stocks = total_number_of_stocks.rename(columns={'valor': 'valor_nos'})
        total_number_of_stocks['data'] = pd.to_datetime(total_number_of_stocks['data'])
        total_number_of_stocks['ticker'] = total_number_of_stocks['ticker'].astype(str)
        total_number_of_stocks['valor_nos'] = total_number_of_stocks['valor_nos'].astype(float)
        total_number_of_stocks = total_number_of_stocks.sort_values(['data', 'ticker'])
        print('total_number_of_stocks: \n', total_number_of_stocks)

        new_total_number_of_stocks_records = pd.DataFrame()
        new_records = pd.DataFrame()
        for i in range(20):
            next_date = total_number_of_stocks['data'].max() + pd.DateOffset(days=i+1)
            next_date = next_date.strftime('%Y-%m-%d')
            new_records = total_number_of_stocks[total_number_of_stocks['data'] == total_number_of_stocks['data'].max()].copy()
            new_records['data'] = next_date
            new_total_number_of_stocks_records = pd.concat([new_total_number_of_stocks_records, new_records])
        
        # new_records['ticker'] = new_records.index

        print('new_total_number_of_stocks_records: \n', new_total_number_of_stocks_records)

        # Concatenar os DataFrames original e resultante
        sync_total_number_of_stocks = pd.concat([total_number_of_stocks, new_total_number_of_stocks_records], ignore_index=True)

        # Classificar o DataFrame por 'ticker' e 'data'
        sync_total_number_of_stocks['data'] = pd.to_datetime(sync_total_number_of_stocks['data']).dt.strftime('%Y-%m-%d')
        sync_total_number_of_stocks = sync_total_number_of_stocks.sort_values(['data']).reset_index(drop=True)
        print('sync_total_number_of_stocks: \n', sync_total_number_of_stocks)



        # total_number_of_stocks['data'] = pd.to_datetime(total_number_of_stocks['data'])
        # patrimonial_value['data'] = pd.to_datetime(patrimonial_value['data'])
        # total_number_of_stocks = total_number_of_stocks.dropna(subset=['ticker', 'data'])
        # patrimonial_value = patrimonial_value.dropna(subset=['ticker', 'data'])
        # quotations = quotations.dropna(subset=['ticker', 'data'])

        # total_number_of_stocks.info()
        # patrimonial_value.info()
        # quotations.info()
        # total_number_of_stocks['data'].fillna(pd.to_datetime('1900-01-01'), inplace=True)
        # patrimonial_value['data'].fillna(pd.to_datetime('1900-01-01'), inplace=True)
        # quotations['data'].fillna(pd.to_datetime('1900-01-01'), inplace=True)
        quotations['data'] = quotations['data'].astype('datetime64[us]')
        sync_patrimonial_value['data'] = sync_patrimonial_value['data'].astype('datetime64[us]')
        sync_total_number_of_stocks['data'] = sync_total_number_of_stocks['data'].astype('datetime64[us]')

        # print('total_number_of_stocks: \n', total_number_of_stocks)
        # print('patrimonial_value: \n', patrimonial_value)
        # print('quotations: \n', quotations)

        # Mesclar os DataFrames após a padronização da resolução
        merge_step1 = pd.merge(sync_total_number_of_stocks, sync_patrimonial_value, on=['ticker', 'data'], how='outer')
        p_vp = pd.merge(merge_step1, quotations, on=['ticker', 'data'], how='outer')

        p_vp = p_vp.sort_values(['data', 'ticker'])
        p_vp = p_vp.dropna()
        print('merged_data: \n', p_vp)
        
        try:
            p_vp['p_vp'] = (p_vp['valor_quo']) / (p_vp['valor_pl'] / p_vp['valor_nos'])
            p_vp['p_vp_invert'] = 1 / p_vp['p_vp']
        except ZeroDivisionError:
            print("Erro: Divisão não pode ser zero.")
            return None
        except pd.errors.OverflowError:
            print("Erro: Divisão resultou em infinito.")
            return None
        
        p_vp.replace([np.inf, -np.inf], np.nan, inplace=True)
        p_vp = p_vp.sort_values(['data', 'ticker'])
        print('p_vp: \n', p_vp)

        p_vp_to_parquet = p_vp[['ticker', 'data', 'p_vp_invert']]
        p_vp_to_parquet = p_vp_to_parquet.rename(columns={'p_vp_invert': 'valor'})

        p_vp_to_parquet.to_parquet('p_vp_invert.parquet', index = False)
        print('p_vp_to_parquet: \n', p_vp_to_parquet)

        print("OK.")

        return p_vp[['ticker', 'data', 'p_vp']]

    def p_ebit(self):

        print("Making P_EBIT")

        quotations = pd.read_parquet('cotacoes.parquet')
        quotations = quotations[['ticker', 'data', 'preco_fechamento_ajustado']]
        quotations = quotations.rename(columns={'preco_fechamento_ajustado': 'valor_quo'})
        quotations['data'] = pd.to_datetime(quotations['data'])
        quotations['ticker'] = quotations['ticker'].astype(str)
        quotations['valor_quo'] = quotations['valor_quo'].astype(float)
        quotations = quotations.sort_values(['data', 'ticker'])
        # print('quotations: \n', quotations)

        ebit = pd.read_parquet('Ebit12m.parquet')
        ebit = ebit[['ticker', 'data', 'valor']]
        ebit = ebit.rename(columns={'valor': 'valor_eb'})
        ebit['data'] = pd.to_datetime(ebit['data'])
        ebit['ticker'] = ebit['ticker'].astype(str)
        ebit['valor_eb'] = ebit['valor_eb'].astype(float)
        ebit = ebit.sort_values(['data', 'ticker'])
        # print('ebit: \n', ebit)

        p_ebit = pd.merge(quotations, ebit, on=['ticker', 'data'], how='outer')
        p_ebit = p_ebit.dropna()
        # print('merged_data: \n', p_ebit)
        
        try:
            p_ebit['p_ebit'] = 100000000 * (p_ebit['valor_quo']) / (p_ebit['valor_eb'])
            p_ebit['p_ebit_invert'] = 1 / p_ebit['p_ebit']
        except ZeroDivisionError:
            print("Erro: Divisão não pode ser zero.")
            return None
        except pd.errors.OverflowError:
            print("Erro: Divisão resultou em infinito.")
            return None
        
        p_ebit.replace([np.inf, -np.inf], np.nan, inplace=True)
        p_ebit = p_ebit.sort_values(['data', 'ticker'])
        # print('p_ebit: \n', p_ebit)

        p_ebit_to_parquet = p_ebit[['ticker', 'data', 'p_ebit_invert']]
        p_ebit_to_parquet = p_ebit_to_parquet.rename(columns={'p_ebit_invert': 'valor'})

        p_ebit_to_parquet.to_parquet('p_ebit_invert.parquet', index = False)
        # print('p_ebit_to_parquet: \n', p_ebit_to_parquet)

        print("OK.")

        return p_ebit[['ticker', 'data', 'p_ebit']]
    
    def net_margin(self):

        print("Making NET_MARGIN")

        net_profit = pd.read_parquet('LucroLiquido.parquet')
        net_profit = net_profit[['ticker', 'data', 'valor']]
        net_profit = net_profit.rename(columns={'valor': 'valor_np'})
        net_profit['data'] = pd.to_datetime(net_profit['data'])
        net_profit['ticker'] = net_profit['ticker'].astype(str)
        net_profit['valor_np'] = net_profit['valor_np'].astype(float)
        net_profit = net_profit.sort_values(['data', 'ticker'])
        # print('net_profit: \n', net_profit)

        net_revenue = pd.read_parquet('ReceitaLiquida.parquet')
        net_revenue = net_revenue[['ticker', 'data', 'valor']]
        net_revenue = net_revenue.rename(columns={'valor': 'valor_nr'})
        net_revenue['data'] = pd.to_datetime(net_revenue['data'])
        net_revenue['ticker'] = net_revenue['ticker'].astype(str)
        net_revenue['valor_nr'] = net_revenue['valor_nr'].astype(float)
        net_revenue = net_revenue.sort_values(['data', 'ticker'])
        # print('net_revenue: \n', net_revenue)

        net_margin = pd.merge(net_profit, net_revenue, on=['ticker', 'data'], how='outer')
        net_margin = net_margin.sort_values(['ticker', 'data'])
        net_margin = net_margin.dropna()
        # print('merged_data: \n', net_margin)
        
        try:
            net_margin['net_margin'] = (net_margin['valor_np']) / (net_margin['valor_nr'])
        except ZeroDivisionError:
            print("Erro: Divisão não pode ser zero.")
            return None
        except pd.errors.OverflowError:
            print("Erro: Divisão resultou em infinito.")
            return None
        
        net_margin.replace([np.inf, -np.inf], np.nan, inplace=True)
        net_margin = net_margin.sort_values(['data', 'ticker'])
        # print('net_margin: \n', net_margin)

        net_margin_to_parquet = net_margin[['ticker', 'data', 'net_margin']]    
        net_margin['net_margin'] = net_margin['net_margin'] * 100
        net_margin_to_parquet = net_margin_to_parquet.rename(columns={'net_margin': 'valor'})  

        net_margin_to_parquet.to_parquet('net_margin.parquet', index = False)
        # print('net_margin_to_parquet: \n', net_margin_to_parquet)  

        print("OK.")
        
        return net_margin[['ticker', 'data', 'net_margin']]

if __name__ == "__main__":

    indicator = MakeIndicator()

    # SEEMS WORKING but different not always from statusinvest.com
    peg_ratio = indicator.peg_ratio()
    print('last 15 peg_ratios: \n', peg_ratio.tail(15)) #[[peg_ratio['ticker'] == 'WEGE3']]

    # APPROVED
    p_vp = indicator.p_vp()
    print(p_vp.tail(15))

    # IN TESTS (follow tendences OK)
    p_ebit = indicator.p_ebit()
    print(p_ebit.tail(15))

    # APPROVED but different not always from statusinvest.com
    net_margin = indicator.net_margin()
    print(net_margin.tail(15))