from fpdf import FPDF
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

    def __init__(self, dd_all, dia_inicial, dia_final, dias_totais_backtest, 
            retorno_acum_modelo, retorno_acum_cdi, retorno_acum_ibov, turn_over_medio,
            retorno_aa_modelo, vol_ultimo_ano, sharpe, var_diario, 
            numero_trades, operacoes_vencedoras, operacoes_perdedoras, media_ganhos, media_perdas, 
            expectativa_matematica, percentual_cart_supera_ibov, maior_sequencia_vitorias, 
            maior_sequencia_derrotas, joesley_day, mar20, boasorteday, greve_caminhao, 
            crise_2008, precatorios, retorno_21_min, retorno_63_min, retorno_126_min, 
            retorno_252_min, retorno_504_min, retorno_756_min, nome_arquivo = "backtest.pdf"):
        
        load_dotenv()

        self.drawdown_maximo = dd_all
        self.turn_over_medio = turn_over_medio
        self.dia_inicial = dia_inicial
        self.dia_final = dia_final
        self.dias_totais_backtest = dias_totais_backtest
        self.retorno_acum_modelo = retorno_acum_modelo
        self.retorno_acum_cdi = retorno_acum_cdi
        self.retorno_acum_ibov = retorno_acum_ibov
        self.retorno_aa_modelo = retorno_aa_modelo
        self.vol_ultimo_ano = vol_ultimo_ano
        self.sharpe = sharpe
        self.var_diario = var_diario
        self.numero_trades = numero_trades
        self.operacoes_vencedoras = operacoes_vencedoras
        self.operacoes_perdedoras = operacoes_perdedoras
        self.media_ganhos = media_ganhos
        self.media_perdas = media_perdas
        self.expectativa_matematica = expectativa_matematica
        self.percentual_cart_supera_ibov = percentual_cart_supera_ibov
        self.maior_sequencia_vitorias = maior_sequencia_vitorias
        self.maior_sequencia_derrotas = maior_sequencia_derrotas
        self.joesley_day = joesley_day
        self.mar20 = mar20
        self.boasorteday = boasorteday
        self.greve_caminhao = greve_caminhao
        self.crise_2008 = crise_2008
        self.precatorios = precatorios
        self.retorno_21_min = retorno_21_min
        self.retorno_63_min = retorno_63_min
        self.retorno_126_min = retorno_126_min
        self.retorno_252_min = retorno_252_min
        self.retorno_504_min = retorno_504_min
        self.retorno_756_min = retorno_756_min 

        self.nome_arquivo = nome_arquivo
        
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

        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.databse_folder = os.getenv("IMAGES_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.databse_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

        self.pdf_intro()
        # self.tabela_dias()
        self.grafico_retorno_acum()
        self.tabelas_estatisticas_gerais()
        self.eventos_estresse_e_dias_sem_lucro()
        self.grafico_underwater()
        self.retorno_ano_a_ano_mes_a_mes()
        self.grafico_janelas_moveis()

        self.current_folder = os.getcwd()

        self.project_folder = os.getenv("PROJECT_FOLDER")
        self.desired_folder = os.getenv("INDICATORS_FOLDER")
        self.full_desired_path = os.path.join(self.project_folder,self.desired_folder)

        if(self.current_folder != self.full_desired_path):
            os.chdir(self.full_desired_path)

        #diretorio_atual = os.getcwd()
        #print("Diretório atual para output PDF:", diretorio_atual)

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

        x=14
        y=45
        w=185
        h=37

        dia_inicial_formatado = self.dia_inicial.strftime('%Y-%m-%d')
        dia_final_formatado = self.dia_final.strftime('%Y-%m-%d')
        
        text = f'''    Está presente nesse relatório diversas visões, gráficas e numéricas, para que você posso tirar suas próprias conclusões sobre a performance histórica dos indicadores escolhidos. Considere também o número de ativos e o período de rebalanceamento. 
    É importante notar que nunca devemos tirar conclusões a partir de somente um parâmetro, deve-ser avaliar o contexto.
    O relatório está considerando a data inicial de {dia_inicial_formatado} e data final de {dia_final_formatado} na qual somam {self.dias_totais_backtest} dias.
        '''
        self.pdf.rect(x, y, w, h)
        self.pdf.set_xy(x + 2, y + 2)  # Margem de 2 unidades para o texto dentro da célula
        self.pdf.multi_cell(w - 4, 8, text)

    def grafico_retorno_acum(self):

        self.pdf.image("./rent_acum.png", w = 140, h = 80, x = 35, y = 89)

        x=16
        y=175
        w=185
        h=65
        text = f'''    Acima o histórico de rentabilidades diárias comparadas entre o Modelo, uma referência da renda fixa - CDI e o IBOV. Para uma análise inicial, esse tipo de gráfico já dá um bom norte sobre a performance de operação do Modelo. Todos os outros parâmetros serão tirados da avaliação da composição histórica da carteira.
    Além de avaliar a performance de rentabilidade, deve-se também olhar para o conjunto de informações geradas a partir dos dados das tabelas apresentadas a seguir. Todo investimento deve ser visto fundamentalemnte por 3 pilares, a Rentabilidade, a Liquidez e a Segurança, dessa forma os dados apresentados a seguir estão ali para que, com a análise devida, lhe dê maior segurançã a respeito do modelo escolhido.
        '''
        self.pdf.rect(x, y, w, h)
        self.pdf.set_xy(x + 2, y + 2)  # Margem de 2 unidades para o texto dentro da célula
        self.pdf.multi_cell(w - 4, 8, text, border = False)

    def tabelas_estatisticas_gerais(self):
            
        self.pdf.add_page()

        x=16
        y=45
        w=185
        h=90
        text = f'''    Avaliar e ter ciências do contexto geral do modelo é essencial para entender a sua robustez. Alguns parâmetros importantes a se olhar são:
            1) 'Vol 252d': reprensenta a volatilidade do ativo no último ano, ou seja, o quanto aquele ativo oscilou de preço do último período de 252 dias úteis.
            2) 'Drawdown máximo': representa o máximo de perda percentual de patrimônio identificado no período de análise.
            3) 'Expec. matemática por trade': 
            4) 'Médias de perda & ganho': representa o valor percentual médio de quando se perde ou se ganha.
            5) 'Retorno a.a. modelo': mostra a rentabilidade anualizada do modelo no período de análise. Trabalha junto com o 'Retorno acum. modelo'.
        Todos os parâmetros mostrados tem algum valor específico em alguma análise, exemplificamos acima alguns que tem mais relevância geral.
        '''
        self.pdf.rect(x, y, w, h)
        self.pdf.set_xy(x + 2, y + 2)  # Margem de 2 unidades para o texto dentro da célula
        self.pdf.multi_cell(w - 4, 8, text, border = False)
        self.pdf.set_draw_color(255, 215, 0)

        self.pdf.set_font('Arial', 'B', 11)

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

    def eventos_estresse_e_dias_sem_lucro(self):

        self.pdf.add_page()

        x=16
        y=45
        w=185
        h=18
        text = f'''    Dentro do período de análise estão contidos e calculadas as oscilações negativas de eventos de estresse na Bolsa de Valores brasileira.
        '''
        self.pdf.rect(x, y, w, h)
        self.pdf.set_xy(x + 2, y + 2)  # Margem de 2 unidades para o texto dentro da célula
        self.pdf.multi_cell(w - 4, 8, text, border = False)
        self.pdf.set_draw_color(255, 215, 0)

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

        x=16
        y=135
        w=185
        h=28
        text = f'''    O grágico de Underderwater, também conhecido como gráfico do azarado, mostra a variação negativa desde a última máxima histórica dentro do período de análise. É possível verificar picos de queda ('Drawdown máximo') e momento da carteira de forma geral. 
        '''
        self.pdf.rect(x, y, w, h)
        self.pdf.set_xy(x + 2, y + 2)  # Margem de 2 unidades para o texto dentro da célula
        self.pdf.multi_cell(w - 4, 8, text, border = False)
        self.pdf.set_draw_color(255, 215, 0)
        self.pdf.image("./grafico_underwater.png", w = 140, h = 90, x = 35, y = 170)

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
