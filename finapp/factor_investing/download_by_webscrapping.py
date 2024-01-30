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

        sectors_dropdown = list(range(11, 20))
        # sectors_dropdown = list(range(2, 20)) comunic
        # sectors_dropdown = list(range(9, 20)) saude
        subsectors_dropdown = list(range(0, 20))
        segments_index_max = list(range(0, 20))

        assets_database = pd.DataFrame(columns=['asset', 'sector', 'subsector', 'segment', 'ticker', 'cnpj', 'mai_activiity', 'company_name', 'trading_name'])
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
                    time.sleep(1)
                    
                    while True:
                        # print('Abrindo Subsetores!')
                        try:
                            for subsector_index in subsectors_dropdown:
                                subsectors_selector = '/html/body/app-root/app-companies-home/div/div/div/div/div[2]/div[2]/div/app-companies-home-filter-classification/form/table/tbody/tr[' + str(subsector_index+1) + ']/td[1]'
                                # print('\t\t', subsectors_selector)
                                
                                subsector = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, subsectors_selector)))
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
                                            segments = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, segments_selector)))
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
                                            segment = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, segment_selector)))
                                            segment_to_dict = segment.text
                                            print('\t\t\t', segment_to_dict)

                                            # ACESSO AOS TICKERS
                                            button_current_segment = WebDriverWait(driver, 20).until(
                                                EC.visibility_of_element_located((By.XPATH, segment_selector))
                                            )
                                            button_current_segment.click()
                                            data = WebDriverWait(driver, 20).until(
                                                EC.visibility_of_element_located((By.XPATH, '//*[@id="nav-bloco"]/div'))
                                            )

                                            total_assets = 0

                                            ## VERIFICAÇÃO DE NÚMERO DE ITENS NA PÁGINA PARA EXPANDIR SE NECESSÁRIO
                                            while True:
                                                # print('Verificando mais de uma página por asset!')
                                                try:

                                                    dropdown_assets_per_page_element = WebDriverWait(driver, 20).until(
                                                        EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/app-companies-search/div/form/div[3]/div[1]/select'))
                                                    )
                                                    # print('dropdown_element: ', dropdown_element.text)
                                                    dropdown_assets = Select(dropdown_assets_per_page_element)

                                                    dropdown_assets.select_by_value('120')
                                                    time.sleep(1)

                                                    break
                                                except Exception as e:
                                                    time.sleep(0.5)
                                                break

                                            index_asset_max = list(range(1, 101))


                                            while True:
                                                try:
                                                    for index in index_asset_max:

                                                        content_list = []

                                                        asset_selector = '#nav-bloco > div > div:nth-child(' + str(index) + ') > div > div > h5'
                                                        # print('asset_selector: ', asset_selector)
                                                        
                                                        # asset_code = data.find_element(By.CSS_SELECTOR, asset_selector)
                                                        
                                                        asset_code = driver.find_element(By.CSS_SELECTOR, asset_selector)

                                                        # asset_code = WebDriverWait(driver, 10).until(
                                                        #     EC.visibility_of_element_located((By.CSS_SELECTOR, asset_selector))
                                                        # )
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






                                                        # descobrindo o número de seguimentos
                                                        assets_selector = '/html/body/app-root/app-companies-search/div/form/div[2]/div[1]/div'
                                                        # print('segments_selector: ', segments_selector)
                                                        number_of_assets = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, assets_selector)))
                                                        elementos_filhos = number_of_assets.find_elements(By.XPATH, '*')
                                                        numero_de_elementos = len(elementos_filhos)
                                                        print('numero_de_elementos: ', numero_de_elementos)

                                                        total_assets+=numero_de_elementos

                                                        if numero_de_elementos > 1:
                                                            asset_details_selector = '/html/body/app-root/app-companies-search/div/form/div[2]/div[1]/div/div[' + str(index) + ']'
                                                            # print('assets_selector: ', asset_details_selector)
                                                        else:
                                                            asset_details_selector = '/html/body/app-root/app-companies-search/div/form/div[2]/div[1]/div/div/div/div'
                                                            
                                                            # print('assets_selector: ', asset_details_selector)

                                                        # ACESSO DETALHADOS AOS TICKERS
                                                        button_asset_details = WebDriverWait(driver, 20).until(
                                                            EC.visibility_of_element_located((By.XPATH, asset_details_selector))
                                                        )
                                                        button_asset_details.click()
                                                        
                                                        # time.sleep(1)

                                                        company_name_selector = '/html/body/app-root/app-companies-menu-select/div/div/div[1]/h2' 
                                                        # print('company_name_selector: ', company_name_selector)
                                                        trading_name_selector = '/html/body/app-root/app-companies-menu-select/div/app-companies-overview/div/div[1]/div/div/p[2]'
                                                        # print('trading_name_selector: ', trading_name_selector)
                                                        
                                                        ticker_selector = '/html/body/app-root/app-companies-menu-select/div/app-companies-overview/div/div[1]/div/div/p[4]/a'
                                                        
                                                        # print('ticker_selector: ', ticker_selector)
                                                        
                                                        ticker_exisitent = False

                                                        try:

                                                            time.sleep(1)
                                                            ticker = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, ticker_selector)))
                                                            ticker_to_dict = ticker.text
                                                            print('\t\t\t\t\t', ticker_to_dict)

                                                            ticker_exisitent = True
                                                        except:
                                                            print('\t\t\t\t\t\tNão existe ticker!!')

                                                        if ticker_exisitent:
                                                            main_activity_selector = '/html/body/app-root/app-companies-menu-select/div/app-companies-overview/div/div[1]/div/div/div[3]/p[2]'
                                                            # print('main_activity_selector: ', main_activity_selector)
                                                            cnpj_selector = '/html/body/app-root/app-companies-menu-select/div/app-companies-overview/div/div[1]/div/div/div[2]/p[2]'
                                                            # print('cnpj_selector: ', cnpj_selector)
                                                            
                                                            content_list.append(ticker_to_dict)
                                                            # print(content_list)
                                                        else:
                                                            main_activity_selector = '/html/body/app-root/app-companies-menu-select/div/app-companies-overview/div/div[1]/div/div/div[2]/p[2]'
                                                            # print('main_activity_selector: ', main_activity_selector)
                                                            cnpj_selector = '/html/body/app-root/app-companies-menu-select/div/app-companies-overview/div/div[1]/div/div/div[1]/p[2]'
                                                            # print('cnpj_selector: ', cnpj_selector)
                                                            
                                                            content_list.append('')
                                                            # print(content_list)

                                                        time.sleep(1)
                                                        cnpj = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, cnpj_selector)))
                                                        cnpj_to_dict = cnpj.text
                                                        print('\t\t\t\t\t', cnpj_to_dict)

                                                        content_list.append(cnpj_to_dict)
                                                        # print(content_list)

                                                        main_activity_exisitent = False

                                                        try:
                                                            time.sleep(1)
                                                            main_activity = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, main_activity_selector)))
                                                            main_activity_to_dict = main_activity.text
                                                            print('\t\t\t\t\t', main_activity_to_dict)

                                                            main_activity_exisitent = True
                                                        except:
                                                            print('\t\t\t\t\t\tNão existe atividade principal!!')

                                                        if main_activity_exisitent:
                                                            content_list.append(main_activity_to_dict)
                                                            # print(content_list)
                                                        else:
                                                            content_list.append('')

                                                        time.sleep(1)
                                                        company_name = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, company_name_selector)))
                                                        company_name_to_dict = company_name.text
                                                        print('\t\t\t\t\t', company_name_to_dict)

                                                        content_list.append(company_name_to_dict)
                                                        # print(content_list)

                                                        time.sleep(0.5)
                                                        trading_name = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, trading_name_selector)))
                                                        trading_name_to_dict = trading_name.text
                                                        print('\t\t\t\t\t', trading_name_to_dict)

                                                        content_list.append(trading_name_to_dict)
                                                        # print(content_list)

                                                        driver.back()
                                                        time.sleep(1)







                                                        assets_database.loc[asset_to_dict] = content_list
                                                        print(assets_database)
                                                    break
                                                except Exception as e:
                                                    # acabou
                                                    # print(e)
                                                    break

                                            back_button = WebDriverWait(driver, 20).until(
                                                EC.visibility_of_element_located((By.CSS_SELECTOR, '#divContainerIframeB3 > form > button'))
                                            )
                                            back_button.click()

                                            time.sleep(1)

                                            button_expand = WebDriverWait(driver, 20).until(
                                                EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/app-companies-home/div/div/div/div/div[2]/div[1]/div/div/a/h6'))
                                            )
                                            button_expand.click()

                                            # selecionando o termo do dropdown de subsetores
                                            # print('\nfinding dropdown sectors element\n')
                                            dropdown_element = WebDriverWait(driver, 20).until(
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
        print('Foram salvos', len(assets_database), 'assets!')
        print('Foram encontrados', total_assets, 'assets!')

        load_dotenv()

        current_folder = os.getcwd()

        project_folder = os.getenv("PROJECT_FOLDER")
        databse_folder = os.getenv("DATABASE_FOLDER")
        full_desired_path = os.path.join(project_folder,databse_folder)

        if(current_folder != full_desired_path):
            os.chdir(full_desired_path)

        assets_database.to_parquet(f'{full_desired_path}/sectors_assets_b3_webscraping.parquet', index = True)


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
    
    # asset_logos.getting_asset_logos_google_by_site()

    asset_logos.getting_b3_assets_sector_by_site()