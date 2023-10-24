import pandas as pd

#otimizar NO MÁXIMO 2 paramtros pro seu próprio bem. Se você quiser otimizar 10, 15, vai cometer overfitting
#Não colocar o intervalo entre os parâmetros muito pequenos. Coloca o step = 5 e tal. A média móvel de 20 pra 21 períodos é praticamente a mesma! 


'''
Erros comuns de otimização:

- Colocar o período INTEIRO pra otimizar! Não faça isso, você vai pegar contextos diferentes de mercado que não faz sentido e pior, não vai ter
uma regra clara de otimização
- Cada estágio da otimização deve representar um novo estado do mercado. Por isso fazemos essa janela móvel e a escolha da janela ideal
varia justamente o suficiente pro mercado ter mudado. Não pode separar em muitos períodos.
O padrão é o ratio de 3:1 -> 3 anos pra 1 ano de predição por exemplo
Entretanto, quanto maior o período que você tem, maior o "luxo" você pode se dar pro período de otimização pra 4:1 ou 5:1

'''

class Optimize():

    def __init__(self, estrategia, class_dados, parametro1 = None, parametro2 = ()):
        
        self.parametro1 = parametro1
        self.parametro2 = parametro2
        
        self.estrategia = estrategia

        estrategia.dados = class_dados.dados

    def run_optimize(self):

        self.df_retorno_acum = pd.DataFrame(columns=['parametro1', 'parametro2', 'retorno'])

        if self.parametro2 != ():

            z = 0

            for i in self.parametro1:
                for j in self.parametro2:

                    self.estrategia.parametro1 = i
                    self.estrategia.parametro2 = j
                    

                    self.estrategia.run_strategy()

                    retorno = ((self.estrategia.df_trades['retorno'] + 1).cumprod() - 1).iat[-1]

                    self.df_retorno_acum.loc[z, 'parametro1'] = i
                    self.df_retorno_acum.loc[z, 'parametro2'] = j
                    self.df_retorno_acum.loc[z, 'retorno'] = retorno

                    z = z + 1

        
        else:

            z = 0

            for i in self.parametro1:
                
                self.estrategia.parametro1 = i

                self.estrategia.run_strategy()

                retorno = ((self.estrategia.df_trades['retorno'] + 1).cumprod() - 1).iat[-1]

                self.df_retorno_acum.loc[z, 'parametro1'] = i
                self.df_retorno_acum.loc[z, 'parametro2'] = None
                self.df_retorno_acum.loc[z, 'retorno'] = retorno

                z = z + 1