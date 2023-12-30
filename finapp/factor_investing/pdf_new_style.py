from fpdf import FPDF
import matplotlib.font_manager

import os
from dotenv import load_dotenv


class PDF(FPDF):

    def header(self):
        
        diretorio_atual = os.getcwd()
        print("Diretório atual para header PDF:", diretorio_atual)

        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.databse_folder = os.getenv("IMAGES_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.databse_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

        # Desenhar um retângulo para definir a cor de fundo
        self.set_fill_color(0, 31, 63)  # Azul Escuro - Cor RGB
        self.rect(0, 0, 230, 297, 'F')

        # Configurar a cor do texto após o desenho do retângulo
        self.set_text_color(255, 255, 255)  # Texto branco para contrastar com o fundo

        largura_pagina = self.w
        x = (largura_pagina - 27) / 2

        # Adiciona a imagem à posição calculada
        self.image('./colored_eye.png', x, 2, 21)

        # font_name = "Gill Sans MT Ext Condensed Bold"
        # font_path = "C:\Windows\Fonts\GLSNECB.TTF"
        # font_name = "Gill Sans Ultra Bold"
        # font_path = "C:\Windows\Fonts\GILSANUB.TTF"
        font_name = "Franklin Gothic Heavy"
        font_path = "C:\Windows\Fonts\FRAHVIT.TTF"
        # font_name = "Lucida Sans Typewriter"
        # font_path = "C:\Windows\Fonts\LTYPEO.TTF"

        self.add_font(font_name, '', font_path, uni=True)
        self.set_font(font_name, size=23)
        self.ln(15)
        
        self.set_draw_color(255, 215, 0)

        self.cell(0, 15, "FINAPP Report", border=True, ln=True, align="C")
        self.ln(5)

    def footer(self):

        self.set_y(-15)

        font_name = "Franklin Gothic Heavy"
        font_path = "C:\Windows\Fonts\FRAHVIT.TTF"
        self.add_font(font_name, '', font_path, uni=True)
        self.set_font(font_name, size=12)

        self.cell(0, 10, f"{self.page_no()}/{{nb}}", align="C")

    def add_custom_font(self, font_name, font_path, style='', size=12):
        self.add_font(font_name, style, font_path, uni=True)
        self.set_font(font_name, size)

class MakePDF():

    def __init__(self):
        
        load_dotenv()

        self.nome_arquivo = 'prototype_pdf.pdf'

        self.pdf = PDF("P", "mm", "Letter")
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.alias_nb_pages()

        # Configurar a cor do texto após o desenho do retângulo
        self.pdf.set_text_color(255, 255, 255)  # Texto branco para contrastar com o fundo
        self.pdf.set_draw_color(35, 155, 132)

        self.pdf.add_page()

        # Desenhar um retângulo para definir a cor de fundo
        self.pdf.set_fill_color(0, 31, 63)  # Azul Escuro - Cor RGB

        # Configurar a cor do texto após o desenho do retângulo
        self.pdf.set_text_color(255, 255, 255)  # Texto branco para contrastar com o fundo
        self.pdf.set_draw_color(35, 155, 132)

        self.pdf_intro()

        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.databse_folder = os.getenv("IMAGES_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.databse_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

        self.pdf_intro()
        self.pdf.ln(32)
        self.tabela_dias()
        self.grafico_retorno_acum()
        # self.tabelas_estatisticas_gerais()
        # self.eventos_estresse_e_dias_sem_lucro()
        # self.grafico_underwater()
        self.retorno_ano_a_ano_mes_a_mes()
        # self.grafico_janelas_moveis()

        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.desired_folder = os.getenv("INDICATORS_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.desired_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

        self.file_name = os.path.join(self.full_desired_path,self.nome_arquivo)

        self.pdf.output(self.file_name)

    def pdf_intro(self):
        # # Obtenha uma lista de todas as fontes disponíveis
        # font_list = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

        # # Imprima a lista de fontes
        # for font_path in font_list:
        #     font_name = matplotlib.font_manager.FontProperties(fname=font_path).get_name()
        #     print(f"Fonte: {font_name}, Caminho: {font_path}")
        
        font_name = "Segoe UI"
        font_path = "C:\Windows\Fonts\segoeuisl.ttf"
        self.pdf.add_font(font_name, '', font_path, uni=True)
        self.pdf.set_font(font_name, size=9)
        self.pdf.set_draw_color(255, 215, 0)
        self.pdf.set_x(28)

        self.pdf.cell(w=149, h=27, txt="Essa vai ser a intro da parada!", ln = False,  border = True, fill = True, align = "C")

    def tabela_dias(self):

        self.pdf.set_draw_color(255, 215, 0)
        self.pdf.set_font('Arial', '', 8)
        self.pdf.cell(20, 7, "Dia inicial", ln = False,  border = True, fill = True, align = "C")
        self.pdf.cell(20, 7, f"2020-02-12", ln = True, 
                border = True, fill = False, align = "C")

        self.pdf.cell(20, 7, "Dia final", ln = False,  border = True, fill = True, align = "C")
        self.pdf.cell(20, 7, f"3729-11-23", ln = True, 
                border = True, fill = False, align = "C")
        
        self.pdf.cell(20, 7, "Dias totais", ln = False,  border = True, fill = True, align = "C")
        self.pdf.cell(20, 7, f"42", ln = True, 
                border = True, fill = False, align = "C")

        self.pdf.ln(7)

    def grafico_retorno_acum(self):

        self.pdf.image("./rent_acum.png", w = 140, h = 80, x = 35, y = 107)

    def tabelas_estatisticas_gerais(self):
            
        self.pdf.cell(0, 60, ln = True)

        self.pdf.set_draw_color(255, 215, 0)

        self.pdf.set_font('Arial', 'B', 11)

        self.pdf.cell(8, 10, ln = False)

        self.pdf.cell(70, 10, "Estatísticas de Retorno e Risco", ln = False, align = "C")

        self.pdf.cell(40, 10, ln = False)

        self.pdf.cell(70, 10, "Estatísticas de Trade", ln = True, align = "C")

        indicadores_risco_retorno = [self.retorno_acum_modelo, self.retorno_acum_cdi, self.retorno_acum_ibov,
                                     self.retorno_aa_modelo, self.vol_ultimo_ano, self.sharpe, self.var_diario, self.turn_over_medio, 
                                     self.drawdown_maximo]
        
        nomes_risco_retorno = ["Retorno acum. modelo", "Retorno acum. CDI", "Retorno acum. IBOV", "Retorno a.a. modelo",
                               "Vol 252d", "Índice Sharpe", 'VAR diário 95%', 'Turn over carteira', 'Drawdown máximo']
        
        indicadores_estatisticas_gerais = [int(self.numero_trades), self.operacoes_vencedoras, self.operacoes_perdedoras, self.media_ganhos,
                                            self.media_perdas, self.expectativa_matematica, self.maior_sequencia_vitorias,
                                            self.maior_sequencia_derrotas, self.percentual_cart_supera_ibov]   
        

        nomes_estat_gerais = ["Número de carteiras", '% Operações vencedoras', '% Operações perdedoras', "Média de ganhos", "Média de perdas", 
                              "Expec. matemática por trade", "Maior sequência de vitória", "Maior sequência de derrotas", "% Meses carteira > IBOV"]


        self.pdf.set_font('Arial', '', 9)

        for i in range(0, 9):

            texto1 = indicadores_risco_retorno[i]
            texto2 = indicadores_estatisticas_gerais[i]

            if texto1 == self.sharpe:

                texto1 = str(round(texto1, 2))
            
            else:

                texto1 = str(round(texto1 * 100, 2)) + "%"

            if texto2 not in [self.numero_trades, self.maior_sequencia_derrotas, self.maior_sequencia_vitorias]:

                texto2 = str(round(texto2 * 100, 2)) + "%"

            else:

                texto2 = str(int(texto2))

            self.pdf.cell(8, 8, border = False, ln = False, align = "C")
            self.pdf.cell(45, 8, nomes_risco_retorno[i], border = True, ln = False, align = "C")
            self.pdf.cell(25, 8, texto1, border = True, ln = False, align = "C")
            self.pdf.cell(40, 8, ln = False)
            self.pdf.cell(45, 8, nomes_estat_gerais[i], border = True, ln = False, align = "C")
            self.pdf.cell(25, 8, texto2, border = True, ln = True, align = "C")

        # self.pdf.image('./nave1.png', x = 70, y = 225, w = 75, h = 33)

        self.pdf.cell(0, 40, ln = True)

    def eventos_estresse_e_dias_sem_lucro(self):

        self.pdf.set_font('Arial', 'B', 11)

        self.pdf.cell(90, 10, "Eventos de estresse", ln = False, align = "C")
        self.pdf.cell(10, 10, ln = False)
        self.pdf.cell(90, 10, "Períodos sem lucro", ln = True, align = "C")


        indicadores_estresse = [self.joesley_day, self.mar20, self.boasorteday, self.greve_caminhao,
                                     self.precatorios, self.crise_2008]
        
        nomes_estresse = ['Joesley Day - 18/05/2017', 'Auge pandemia: Março - 2020', 'Boa sorte Day - 10/11/2022',
                          'Greve dos caminhoneiros - 2018', 'Precatórios - ago/nov 2021', 'Crise de 2008']
        
        indicadores_sem_lucro = [self.retorno_21_min, self.retorno_63_min, self.retorno_126_min, self.retorno_252_min, 
                                 self.retorno_504_min, self.retorno_756_min]
        
        nome_indicadores_sem_lucro = ['Pior período de 1 mês', 'Pior período de 3 meses', 'Pior período de 6 meses', 'Pior período de 1 ano',
                                      'Pior período de 2 anos', 'Pior período de 3 anos']
        

        self.pdf.set_font('Arial', '', 9)

        for i in range(0, 6):

            texto1 = indicadores_estresse[i]
            texto2 = str(round(indicadores_sem_lucro[i] * 100, 2)) + "%"

            if texto1 != '-':

                texto1 = str(round(texto1 * 100, 2)) + "%"

            self.pdf.cell(4, 8, border = False, ln = False)
            self.pdf.cell(53, 8, nomes_estresse[i], border = True, ln = False, align = "C")
            self.pdf.cell(25, 8, texto1, border = True, ln = False, align = "C")
            self.pdf.cell(25, 8, border = False, ln = False)
            self.pdf.cell(53, 8, nome_indicadores_sem_lucro[i], border = True, ln = False, align = "C")
            self.pdf.cell(25, 8, texto2, border = True, ln = True, align = "C")

        # self.pdf.image('./nave2.png', x = 90, y = 105, w = 50, h = 50)
 
    def grafico_underwater(self):


        self.pdf.image("./grafico_underwater.png", w = 140, h = 90, x = 35, y = 160)

    def retorno_ano_a_ano_mes_a_mes(self):

        self.pdf.add_page()

        self.pdf.image("./grafico_ano.png", w = 175, h = 80, x = 20, y = 50)
        self.pdf.image("./grafico_mes.png", w = 175, h = 80, x = 20, y = 150)

    def grafico_janelas_moveis(self):

        self.pdf.add_page()

        self.pdf.image("./janela_movel_12M_retorno_movel.png", w = 80, h = 64, x = 15, y = 45)
        self.pdf.image("./janela_movel_12M_alfa.png", w = 80, h = 64, x = 110, y = 45)
        self.pdf.image("./janela_movel_24M_retorno_movel.png", w = 80, h = 64, x = 15, y = 115)
        self.pdf.image("./janela_movel_24M_alfa.png", w = 80, h = 64, x = 110, y = 115)
        self.pdf.image("./janela_movel_36M_retorno_movel.png", w = 80, h = 64, x = 15, y = 185)
        self.pdf.image("./janela_movel_36M_alfa.png", w = 80, h = 64, x = 110, y = 185)


pdf = PDF()

MakePDF()