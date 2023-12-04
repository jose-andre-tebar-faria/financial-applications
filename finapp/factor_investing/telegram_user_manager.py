import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from io import StringIO
from datetime import datetime
import time


class TelegramUserManager:   

    def __init__(self):
                
        print(".\nInicializing TelegramUserManager!")
        
        load_dotenv()

        current_folder = os.getcwd()

        project_folder = os.getenv("PROJECT_FOLDER")
        databse_folder = os.getenv("DATABASE_FOLDER")
        self.full_desired_path = os.path.join(project_folder,databse_folder)

        if(current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

    def read_telegram_users(self):

        file_not_found = False

        try:
            telegram_users_parquet = pd.read_parquet(f'{self.full_desired_path}/telegram_users.parquet')
            telegram_users_df = pd.DataFrame(telegram_users_parquet)
            telegram_users_df['onboarding_date'] = pd.to_datetime(telegram_users_df['onboarding_date'])
            telegram_users_df['user_id'] = telegram_users_df['user_id'].astype(str)
            telegram_users_df['username'] = telegram_users_df['username'].astype(str)
            telegram_users_df['first_name'] = telegram_users_df['first_name'].astype(str)
            telegram_users_df['last_name'] = telegram_users_df['last_name'].astype(str)
            telegram_users_df['is_bot'] = telegram_users_df['is_bot'].astype(bool)
            telegram_users_df['is_adm'] = telegram_users_df['is_adm'].astype(bool)
            telegram_users_df = telegram_users_df.sort_values(['onboarding_date', 'username'])
            print('telegram_users: \n', telegram_users_df)
        except:
            telegram_users_df = None
            file_not_found = True
            print("File not found. Creating...")
            telegram_users_df = pd.DataFrame(columns=['user_id', 'username', 'first_name', 'last_name', 'is_bot', 'is_adm', 'onboarding_date'])
            telegram_users_df['onboarding_date'] = pd.to_datetime(telegram_users_df['onboarding_date'])
            telegram_users_df['user_id'] = telegram_users_df['user_id'].astype(str)
            telegram_users_df['username'] = telegram_users_df['username'].astype(str)
            telegram_users_df['first_name'] = telegram_users_df['first_name'].astype(str)
            telegram_users_df['last_name'] = telegram_users_df['last_name'].astype(str)
            telegram_users_df['is_bot'] = telegram_users_df['is_bot'].astype(bool)
            telegram_users_df['is_adm'] = telegram_users_df['is_adm'].astype(bool)
            telegram_users_df = telegram_users_df.sort_values(['onboarding_date', 'username'])
            # print(telegram_users_df.dtypes)
            
            telegram_users_df.to_parquet(f'{self.full_desired_path}/telegram_users.parquet', index = True)

        return file_not_found, telegram_users_df

    def prepare_telegram_user(self,user_id, username, first_name=None, last_name=None, is_bot=None, is_adm=None):
        
        telegram_user_df = pd.DataFrame(columns=['user_id', 'username', 'first_name', 'last_name', 'is_bot', 'is_adm', 'onboarding_date'])

        create_date_auto = datetime.now()
        create_date_auto = create_date_auto.strftime('%Y-%m-%d')
        telegram_user_df.at[0,'onboarding_date'] = create_date_auto
        telegram_user_df['onboarding_date'] = pd.to_datetime(telegram_user_df['onboarding_date'])

        telegram_user_df['user_id'] = telegram_user_df['user_id'].astype(str)
        telegram_user_df.at[0,'user_id'] = str(user_id)

        telegram_user_df['username'] = telegram_user_df['username'].astype(str)
        telegram_user_df.at[0,'username'] = str(username)

        telegram_user_df['first_name'] = telegram_user_df['first_name'].astype(str)
        telegram_user_df.at[0,'first_name'] = str(first_name)

        telegram_user_df['last_name'] = telegram_user_df['last_name'].astype(str)
        telegram_user_df.at[0,'last_name'] = str(last_name)

        telegram_user_df['is_bot'] = telegram_user_df['is_bot'].astype(bool)
        telegram_user_df.at[0,'is_bot'] = bool(is_bot)

        telegram_user_df['is_adm'] = telegram_user_df['is_adm'].astype(bool)
        telegram_user_df.at[0,'is_adm'] = bool(is_adm)

        telegram_user_df = telegram_user_df.sort_values(['onboarding_date', 'username'])

        # print('telegram_users: \n', telegram_user_df)

        return telegram_user_df


    def delete_telegram_user(self, username = None, user_id = None):
        
        if(username == None):
            username = ''

        file_not_found, telegram_user_database_df = TelegramUserManager.read_telegram_users(self)
        telegram_user_database_df = telegram_user_database_df.reset_index(drop=True)
        telegram_user_database_df['user_id'] = telegram_user_database_df['user_id'].astype(str)
        telegram_user_database_df['username'] = telegram_user_database_df['username'].astype(str)
        print('\ntelegram_user_database_df: \n', telegram_user_database_df)

        if(file_not_found):
            print('\telegram_users.parquet does not exist!')
        else:
            condition = (telegram_user_database_df['user_id'] == user_id) & (telegram_user_database_df['username'] == username)
            user_to_delete = telegram_user_database_df[condition]
            print('Setup to delete: \n', user_to_delete)

            if(user_to_delete.empty):
                print('Setup does not exist!')
            else:
                new_database = telegram_user_database_df.drop(telegram_user_database_df[condition].index)
                print('New setup: \n', new_database)
                
                new_database.to_parquet(f'{self.full_desired_path}/telegram_users.parquet', index = True)

    def verify_telegram_user(self, telegram_user_df):

        new_user = False
        username_existent = ''
        user_id_existent = ''
        # print('\ntelegram_users: \n', telegram_user_df)

        file_not_found, telegram_user_database_df = TelegramUserManager.read_telegram_users(self)
        # print('\ntelegram_user_database_df: \n', telegram_user_database_df)
        
        verifying_presence = pd.merge(telegram_user_database_df, telegram_user_df, on = ['user_id'], how = 'left', indicator=True)

        found_in_database = (verifying_presence['_merge'] == 'both').any()
        # print(found_in_database)
        
        if(found_in_database):
            verifying_presence = verifying_presence[verifying_presence['_merge'] == 'both']
            found_user = verifying_presence[['user_id', 'username_x']][verifying_presence['_merge'] == 'both']
            found_user.rename(columns={'username_x': 'username',}, inplace=True)
            print('\nfound_user: \n', found_user)
            username_existent = verifying_presence['username_x'].iloc[0]
            # print('\nusername_existent', username_existent)
        
        if(found_in_database == False):
            print('.\n.\nnew user!\n.\n.')
            new_user = True
        else:
            print('.\nknown user!\n.')
            user_id_existent = verifying_presence['user_id'].iloc[0]
            print('user_detected: \n', telegram_user_database_df[telegram_user_database_df['user_id'] == user_id_existent])

        return new_user, verifying_presence, username_existent, user_id_existent

    def insert_telegram_user(self, telegram_user_df):
        
        file_not_found = False
        
        print('telegram_user_df: \n', telegram_user_df)

        try:
            telegram_users_parquet = pd.read_parquet(f'{self.full_desired_path}/telegram_users.parquet')
            telegram_users_df = pd.DataFrame(telegram_users_parquet)
            telegram_users_df['onboarding_date'] = pd.to_datetime(telegram_users_df['onboarding_date'])
            telegram_users_df['user_id'] = telegram_users_df['user_id'].astype(str)
            telegram_users_df['username'] = telegram_users_df['username'].astype(str)
            telegram_users_df['first_name'] = telegram_users_df['first_name'].astype(str)
            telegram_users_df['last_name'] = telegram_users_df['last_name'].astype(str)
            telegram_users_df['is_bot'] = telegram_users_df['is_bot'].astype(bool)
            telegram_users_df['is_adm'] = telegram_users_df['is_adm'].astype(bool)
            telegram_users_df = telegram_users_df.sort_values(['onboarding_date', 'username'])
            print('telegram_users: \n', telegram_users_df)
        except:
            telegram_users_df = None
            file_not_found = True
            print("File not found.")
            
        updated_setup = pd.concat([telegram_users_df, telegram_user_df], ignore_index=False)
        updated_setup = updated_setup.reset_index(drop=True)
        print('updated_setup: \n', updated_setup)
        
        updated_setup.to_parquet(f'{self.full_desired_path}/telegram_users.parquet', index = True)



#
## MAIN
#
if __name__ == "__main__":
        
    print("\nInicializing Telegram User Manager!")

    telegram_user_manager = TelegramUserManager()

    telegram_user_manager.read_telegram_users()

    # telegram_users_df = telegram_user_manager.prepare_telegram_user(user_id='1',username='aaa')
    # telegram_user_manager.verify_telegram_user(telegram_users_df)

    telegram_user_manager.delete_telegram_user(username = 'jandretebarf', user_id = '6013346178')