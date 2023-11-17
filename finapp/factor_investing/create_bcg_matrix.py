import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import update_asset_profile as uap

class BcgMatrix:

    def __init__(self, bcg_dimensions):
        
        self.bcg_dimensions = bcg_dimensions
        print("\nInicializing BCG Matrix!")

        load_dotenv()

        self.asset_acess = uap.UpdateAssetProfile()

        current_folder = os.getcwd()

        project_folder = os.getenv("PROJECT_FOLDER")
        databse_folder = os.getenv("DATABASE_FOLDER")
        self.full_desired_path = os.path.join(project_folder,databse_folder)

        if(current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

#
##
###
# CALCULANDO MATRIX BCG
###
##
#
    def create_bcg_matrix(self):

        print('\n=== CALCULANDO MATRIZ BCG! ==')

        asset_profile_database = self.asset_acess.read_profile_database()

        sectors = asset_profile_database.drop_duplicates('sector')['sector'].sort_values(ascending = True)
        sectors.reset_index(inplace=True, drop=True)
        list_sectors = list(sectors)
        print('\nForam localizados', len(list_sectors), ' setores.')

        subsectors = asset_profile_database.drop_duplicates('subsector')['subsector'].sort_values(ascending = True)
        subsectors.reset_index(inplace=True, drop=True)
        list_subsectors = list(subsectors)
        print('\nForam localizados', len(list_subsectors), ' subsetores.')
        # print(list_subsectors)

        acum_category_profile = asset_profile_database

        for dimension in self.bcg_dimensions:

            dimension_column = dimension + '_marketshare'
            dimension_destin_column = dimension + '_bcg_category'

            if(dimension == 'sector'):
                list_category = list_sectors
            if(dimension == 'subsector'):
                list_category = list_subsectors
            # print(list_category)

            for category_filter in list_category:

                # print('=== category: ', category_filter)
                category_profile_database = asset_profile_database[['asset', dimension, dimension_column, 'last_growth_rate']][asset_profile_database[dimension] == category_filter].sort_values(by=['last_growth_rate', dimension], ascending = False)
                # print(category_profile_database)

                threshold_last_growth_rate = category_profile_database['last_growth_rate'].astype(float).mean()
                threshold_category_marketshare = category_profile_database[dimension_column].astype(float).mean()
                # print('\nthreshold_last_growth_rate: \n', threshold_last_growth_rate)
                # print('threshold_', dimension , '_marketshare: \n', threshold_category_marketshare)

                conditions = [
                    (asset_profile_database['last_growth_rate'] >= threshold_last_growth_rate) & (asset_profile_database[dimension_column] >= threshold_category_marketshare),
                    (asset_profile_database['last_growth_rate'] < threshold_last_growth_rate) & (asset_profile_database[dimension_column] >= threshold_category_marketshare),
                    (asset_profile_database['last_growth_rate'] >= threshold_last_growth_rate) & (asset_profile_database[dimension_column] < threshold_category_marketshare),
                    (asset_profile_database['last_growth_rate'] < threshold_last_growth_rate) & (asset_profile_database[dimension_column] < threshold_category_marketshare)
                ]

                categories = ['Estrela', 'Vaca Leiteira', 'Ponto de Interrogação', 'Abacaxi']
                category_profile_database[f'{dimension}_bcg_category'] = pd.DataFrame(np.select(conditions, categories))
                category_profile = category_profile_database.drop(columns=[dimension, dimension_column, 'last_growth_rate'])
                # print(category_profile)

                for index, row in category_profile.iterrows():
                    asset = row['asset']
                    # print(asset)
                    bcg_category = row[dimension_destin_column]
                    # print(bcg_category)

                    # Encontrar o índice correspondente no DataFrame 1
                    index_to_go = acum_category_profile.index[acum_category_profile['asset'] == asset].tolist()
                    # print(index_df1)

                    if index_to_go:
                        acum_category_profile.at[index_to_go[0], dimension_destin_column] = bcg_category
                        # print(acum_category_profile[acum_category_profile['asset'] == asset])
                        # print('')

        bcg_matrix = acum_category_profile[['asset', 'sector', 'sector_marketshare', 'subsector', 'subsector_marketshare', 'last_growth_rate', 'sector_bcg_category', 'subsector_bcg_category']]
        # print('Estrelas DUPLAS: \n', bcg_matrix[(bcg_matrix['sector_bcg_category'] == 'Estrela') & (bcg_matrix['subsector_bcg_category'] == 'Estrela')])
        # print('Estrelas do Setor: \n', bcg_matrix[(bcg_matrix['sector_bcg_category'] == 'Estrela')])
        # print('Estrelas do Subsetor: \n', bcg_matrix[bcg_matrix['subsector_bcg_category'] == 'Estrela'])
        print('\nBCG Matrix: \n', bcg_matrix)

        print('\t==saving BCG matrix to file bcg_matrix.parquet.')
        bcg_matrix.to_parquet(f'{self.full_desired_path}/bcg_matrix.parquet', index = True)

    def read_bcg_matrix_database(self):
        
        bcg_matrix_read = pd.read_parquet(f'{self.full_desired_path}/bcg_matrix.parquet')
        bcg_matrix_read_df = pd.DataFrame(bcg_matrix_read)
        bcg_matrix_read_df.reset_index(inplace=True)
        # print(bcg_matrix_read_df)

        return bcg_matrix_read_df

if __name__ == "__main__":
    
    bcg_dimensions = ['sector', 'subsector']

    bcg_matrix = BcgMatrix(bcg_dimensions)

    bcg_matrix.create_bcg_matrix()