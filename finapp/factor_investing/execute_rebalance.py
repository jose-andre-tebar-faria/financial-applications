import wallet_manager as wm
import pandas as pd

def execute_rebalance(wallet_id, rebalance_date):

    wallet_manager = wm.WalletManager()

    file_not_found, compositions_df = wallet_manager.read_portifolios_composition(wallet_id)

    if file_not_found:

        number_of_compositions = 0
        last_dates = []
        compositions_df = pd.DataFrame()

        return number_of_compositions, last_dates, compositions_df
    else:

        compositions_df['rebalance_date'] = pd.to_datetime(compositions_df['rebalance_date'])

        # Filtrar o DataFrame pela wallet_id e a data passada
        df_filtrado = compositions_df[(compositions_df['wallet_id'] == str(wallet_id)) & (compositions_df['rebalance_date'] == pd.to_datetime(rebalance_date))]
        # df_filtrado = compositions_df[(compositions_df['rebalance_date'] == pd.to_datetime(rebalance_date))]
        # print(df_filtrado)

        # Verificar se há registros para a data passada
        if df_filtrado.empty:
            print(f"Nenhum registro encontrado para a wallet_id {wallet_id} na data {rebalance_date}.")
            return

            # Obter a última data existente no banco para a wallet_id antes da data passada
        ultima_data_antes_passada = compositions_df[(compositions_df['wallet_id'] == str(wallet_id)) & (compositions_df['rebalance_date'] < pd.to_datetime(rebalance_date))]['rebalance_date'].max()
        # ultima_data_antes_passada = compositions_df[(compositions_df['rebalance_date'] < pd.to_datetime(rebalance_date))]['rebalance_date'].max()

        if pd.isnull(ultima_data_antes_passada):
            # Se não houver data anterior, considerar que a variação é toda a quantidade da data passada
            df_resultado = df_filtrado[['wallet_id', 'rebalance_date', 'ticker', 'wallet_proportion']].copy()
            df_resultado['perc_variation'] = df_resultado['wallet_proportion']  # Variação é igual a composição atual quando não há data anterior
            df_resultado = df_resultado[['wallet_id', 'rebalance_date', 'ticker', 'perc_variation']]
            # print(df_resultado)
        else:
            # Filtrar o DataFrame para incluir apenas as linhas correspondentes à última data antes da data passada
            df_ultima_data_antes_passada = compositions_df[(compositions_df['wallet_id'] == str(wallet_id)) & (compositions_df['rebalance_date'] == ultima_data_antes_passada)]
            # df_ultima_data_antes_passada = compositions_df[(compositions_df['rebalance_date'] == ultima_data_antes_passada)]

            # Mesclar os DataFrames para obter as proporções para a data passada e a última data antes da data passada
            df_merge = pd.merge(df_filtrado, df_ultima_data_antes_passada, on='ticker', suffixes=('_passada', '_ultima'))

            # Calcular a variação percentual para cada ticker
            df_merge['perc_variation'] = ((df_merge['wallet_proportion_passada'] - df_merge['wallet_proportion_ultima']) / df_merge['wallet_proportion_ultima']) * 100

            # Selecionar as colunas necessárias
            df_resultado = df_merge[['wallet_id', 'rebalance_date_passada', 'ticker', 'perc_variation']]
            # df_resultado = df_merge[['rebalance_date_passada', 'ticker', 'perc_variation']]

        # Renomear as colunas
        df_resultado.columns = ['wallet_id', 'rebalance_date', 'ticker', 'perc_variation']

        # Exibir o resultado
        print(df_resultado)




wallet_id = 5312
# wallet_id = None

rebalance_date = '2023-11-20'

execute_rebalance(wallet_id, rebalance_date)
