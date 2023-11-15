from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
import os
from dotenv import load_dotenv

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
            # print('\nfinding dropdown sectors element\n')
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

assets_database.to_parquet(f'{full_desired_path}/assets_database.parquet', index = True)




api_key = 'UTBW1G0YXLD6LKJ5'

tickers = ['WEGE', 'AAPL',
#  'JBDU3', 'CSAN3', 'TOYB3', 'DOHL4', 'GOAU3', 'COCE5', 'BTOW3', 'BAZA3',
#  'ACGU3', 'BRFS3', 'BRKM5', 'TCNO4', 'LOGN3', 'SBSP3', 'GAZO4', 'POMO4', 'TRPL4',
#  'EALT4', 'MARI3', 'PMAM4', 'CGAS5', 'FIBR3', 'INEP4', 'PLAS3', 'IGUA6', 'CCHI3',
#  'CAMB4', 'IGTA3', 'TRIS3', 'TEMP3', 'FTRX4', 'BMEB3', 'SCAR3', 'PMET6', 'MNDL4',
#  'SULT4', 'AMBV3', 'UOLL4', 'MRSL4', 'LUPA3', 'RHDS3', 'CCIM3', 'TRPN3', 'CYRE3',
#  'CTKA4', 'PFRM3', 'BTTL3', 'EKTR4', 'LEVE4', 'ITSA3', 'HGTX3', 'ROMI3', 'IMBI4',
#  'HYPE3', 'REDE4', 'BMIN4', 'BNCA3', 'CZRS4', 'GETI4', 'IGBR3', 'MWET4', 'ABYA3',
#  'LREN3', 'TNLP3', 'RNAR3', 'LIGT3', 'MAGG3', 'HOOT4', 'VPSC4', 'CCRO3', 'EZTC3',
#  'ENMA3B', 'COCE3', 'ALPA4', 'TEKA4', 'CESP5', 'BEES3', 'IDNT3', 'KEPL3', 'POSI3',
#  'IDVL4', 'LCSA3', 'INEP3', 'TLPP3', 'CREM3', 'PRBC4', 'CSMG3', 'BICB4', 'UNIP6',
#  'VIVO3', 'ELET3', 'TBLE3', 'ODPV3', 'ELEK4', 'VAGV4', 'SULT3', 'MNPR3', 'PETR4',
#  'AELP3', 'STRP4', 'PNOR6', 'BDLL4', 'OGXP3', 'OHLB3', 'TVIT3', 'GVTT3', 'RPAD6',
#  'DIRR3', 'CTPC3', 'INET3', 'CRUZ3', 'NETC4', 'ESTR4', 'BBAS3', 'CEPE5', 'DTCY3',
#  'RCSL4', 'EBTP3', 'TEND3', 'HAGA4', 'TKNO4', 'BRTO3', 'RDCD3', 'GPCP3', 'CGRA3',
#  'IGUA5', 'EBTP4', 'UNIP5', 'SUZB5', 'CESP6', 'CLSC6', 'FFTL4', 'HETA4', 'SLED4',
#  'CBMA4', 'SNSY5', 'RPMG3', 'GUAR4', 'BBDC3', 'LPSB3', 'MYPK3', 'BRSR3', 'SMTO3',
#  'GGBR3', 'FJTA4', 'GETI3', 'LLXL3', 'LAME3', 'CRDE3', 'DAYC4', 'FHER3', 'MTSA4',
#  'PMAM3', 'TENE7', 'LUXM4', 'UGPA4', 'JFEN3', 'FESA4', 'BVMF3', 'EUCA4', 'ABCB4',
#  'CBEE3', 'LAME4', 'UNIP3', 'MLFT4', 'BRIV3', 'STBP11', 'ITSA4', 'CTIP3', 'CIEL3',
#  'CESP3', 'PNOR5', 'FRAS4', 'TIBR5', 'MTIG3', 'DROG3', 'GTDP3B', 'TAMM4', 'TOTS3',
#  'TLPP4', 'IENG5', 'VALE5', 'RPMG4', 'DASA3', 'SLCE3', 'TELB4', 'FLRY3', 'USIM5',
#  'TOYB4', 'HBTS5', 'DXTG4', 'BRAP4', 'DTEX3', 'EMBR3', 'PTBL3', 'BBRK3', 'MGEL4',
#  'JHSF3', 'BISA3', 'VALE3', 'TMAR5', 'PCAR5', 'CTNM4', 'ABNB3', 'PINE4', 'MDIA3',
#  'PRVI3', 'HBOR3', 'MEND5', 'SFSA4', 'MEDI3', 'GOAU4', 'FRIO3', 'SANB11', 'WHRL4',
#  'MMXM3', 'RENT3', 'SHUL4', 'ELPL6', 'AVIL3', 'NATU3', 'ALLL3', 'PTPA4', 'CTAX4',
#  'CPLE6', 'BTTL4', 'BPNM4', 'CLAN4', 'MNDL3', 'TCSL3', 'KROT11', 'SGPS3', 'TCNO3',
#  'SGAS4', 'ALLL4', 'GLOB3', 'ENBR3', 'VULC3', 'KSSA3', 'AGRO3', 'BRIV4', 'ELET6',
#  'MPXE3', 'TRNA11', 'TCSL4', 'RAPT3', 'BEEF3', 'WISA3', 'RDNI3', 'BRML3', 'CNFB4',
#  'ALLL11', 'IVTT3', 'CPLE3', 'POMO3', 'BMEB4', 'CEBR6', 'INPR3', 'SCLO4', 'BAUH4',
#  'EMAE4', 'ESTC3', 'CMIG3', 'TRFO4', 'MTIG4', 'BEMA3', 'AMBV4', 'MRVE3', 'USIM3',
#  'BGIP4', 'PDGR3', 'ECOD3', 'GUAR3', 'SULA11', 'EQTL3', 'CCHI4', 'CARD3', 'ENGI4',
#  'KLBN4', 'TROR4', 'NOVA4B', 'AGIN3', 'JBDU4', 'FESA3', 'RAPT4', 'ILMD4', 'TGMA3', 
#  'TXRX4', 'TCSA3', 'BBDC4', 'RSID3', 'PSSA3', 'TPIS3', 'PETR3', 'MRFG3',
#     'BEES4', 'CPFE3', 'LIXC4', 'EVEN3', 'BOBR4', 'MULT3', 'BMTO4', 'SAPR4', 'ITUB3', 'WISA4',
#     'BALM4', 'VIVO4', 'CRIV4', 'BRAP3', 'AEDU11', 'ETER3', 'TELB3', 'AMIL3', 'SANB4', 'JBSS3',
#     'CMIG4', 'BRKM3', 'BRSR6', 'SANB3', 'GOLL4', 'ITUB4', 'FBMC4', 'GRND3', 'IENG3', 'BRTO4',
#     'RSIP4', 'CBMA3', 'CSNA3', 'CRIV3', 'GSHP3', 'GFSA3', 'GGBR4', 'TNLP4', 'CCPR3', 'TUPY3',
#     'LLIS3', 'RSIP3', 'CTNM3', 'PNVL4', 'RCSL3', 'TIBR6', 'ENGI11', 'DUQE4', 'CGAS3', 'TMAR3',
#     'SZPQ4', 'CEEB3', 'BRSR5', 'SEBB11', 'RANI4', 'BALM3', 'CEBR5', 'CTAX3', 'CEDO4', 'SJOS4',
#     'EEEL4B', 'FIGE4', 'ECPR4', 'SLED3', 'FIGE3', 'ENGI3', 'BGIP3', 'CTSA3', 'MEND6', 'ELEK3',
#     'PNVL3', 'GTDP4B', 'SOND5', 'REDE3', 'MAPT4', 'BMTO3', 'NETC3', 'CMGR4', 'CAFE4', 'BAHI3',
#     'IGUA3', 'LFFE4', 'KLBN3', 'ITEC3', 'PTNT3', 'CTSA4', 'MSPA4', 'RPAD3', 'BRGE3', 'CALI4',
#     'AMCE3', 'TEKA3', 'CEEB5', 'SGEN4', 'PTNT4', 'CIQU4', 'BSLI3', 'CSRN3', 'CEDO3', 'SPRI3',
#     'UCOP4', 'FTRX3', 'ELPL3', 'RANI3', 'BIOM4', 'CGRA4', 'ALPA3', 'BICB3', 'HAGA3', 'TAMM3',
#     'NAFG4', 'CSRN6', 'ELPL5', 'PATI3', 'BRKM6', 'BMIN3', 'CMGR3', 'CELP7', 'CEPE6', 'MERC4',
#     'BSLI4', 'RPAD5', 'CELP5', 'NUTR3M', 'CLSC3', 'BRGE12', 'WHRL3', 'PATI4', 'IMBI3', 'BRGE6',
#     'BRGE11', 'JOPA4', 'EEEL3B', 'TENE5', 'CSAB3', 'LIXC3', 'LCSA4', 'LIPR3', 'CTKA3', 'CSAB4',
#     'AMPI3', 'SJOS3', 'CSRN5', 'MERC3', 'NORD3', 'PEAB4', 'BHGR3', 'BNBR4', 'CIQU3', 'DHBI4',
#     'SGAS3', 'ECPR3', 'FFTL3', 'TIBR3', 'SPRI5', 'BMKS3', 'SOND6', 'NOVA3B', 'CPTP3B', 'MWET3',
#     'TRPL3', 'CEED4B', 'STLB3', 'CEED3B', 'CAFE3', 'TUPY4', 'JOPA3', 'TNCP4', 'SNSY3', 'EUCA3',
#     'DOCA3', 'ELUM4', 'AFLU3', 'PEAB3', 'SPRI6', 'USIM6', 'GEPA3', 'ALSC3', 'GEPA4', 'TNCP3',
#     'CEBR3', 'CEGR3', 'BNBR3', 'CNFB3', 'DOCA4', 'VSPT3', 'MPLU3', 'QGNP4B', 'LHER4', 'TXRX3',
#     'REEM4', 'ELET5', 'FJTA3', 'ESTR3', 'AGEI3', 'LARK4', 'MOAR3', 'BDLL3', 'LFFE3', 'MLFT3',
#     'CORR4', 'BUET4', 'GPAR3', 'SGEN3', 'AHEB3', 'CASN4', 'MAPT3', 'EKTR3', 'CALI3', 'UGPA3',
#     'VINE5', 'AHEB6', 'PCAR3', 'AHEB5', 'BRPR3', 'NEMO4', 'FBMC3', 'CASN3', 'BRGE8', 'SCLO3',
#     'OSXB3', 'FRAS3', 'MSPA3', 'ECOR3', 'WMBY3', 'GRND11', 'GAZO3', 'COBE3B', 'HETA3', 'BRGE5',
#     'MILS3', 'SUZB6', 'JSLG3', 'BIOM3', 'RSUL4', 'COBE6B', 'TKNO3', 'BUET3', 'AMAR3', 'VINE6',
#     'RNEW11', 'VINE3', 'MTSA3', 'SPRT3B', 'TERI3', 'BRGE7', 'TMAR6', 'RDTR3', 'EEEL4', 'CEED3',
#     'EEEL3', 'DOHL3', 'CEED4', 'CPLE5', 'LUXM3', 'HRTP3', 'PMET5', 'BRIN3', 'VLID3', 'SOND3',
#     'CELP6', 'AFLT3', 'PRTX3', 'AEDU3', 'ILMD3', 'IDVL3', 'RAIA3', 'ELPL4', 'CLSC5', 'COBE5B',
#     'LEVE3', 'MRSL3', 'EALT3', 'ARZZ3', 'SSBR3', 'AUTM3', 'QGEP3', 'DHBI3', 'IMCH3',
#     'MGEL3', 'PCAR4', 'CELP3', 'SHOW3', 'MGLU3', 'AZEV4', 'VIVR3', 'AORE3', 'DOMO3',
#     'COCE6', 'AZEV3', 'BPHA3', 'RJCP3', 'QUAL3', 'TECN3', 'DUQE3', 'ABRE11', 'MRSA3B',
#     'TIMP3', 'CEPE3', 'VIVT3', 'VIVT4', 'VAGR3', 'QGNP3B', 'SNSY6', 'RADL3', 'CLSC4',
#     'KROT3', 'KROT4', 'OIBR4', 'OIBR3', 'VVAR3', 'LCAM3', 'BBTG11', 'UCAS3', 'CCXC3',
#     'TAEE11', 'VIGR3', 'MAOR3B', 'MAOR4B', 'ARTR3', 'LINX3', 'SNSL3M', 'BSEV3',
#     'ALUP11', 'BBSE3', 'SMLE3', 'CTAX11', 'SAPR3', 'CPRE3', 'RNEW3', 'ENEV3', 'ANIM3',
#     'SEER3', 'ABEV3', 'KLBN11', 'CVCB3', 'VVAR11', 'BIOM3M', 'SNSL3', 'NUTR3',
#     'PRML3', 'BPAN4', 'ABRE3', 'MRSA6B', 'RLOG3', 'OFSA3', 'ENMT3', 'OGSA3', 'MEAL3',
#     'RUMO3', 'MEND3', 'ENMT4', 'PARC3', 'SWET3', 'PRIO3', 'APTI4', 'SEDU3', 'NAFG3',
#     'CRPG5', 'VVAR4', 'ATOM3', 'CRPG6', 'SHUL3', 'FRTA3', 'TIET4', 'TIET11', 'TIET3',
#     'PTPA3', 'VTLM3', 'BPAC5', 'BPAC3', 'EGIE3', 'MRSA5B', 'STBP3', 'ALUP4', 'ALUP3',
#     'AALR3', 'TESA3', 'ADHM3', 'MOVI3', 'PARD3', 'BBTG12', 'BPAC11', 'RAIL3',
#     'GFSA11', 'RNEW4', 'CRPG3', 'SULA4', 'AZUL4', 'SULA3', 'WIZS3', 'TAEE4', 'TAEE3',
#     'WLMM4', 'WLMM3', 'CRFB3', 'IRBR3', 'OMGE3', 'ODER4', 'PPLA11', 'DMMO3', 'CAML3',
#     'SMLS3', 'SUZB3', 'AFLU5', 'SAPR11', 'BRDT3', 'BKBR3', 'JPSA4', 'JPSA3', 'LIQO3',
#     'B3SA3', 'GNDI3', 'HAPV3', 'BIDI11', 'BIDI4', 'BPAR3', 'LOGG3', 'APER3', 'SQIA3',
#     'BIDI3', 'YDUQ3', 'ALSO3', 'VIVA3', 'COGN3', 'BMGB11', 'CEAB3', 'TASA3', 'TASA4',
#     'BMGB4', 'NTCO3', 'EQPA3', 'EQPA5', 'EQPA7', 'CAMB3', 'EQPA6', 'BOBR3', 'MTRE3',
#     'EQMA3B', 'LWSA3', 'MDNE3', 'PRNR3', 'ATMP3', 'ALPK3', 'BPAC13', 'PDTC3', 'AMBP3',
#     'SOMA3', 'LJQQ3', 'DMVF3', 'PGMN3', 'LAVV3', 'JSLG11', 'PETZ3', 'PLPL3', 'SIMH3',
#     'CURY3', 'HBSA3', 'GPCP4', 'MELK3', 'BOAS3', 'SEQL3', 'GMAT3', 'TIMS3', 'TFCO4',
    'CASH3', 'ENJU3', 'AERI3', 'RRRP3', 'RDOR3', 'AVLL3', 'NGRD3', 'HBRE3', 'VAMO3',
    'ESPA3', 'INTB3', 'MOSI3', 'MBLY3', 'POWE3', 'JALL3', 'BMOB3', 'CSED3', 'WEST3', 
    'OPCT3', 'ELMD3', 'ORVR3', 'CMIN3', 'ASAI3', 'AESB3', 'SBFG3', 'ALLD3', 'MATD3',
    'BLAU3', 'GGPS3', 'CPLE11', 'CXSE3', 'SOJA3', 'MODL11', 'MODL4', 'MODL3', 'IFCM3', 'RECV3', 'NINJ3', 'DOTZ3',
    'DEXP4', 'DEXP3', 'EPAR3', 'BRBI11', 'TTEN3', 'SMFT3', 'BRIT3', 'CLSA3', 'LAND3', 'RAIZ4', 'VVEO3', 'ONCO3',
    'KRSA3', 'VIIA3', 'FNCN3', 'DXCO3', 'VITT3', 'SYNE3', 'BLUT4', 'BLUT3', 'GETT3', 'GETT4', 'GETT11', 'VBBR3',
    'PORT3', 'IGTI11', 'IGTI3', 'MEGA3', 'AURE3', 'NEXP3', 'DMFN3', 'CSUD3', 'IGTI4', 'ZAMP3', 'WIZC3', 'VSTE3',
    'FIEI3', 'PINE3', 'BHIA3', 'YBRA4', 'ALOS3', 'ALOS3'
    ]

# tickers = set(tickers)
# len_tickers = len(tickers)
# print(len_tickers)