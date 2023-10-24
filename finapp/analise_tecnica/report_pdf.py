from fpdf import FPDF


class PDF(FPDF):

    
    def header(self):
     
        self.image('./logo.png', 10, 8, 40)
        self.set_font('Arial', 'B', 20)
        self.ln(15)
        self.set_draw_color(35, 155, 132) #cor RGB
        self.cell(0, 15, f"Relatório do Modelo", 
                  border = True, ln = True, align = "C")
        self.ln(5)
        
    def footer(self):
        
        self.set_y(-15) #espaço ate o final da folha
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f"{self.page_no()}/{{nb}}", align = "C")


class MakePDF():

    def __init__(self, drawdown_maximo, dia_inicial, dia_final, dias_totais_backtest, 
                 retorno_acum_modelo, retorno_acum_acao, retorno_acum_cdi, retorno_acum_ibov, 
                 retorno_aa_modelo, vol_ultimo_ano, sharpe, var_diario, 
                 numero_trades, operacoes_vencedoras, operacoes_perdedoras, media_ganhos, 
                 media_perdas, expectativa_matematica, media_tempo_operacao, maior_sequencia_vitorias, 
                 maior_sequencia_derrotas, joesley_day, mar20, boasorteday, greve_caminhao, crise_2008, precatorios, df_otimizacao = None,
                 otimizacao = False, nome_arquivo = "backtest.pdf", caminho_imagens = None):
            
        self.otimizacao = otimizacao    
        self.df_otimizacao = df_otimizacao
        self.drawdown_maximo = drawdown_maximo
        self.dia_inicial = dia_inicial
        self.dia_final = dia_final
        self.dias_totais_backtest = dias_totais_backtest
        self.retorno_acum_modelo = retorno_acum_modelo
        self.retorno_acum_acao = retorno_acum_acao
        self.retorno_acum_cdi = retorno_acum_cdi
        self.retorno_acum_ibov = retorno_acum_ibov
        self.retorno_aa_modelo = retorno_aa_modelo
        self.vol_ultimo_ano = vol_ultimo_ano
        self.sharpe = sharpe
        self.var_diario = var_diario
        self.drawdown_maximo = drawdown_maximo
        self.numero_trades = numero_trades
        self.operacoes_vencedoras = operacoes_vencedoras
        self.operacoes_perdedoras = operacoes_perdedoras
        self.media_ganhos = media_ganhos
        self.media_perdas = media_perdas
        self.expectativa_matematica = expectativa_matematica
        self.media_tempo_operacao = media_tempo_operacao
        self.maior_sequencia_vitorias = maior_sequencia_vitorias
        self.maior_sequencia_derrotas = maior_sequencia_derrotas
        self.joesley_day = joesley_day
        self.mar20 = mar20
        self.boasorteday = boasorteday
        self.greve_caminhao = greve_caminhao
        self.crise_2008 = crise_2008
        self.precatorios = precatorios

        self.nome_arquivo = nome_arquivo
        self.caminho_imagens = caminho_imagens
        
        self.pdf = PDF("P", "mm", "Letter")
        self.pdf.set_auto_page_break(auto = True, margin = 15)
        self.pdf.alias_nb_pages()
        self.pdf.add_page()
        self.pdf.set_fill_color(255, 255, 255)
        self.pdf.set_draw_color(35, 155, 132)

        self.tabela_dias()
        self.grafico_retorno_acum()
        self.tabelas_estatisticas_gerais()
        self.grafico_preco_indicadores()
        self.eventos_estresse()
        self.grafico_underwater()
        self.retorno_ano_a_ano_mes_a_mes()

        if self.otimizacao:

            self.tabela_in_sample_out_sample()
            self.grafico_parametros()

        self.pdf.output(f"{self.nome_arquivo}")

    def tabela_dias(self):

        self.pdf.set_font('Arial', '', 8)
        self.pdf.cell(20, 7, "Dia inicial", ln = False,  border = True, fill = True, align = "C")
        self.pdf.cell(20, 7, f" {self.dia_inicial.date()}", ln = True, 
                border = True, fill = False, align = "C")

        self.pdf.cell(20, 7, "Dia final", ln = False,  border = True, fill = True, align = "C")
        self.pdf.cell(20, 7, f" {self.dia_final.date()}", ln = True, 
                border = True, fill = False, align = "C")
        
        self.pdf.cell(20, 7, "Dias totais", ln = False,  border = True, fill = True, align = "C")
        self.pdf.cell(20, 7, f" {self.dias_totais_backtest}", ln = True, 
                border = True, fill = False, align = "C")

        self.pdf.ln(7)


    def grafico_retorno_acum(self):

        self.pdf.image("./rent_acum.png", w = 140, h = 80, x = 55, y = 44.9)

    def tabelas_estatisticas_gerais(self):
            
        self.pdf.cell(0, 60, ln = True)

        self.pdf.set_font('Arial', 'B', 11)

        self.pdf.cell(8, 10, ln = False)

        self.pdf.cell(70, 10, "Estatísticas de Retorno e Risco", ln = False, align = "C")

        self.pdf.cell(40, 10, ln = False)

        self.pdf.cell(70, 10, "Estatísticas de Trade", ln = True, align = "C")

        indicadores_risco_retorno = [self.retorno_acum_modelo, self.retorno_acum_acao, self.retorno_acum_cdi, self.retorno_acum_ibov,
                                     self.retorno_aa_modelo, self.vol_ultimo_ano, self.sharpe, self.var_diario, self.drawdown_maximo]
        
        nomes_risco_retorno = ["Retorno acum. modelo", "Retorno acum. ativo", "Retorno acum. CDI", "Retorno acum. IBOV", "Retorno a.a. modelo",
                               "Vol 252d", "Índice Sharpe", 'VAR diário 95%', 'Drawdown máximo']
        
        indicadores_estatisticas_gerais = [int(self.numero_trades), self.operacoes_vencedoras, self.operacoes_perdedoras, self.media_ganhos,
                                            self.media_perdas, self.expectativa_matematica, self.media_tempo_operacao, self.maior_sequencia_vitorias,
                                            self.maior_sequencia_derrotas]   
        

        nomes_estat_gerais = ["Número de trades", '% Operações vencedoras', '% Operações perdedoras', "Média de ganhos", "Média de perdas", 
                              "Expec. matemática por trade", "Tempo médio de operação", "Maior sequência de vitória", "Maior sequência de derrotas"]


        self.pdf.set_font('Arial', '', 9)

        for i in range(0, 9):

            texto1 = indicadores_risco_retorno[i]
            texto2 = indicadores_estatisticas_gerais[i]

            if texto1 == self.sharpe:

                texto1 = str(round(texto1, 2))
            
            else:

                texto1 = str(round(texto1 * 100, 2)) + "%"

            if texto2 not in [self.numero_trades, self.maior_sequencia_derrotas, self.maior_sequencia_vitorias, self.media_tempo_operacao]:

                texto2 = str(round(texto2 * 100, 2)) + "%"

            else:

                texto2 = str(int(texto2))

            self.pdf.cell(8, 8, border = False, ln = False, align = "C")
            self.pdf.cell(45, 8, nomes_risco_retorno[i], border = True, ln = False, align = "C")
            self.pdf.cell(25, 8, texto1, border = True, ln = False, align = "C")
            self.pdf.cell(40, 8, ln = False)
            self.pdf.cell(45, 8, nomes_estat_gerais[i], border = True, ln = False, align = "C")
            self.pdf.cell(25, 8, texto2, border = True, ln = True, align = "C")

        self.pdf.image('./nave1.png', x = 70, y = 225, w = 75, h = 33)

        self.pdf.cell(0, 90, ln = True)


    def grafico_preco_indicadores(self):


        self.pdf.image("./grafico_sinais.png", w = 175, h = 80, x = 20, y = 50)

        
    def eventos_estresse(self):

        self.pdf.set_font('Arial', 'B', 11)

        self.pdf.cell(78, 10, "Eventos de estresse", ln = True, align = "C")

        indicadores_estresse = [self.joesley_day, self.mar20, self.boasorteday, self.greve_caminhao,
                                     self.precatorios, self.crise_2008]
        
        nomes_estresse = ['Joesley Day - 18/05/2017', 'Auge pandemia: Março - 2020', 'Boa sorte Day - 10/11/2022',
                          'Greve dos caminhoneiros - 2018', 'Precatórios - ago/nov 2021', 'Crise de 2008']
        

        self.pdf.set_font('Arial', '', 9)

        for i in range(0, 6):

            texto1 = indicadores_estresse[i]

            if texto1 != '-':

                texto1 = str(round(texto1 * 100, 2)) + "%"

            self.pdf.cell(53, 8, nomes_estresse[i], border = True, ln = False, align = "C")
            self.pdf.cell(25, 8, texto1, border = True, ln = True, align = "C")

        self.pdf.image('./nave2.png', x = 130, y = 140, w = 50, h = 50)

    
    def grafico_underwater(self):


        self.pdf.image("./grafico_underwater.png", w = 140, h = 60, x = 35, y = 200)

    def retorno_ano_a_ano_mes_a_mes(self):


        self.pdf.cell(0, 297, border=False, ln = True)

        self.pdf.image("./grafico_ano.png", w = 175, h = 80, x = 20, y = 50)
        self.pdf.image("./grafico_mes.png", w = 175, h = 80, x = 20, y = 150)

    
    def tabela_in_sample_out_sample(self):

        self.pdf.set_font('Arial', 'B', 11)

        self.pdf.cell(0, 12, "Tabela resultados otimização", border = False, ln = True, align = "C")

        self.pdf.set_font('Arial', '', 8)

        for i in range(0, len(self.df_otimizacao) + 1):

            self.pdf.cell(2, 10, border = False, ln = False, align = "C")

            if i == 0:
            
                self.pdf.cell(24, 10, "Data inicial IS", border = True, ln = False, align = "C")
                self.pdf.cell(24, 10, "Data final IS", border = True, ln = False, align = "C")
                self.pdf.cell(24, 10, "Retorno IS a.m.", border = True, ln = False, align = "C")
                self.pdf.cell(24, 10, "Data inicial OOS", border = True, ln = False, align = "C")
                self.pdf.cell(24, 10, "Data final OOS", border = True, ln = False, align = "C")
                self.pdf.cell(24, 10, "Retorno OOS a.m.", border = True, ln = False, align = "C")
                self.pdf.cell(24, 10, "Parâmetro 1", border = True, ln = False, align = "C")
                self.pdf.cell(24, 10, "Parâmetro 2", border = True, ln = True, align = "C")

            else:

                self.pdf.cell(24, 10, f"{self.df_otimizacao.iloc[(i - 1), 0]}", border = True, ln = False, align = "C")
                self.pdf.cell(24, 10, f"{self.df_otimizacao.iloc[(i - 1), 1]}", border = True, ln = False, align = "C")
                self.pdf.cell(24, 10, f"{round((self.df_otimizacao.iloc[(i - 1), 2])*100, 2)}%", border = True, ln = False, align = "C")
                self.pdf.cell(24, 10, f"{self.df_otimizacao.iloc[(i - 1), 3]}", border = True, ln = False, align = "C")
                self.pdf.cell(24, 10, f"{self.df_otimizacao.iloc[(i - 1), 4]}", border = True, ln = False, align = "C")
                self.pdf.cell(24, 10, f"{round((self.df_otimizacao.iloc[(i - 1), 5])*100, 2)}%", border = True, ln = False, align = "C")
                self.pdf.cell(24, 10, f"{self.df_otimizacao.iloc[(i - 1), 6]}", border = True, ln = False, align = "C")
                self.pdf.cell(24, 10, f"{self.df_otimizacao.iloc[(i - 1), 7]}", border = True, ln = True, align = "C")
            
        self.pdf.cell(0, 12, border = False, ln = True, align = "C")

        self.pdf.set_font('Arial', 'B', 11)

        self.pdf.cell(40, 10, "Retono médio IS", border = True, ln = False, align = "C")
        self.pdf.cell(40, 10, "Retorno médio OOS", border = True, ln = True, align = "C")

        media_mensal_is = self.df_otimizacao['retorno_IS_am'].mean()
        media_mensal_oos = self.df_otimizacao['retorno_OOS_am'].mean()

        self.pdf.cell(40, 10, f"{round(media_mensal_is*100, 2)}%", border = True, ln = False, align = "C")
        self.pdf.cell(40, 10, f"{round(media_mensal_oos*100, 2)}%", border = True, ln = False, align = "C")


    def grafico_parametros(self):

        self.pdf.add_page()

        for i in range(0, (len(self.df_otimizacao))):

            if i % 2 == 0:

                self.pdf.image(f"./retorno_por_parametro_{i}.png", w = 175, h = 80, x = 20, y = 50)

            else:
                
                self.pdf.image(f"./retorno_por_parametro_{i}.png", w = 175, h = 80, x = 20, y = 150)
                
                if i != max(range(0, (len(self.df_otimizacao)))):
                    self.pdf.add_page()


        
        



        















