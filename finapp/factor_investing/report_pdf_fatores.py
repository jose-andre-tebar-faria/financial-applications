from fpdf import FPDF

class PDF(FPDF):

    def header(self):
     
        self.image('logo.png', 10, 8, 40)
        self.set_font('Arial', 'B', 20)
        self.ln(15)
        self.set_draw_color(35, 155, 132) #cor RGB
        self.cell(0, 15, f"Relatório dos Fatores", 
                  border = True, ln = True, align = "C")
        self.ln(5)
        
    def footer(self):
        
        self.set_y(-15) #espaço ate o final da folha
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f"{self.page_no()}/{{nb}}", align = "C")


class MakePDF():

    def __init__(self, fatores, liquidez, matriz_correl,
                 nome_arquivo = "premios_de_risco.pdf", caminho_imagens = None):
            
        self.lista_nome_fatores = fatores
        self.liquidez = liquidez
        self.matriz_correl = matriz_correl
        
        self.nome_arquivo = nome_arquivo
        self.caminho_imagens = caminho_imagens
        
        self.pdf = PDF("P", "mm", "Letter")
        self.pdf.alias_nb_pages()
        self.pdf.add_page()
        self.pdf.set_fill_color(255, 255, 255)
        self.pdf.set_draw_color(35, 155, 132)

        self.primeira_pagina()
        self.segunda_pagina()

        for i, fator in enumerate(self.lista_nome_fatores):
        
            self.pagina_fator(nome_fator= fator, liquidez= self.liquidez[i])

        self.pdf.output(f"{self.nome_arquivo}")

    def primeira_pagina(self):

        self.pdf.image(f"{self.caminho_imagens}/comparando_1Q.png", w = 180, h = 90, x = 13, y = 60)
        self.pdf.image(f"{self.caminho_imagens}/comparando_premios.png", w = 180, h = 90, x = 13, y = 160)

    def segunda_pagina(self):

        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 9)
        self.pdf.cell(0, 15, 'Matriz de correlação', ln = True, align = 'C')
        self.pdf.cell(0, 5, ln = True)

        tamanho_tabela = len(self.matriz_correl)

        if tamanho_tabela > 20:

            print("Não é possível ter mais de 20 fatores no relatório!")
            exit()
        

        for linha in range(0, tamanho_tabela + 1):
            for coluna in range(0, tamanho_tabela + 1):

                if linha == 0:

                    self.pdf.set_font('Arial', 'B', 9)

                    if coluna == 0:

                        self.pdf.cell(195/(tamanho_tabela + 1), 6, align = 'C', border= False)

                    elif coluna == (tamanho_tabela):

                        self.pdf.cell(195/(tamanho_tabela + 1), 6, str(coluna), ln = True, align = 'C', border= True)

                    else:

                        self.pdf.cell(195/(tamanho_tabela + 1), 6, str(coluna), align = 'C', border= True)

                else:

                    if coluna == 0:

                        self.pdf.set_font('Arial', 'B', 9)

                        self.pdf.cell(195/(tamanho_tabela + 1), 6, str(linha), align = 'C', border= True)

                    elif coluna == (tamanho_tabela):

                        self.pdf.set_font('Arial', '', 9)

                        try:

                            self.pdf.cell(195/(tamanho_tabela + 1), 6, str(round(self.matriz_correl.iloc[linha - 1, coluna - 1], 2)), ln = True, 
                                      align = 'C', border= True)
                        except:

                            self.pdf.cell(195/(tamanho_tabela + 1), 6, 'teste', ln = True, 
                                      align = 'C', border= True)

                    else:

                        self.pdf.set_font('Arial', '', 9)

                        try:

                            self.pdf.cell(195/(tamanho_tabela + 1), 6, str(round(self.matriz_correl.iloc[linha - 1, coluna - 1], 2)), align = 'C', 
                                      border= True)
                        
                        except:

                            self.pdf.cell(195/(tamanho_tabela + 1), 6, 'teste', 
                                      align = 'C', border= True)


        self.pdf.set_font('Arial', 'B', 9)
        
        self.pdf.cell(0, 10, 'Legenda', ln = True)

        
        for i in range(1, (tamanho_tabela + 1)):
            
            if i % 3 == 0:

                self.pdf.set_font('Arial', 'B', 9)
                self.pdf.cell(8, 8, str(i), align = 'C', border= True)
                self.pdf.set_font('Arial', '', 7)

                try:

                    self.pdf.cell(53, 8, self.matriz_correl.columns[i - 1], ln = True, align = 'C', border= True)

                except:

                    self.pdf.cell(53, 8, 'teste', ln = True, align = 'C', border= True)

            else:
                self.pdf.set_font('Arial', 'B', 9)
                self.pdf.cell(8, 8, str(i), align = 'C', border= True)
                self.pdf.set_font('Arial', '', 7)
                
                try:

                    self.pdf.cell(53, 8, self.matriz_correl.columns[i - 1], align = 'C', border= True)
                
                except:

                    self.pdf.cell(53, 8, 'teste', align = 'C', border= True)


                self.pdf.cell(5, 8)


    def pagina_fator(self, nome_fator, liquidez):

        self.pdf.add_page()
        self.pdf.image(f"{self.caminho_imagens}/barras_quartis_{nome_fator}_{liquidez}.png", w = 95, h = 80, x = 10, y = 60)
        self.pdf.image(f"{self.caminho_imagens}/linha_quartis_{nome_fator}_{liquidez}.png", w = 95, h = 80, x = 110, y = 60)
        self.pdf.image(f"{self.caminho_imagens}/movel_12m_premio_de_risco_{nome_fator}_{liquidez}.png", w = 95, h = 80, x = 10, y = 160)
        self.pdf.image(f"{self.caminho_imagens}/premio_de_risco_{nome_fator}_{liquidez}.png", w = 95, h = 80, x = 110, y = 160)