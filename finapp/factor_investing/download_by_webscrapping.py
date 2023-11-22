from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import base64
from io import BytesIO
from PIL import Image
import time
import pandas as pd
import os
import numpy as np
from dotenv import load_dotenv

import update_asset_profile as uap

class DownloadByWebscrapping:

    def __init__(self):        
        
        print("Inicializing Downloader by Webscrapping!")

        load_dotenv()

        self.api_key = os.getenv("API_FINTZ")

        self.headers = {'accept': 'application/json',
                        'X-API-Key': self.api_key}
        
        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.databse_folder = os.getenv("DATABASE_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.databse_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)
        
        print("OK.")

    def getting_b3_assets_sector_by_site(self):

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        driver.get('''https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/''')
        driver.maximize_window()

        print('\nfinding button_expand')
        button_expand = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/app-companies-home/div/div/div/div/div[2]/div[1]/div/div/a/h6'))
        )
        button_expand.click()

        # listando todos os setores contidos no dropdown e salvando na lista = list_sectors
        index_sectors_max = list(range(1, 101))
        list_sectors = []

        while True:
            print('Buscando Setores existentes no dropdown!')
            try:
                for index in index_sectors_max:
                    #print(index)
                    sectors_selector = '#accordionClassification > div > app-companies-home-filter-classification > form > div.row > div > div > select > option:nth-child(' + str(index) + ')'
                    #print(subsectors_selector)
                    subsectors_name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, sectors_selector)))
                    list_sectors.append(subsectors_name.text)
                    # print(subsectors_name.text)
                    index+=1
                break
            except Exception as e:
                print("OK!\n.\n.")
                break

        print('\nSETORES:', list_sectors)

        sectors_dropdown = list(range(0, 20))
        subsectors_dropdown = list(range(0, 20))
        segments_index_max = list(range(0, 20))

        assets_database = pd.DataFrame(columns=['asset', 'sector', 'subsector', 'segment'])
        assets_database.set_index('asset', inplace=True)

        while True:
            print('Abrindo Setores!\n')
            try:
                # print(subsectors_dropdown)
                for sector_index in sectors_dropdown:
                    
                    print('SETOR: ', list_sectors[sector_index])

                    # selecionando o termo do dropdown de setores
                    dropdown_element = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="accordionClassification"]/div/app-companies-home-filter-classification/form/div[1]/div/div/select'))
                    )
                    # print('dropdown_element: ', dropdown_element.text)
                    dropdown = Select(dropdown_element)

                    dropdown.select_by_value(list_sectors[sector_index])
                    time.sleep(2)
                    
                    while True:
                        # print('Abrindo Subsetores!')
                        try:
                            for subsector_index in subsectors_dropdown:
                                subsectors_selector = '/html/body/app-root/app-companies-home/div/div/div/div/div[2]/div[2]/div/app-companies-home-filter-classification/form/table/tbody/tr[' + str(subsector_index+1) + ']/td[1]'
                                # print('\t\t', subsectors_selector)
                                
                                subsector = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, subsectors_selector)))
                                subsector_to_dict = subsector.text
                                print('\t\t', subsector_to_dict)
                                
                                # segments
                                while True:
                                    # print('Abrindo Segments!')
                                    try:
                                        for segment_index in segments_index_max:

                                            # descobrindo o número de seguimentos
                                            segments_selector = '/html/body/app-root/app-companies-home/div/div/div/div/div[2]/div[2]/div/app-companies-home-filter-classification/form/table/tbody/tr[' + str(subsector_index+1) + ']/td[2]'
                                            # print('', segments_selector)
                                            segments = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, segments_selector)))
                                            # print('\t\t\t', segments.text)
                                            elementos_filhos = segments.find_elements(By.XPATH, '*')
                                            numero_de_elementos = len(elementos_filhos)
                                            # print('numero de elementos: ', numero_de_elementos)

                                            if(numero_de_elementos != 1):
                                                segment_selector = '/html/body/app-root/app-companies-home/div/div/div/div/div[2]/div[2]/div/app-companies-home-filter-classification/form/table/tbody/tr[' + str(subsector_index+1) +']/td[2]/p[' + str(segment_index+1) + ']/a'
                                            elif(segment_index == 0):
                                                segment_selector = '/html/body/app-root/app-companies-home/div/div/div/div/div[2]/div[2]/div/app-companies-home-filter-classification/form/table/tbody/tr[' + str(subsector_index+1) +']/td[2]/p/a'
                                            else:
                                                segment_selector = ''
                                            
                                            # print('segment_selector: ', segment_selector)
                                            segment = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, segment_selector)))
                                            segment_to_dict = segment.text
                                            print('\t\t\t', segment_to_dict)

                                            # ACESSO AOS TICKERS
                                            button_current_segment = WebDriverWait(driver, 10).until(
                                                EC.visibility_of_element_located((By.XPATH, segment_selector))
                                            )
                                            button_current_segment.click()
                                            data = WebDriverWait(driver, 10).until(
                                                EC.visibility_of_element_located((By.XPATH, '//*[@id="nav-bloco"]/div'))
                                            )

                                            ## VERIFICAÇÃO DE NÚMERO DE ITENS NA PÁGINA PARA EXPANDIR SE NECESSÁRIO
                                            while True:
                                                # print('Verificando mais de uma página por asset!')
                                                try:

                                                    dropdown_assets_per_page_element = WebDriverWait(driver, 10).until(
                                                        EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/app-companies-search/div/form/div[3]/div[1]/select'))
                                                    )
                                                    # print('dropdown_element: ', dropdown_element.text)
                                                    dropdown_assets = Select(dropdown_assets_per_page_element)

                                                    dropdown_assets.select_by_value('120')
                                                    time.sleep(1)

                                                    break
                                                except Exception as e:
                                                    time.sleep(0.05)
                                                break

                                            index_asset_max = list(range(1, 101))

                                            while True:
                                                try:
                                                    for index in index_asset_max:

                                                        content_list = []

                                                        asset_selector = '#nav-bloco > div > div:nth-child(' + str(index) + ') > div > div > h5'
                                                        asset_code = data.find_element(By.CSS_SELECTOR, asset_selector)
                                                        print('\t\t\t\t', asset_code.text)

                                                        ## INSERIR NO DICIONÁRIO

                                                        asset_to_dict = str(asset_code.text)
                                                        # print(asset_to_dict)
                                                        sector_to_dict = str(list_sectors[sector_index])
                                                        # print(sector_to_dict)
                                                        content_list.append(sector_to_dict)
                                                        # print(subsector_to_dict)
                                                        content_list.append(subsector_to_dict)
                                                        # print(segment_to_dict)
                                                        content_list.append(segment_to_dict)
                                                        # print(content_list)
                                                        
                                                        assets_database.loc[asset_to_dict] = content_list
                                                        # print(assets_database)
                                                    break
                                                except Exception as e:
                                                    # acabou
                                                    break

                                            back_button = WebDriverWait(driver, 10).until(
                                                EC.visibility_of_element_located((By.CSS_SELECTOR, '#divContainerIframeB3 > form > button'))
                                            )
                                            back_button.click()

                                            time.sleep(1)

                                            button_expand = WebDriverWait(driver, 10).until(
                                                EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/app-companies-home/div/div/div/div/div[2]/div[1]/div/div/a/h6'))
                                            )
                                            button_expand.click()

                                            # selecionando o termo do dropdown de subsetores
                                            # print('\nfinding dropdown sectors element\n')
                                            dropdown_element = WebDriverWait(driver, 10).until(
                                                EC.visibility_of_element_located((By.XPATH, '//*[@id="accordionClassification"]/div/app-companies-home-filter-classification/form/div[1]/div/div/select'))
                                            )
                                            # print('dropdown_element: ', dropdown_element.text)
                                            dropdown = Select(dropdown_element)

                                            dropdown.select_by_value(list_sectors[sector_index])
                                            time.sleep(1)
                                        break
                                    except Exception as e:
                                        time.sleep(0.05)
                                    break
                            break
                        except Exception as e:
                            time.sleep(0.05)
                        break
                break
            except Exception as e:
                print("OK!\n.\n.")
                break

        # print(assets_database)
        # print('Foram encontrados ', len(assets_database), 'tickers!')

        print(assets_database)
        print('Foram encontrados', len(assets_database), 'tickers!')

        load_dotenv()

        current_folder = os.getcwd()

        project_folder = os.getenv("PROJECT_FOLDER")
        databse_folder = os.getenv("DATABASE_FOLDER")
        full_desired_path = os.path.join(project_folder,databse_folder)

        if(current_folder != full_desired_path):
            os.chdir(full_desired_path)

        assets_database.to_parquet(f'{full_desired_path}/sectors_assets_b3_webscraping.parquet', index = True)


        # api_key = 'UTBW1G0YXLD6LKJ5'


    def getting_asset_logos_google_by_site(self):

        # URL da página da web que contém a imagem
        url_base = 'https://www.google.com/search?q=cotações+'

        profile_updater = uap.UpdateAssetProfile()

        assets_database_df = profile_updater.read_profile_database()

        assets_list = list(assets_database_df['asset'])
        # print(assets_list)

        tickers_list = [element + '3' for element in assets_list]
        tickers_list = tickers_list[150:]
        print(tickers_list)
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        current_folder = os.getcwd()

        project_folder = os.getenv("PROJECT_FOLDER")
        databse_folder = os.getenv("LOGOS_FOLDER")
        full_desired_path = os.path.join(project_folder,databse_folder)

        if(current_folder != full_desired_path):
            os.chdir(full_desired_path)

        for ticker in tickers_list:

            url = url_base + ticker
            # print(url)
            file_name = f'logo_{ticker}.png'

            if os.path.exists(file_name):

                print(f'O arquivo {file_name} já existe.\n')

            else:
                
                delay_to_request = np.random.randint(2,6)
                time.sleep(delay_to_request)
                driver.get(url)

                try:
                    img_element = driver.find_element(By.XPATH, '//*[@id="dimg_1"]')
                    img_src = img_element.get_attribute('src')

                    img_data = img_src.split(',')[1]
                    img_binary = base64.b64decode(img_data)

                    print('Logo referente ao ticker: ', ticker)
                    # Salvar a imagem localmente ou realizar outras operações, por exemplo, exibir a imagem usando a biblioteca Pillow (PIL)
                    with BytesIO(img_binary) as img_buffer:
                        
                        img = Image.open(img_buffer)
                        img.save(file_name)
                        print('Download OK.')
                except NoSuchElementException:
                    print(f'O a logo referente ao ticker {ticker} não pôde ser encontrado.\n')

        # driver.maximize_window()


if __name__ == "__main__":
    print('')

    asset_logos = DownloadByWebscrapping()
    
    asset_logos.getting_asset_logos_google_by_site()


