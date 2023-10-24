
class MakeIndicator():

    def __init__(self):

        pass

    def media_movel_simples(self, coluna_preco, periodo):

        sma = coluna_preco.rolling(periodo).mean().dropna()

        return sma
    
    def media_movel_exponencial(self, coluna_preco, periodo):

        ewa = coluna_preco.ewm(span=periodo, min_periods=periodo).mean().dropna()
        
        return ewa

    def RSI(self, coluna_preco, periodo):

        ### Fórmula RSI:

        #100 - 100/(1 + mediaRetornosPositivos / mediaRetornosNegativos) 

        retornos = coluna_preco.pct_change().dropna()

        retornos_positivos = retornos.apply(lambda x: x if x > 0 else 0)
        retornos_negativos = retornos.apply(lambda x: abs(x) if x < 0 else 0)

        media_retornos_positivos = retornos_positivos.rolling(window = periodo).mean().dropna()
        media_retornos_negativos = retornos_negativos.rolling(window = periodo).mean().dropna()
        
        rsi = 100 - 100/(1 + media_retornos_positivos/media_retornos_negativos) 

        return rsi
    
    def bollinger_bands(self, coluna_preco, periodo_media, numero_desvios):

        sma = coluna_preco.rolling(periodo_media).mean().dropna()

        desvio_padrao =coluna_preco.rolling(periodo_media).std().dropna()

        borda_superior = sma + (desvio_padrao * numero_desvios)
        borda_inferior = sma - (desvio_padrao * numero_desvios)

        return sma, borda_superior, borda_inferior
    
    def quebra_resistencia_maximo(self, coluna_preco, periodo):

        valor_maximo = coluna_preco.rolling(periodo).max().dropna()

        return valor_maximo
    
    def quebra_resistencia_minimo(self, coluna_preco, periodo):

        valor_minimo = coluna_preco.rolling(periodo).min().dropna()

        return valor_minimo
