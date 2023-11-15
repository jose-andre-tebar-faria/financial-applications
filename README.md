<h1 align="center">
    <img src=".\files\colored_eye.svg" width="155" />
    <p>🙇🏽‍♂️ financial-applications 🙇🏽 </p>
</h1>

## 🚨 ABOUT

### This **Project** have a lot of python code for download and analisys of stock market.

## ⚓ seven_mean_factor_investing

This folder contains a static code that have a end-to-end work flow. The code itself can download all needed data for applying the 7 mean model using a factor investing methodology with backtest.

Basically this code are creating a dataframe that contains in the lines - last business day of each month - the mean of the profitability of last 7 months, considering only price! after that, for each month, the program rank all the companies and choose the first 8 (TOP8) to be in our wallet. Each month the program calibrate the TOP8 stocks to compose our wallet! In the end are create a .png image to show the mapheat with profitability.

#### **CODE FLOW**:
    1) read total and monthly ibov indices compose
    2) download all needed data throught yahoo_finance

    ### MODELING
    3) calculate monthly returns in percentage
    4) 🚩transform montlhy_returns dataframe to monthly last seven mean return in percentage droping missing data
    5) rank companies monthly
    6) create montlhy_wallet

    ### BACK TESTING
    7) create monthly returns dataframe
    8) create returns heatmap plot for sns
    9) create acum returns heatmap plot for sns
    10) create ibov acum returns heatmap plot for sns 
    11) compare model & ibov monthly returns
    12) create compare ibov returns heatmap plot for sns
    13) configure heatmaps

Below a example of how a code will be presented here.

```bash
#example of bash
print('Hello World!')
```
#

#
<h1 align="center">
    <img src=".\files\gear.svg" width="155" />
    <p>FINAPP</p>
</h1>

## 🚨 ABOUT

### This **Project** intends to create an application that can optimize a stock wallet for long-term investments. Where are using here ywo types of analisys, first a Factor Investing modeling considering a 5 Factor Model by Eugene Fama & Kenneth French, and then a technical analisys.

# 🧭 Factor Investing

O modelo de 5 fatores, desenvolvido por Eugene Fama e Kenneth French, é uma extensão do modelo de três fatores original (CAPM) que visa explicar os retornos de ações com base em cinco fatores diferentes. Esses cinco fatores são:

- **Retorno do Mercado (Market Risk Premium)**: Este fator representa o retorno do mercado como um todo e é frequentemente capturado pelo retorno de um índice de mercado amplo, como o S&P 500. Ele mede o prêmio de risco associado a investir em ações em vez de um ativo livre de risco.

- **Capitalização de Mercado (Market Capitalization)**: Esse fator captura o prêmio associado a investir em ações de diferentes tamanhos de capitalização. As ações de pequena capitalização tendem a ter retornos diferentes das ações de grande capitalização. Portanto, esse fator leva em consideração as ações com base em sua capitalização de mercado.

- **Valor (Value)**: O fator de valor mede o prêmio de risco associado a investir em ações com baixas relações preço/lucro (P/L), baixas relações preço/valor contábil (P/VC) e outras métricas de valor. Em termos simples, ele procura identificar ações que estão subvalorizadas em relação aos seus fundamentos.

- **Momentum (Momentum)**: Este fator reflete a tendência recente dos preços das ações. Ações que tiveram um forte desempenho no passado tendem a continuar a ter um desempenho forte no curto prazo, enquanto ações que tiveram um desempenho fraco tendem a continuar com desempenho fraco.

- **Qualidade (Quality)**: O fator de qualidade considera métricas de qualidade financeira das empresas, como a estabilidade dos lucros, a força do balanço e a eficiência operacional. Ações de empresas com alta qualidade financeira tendem a ter um desempenho melhor.

Esses cinco fatores são usados para analisar os retornos das ações e entender melhor as fontes de risco e retorno no mercado de ações. O modelo de 5 fatores é uma extensão significativa em relação ao modelo de três fatores original (CAPM), que considerava apenas o mercado, o tamanho e o valor. A incorporação de fatores como momentum e qualidade torna o modelo mais robusto na explicação dos retornos das ações e é frequentemente usado no contexto de factor investing para criar estratégias de investimento baseadas em fatores específicos.

## 🪒 Equation
<h1 align="center">
    <img src=".\files\fama-french-5-factor-model-equation.png" width="1550" />
</h1>

## ⚒ Indicators

Para cada fator aprensentado acima deve-se modelar o indicador que descreve aquele determinado perfil. Abaixo os indicadores usados nesse estudo:

- **Retorno do Mercado (Market Risk Premium)**
    - **Retorno do índice de mercado**: Normalmente, o retorno do índice de mercado amplo, como o S&P 500, é usado como indicador-chave deste fator.

- **Capitalização de Mercado (Market Capitalization)**

    - **Capitalização de mercado**: A capitalização de mercado da empresa é o valor total de mercado de suas ações em circulação. As ações são geralmente divididas em categorias de grande capitalização, média capitalização e pequena capitalização.

- **Valor (Value)**

    - **Relação preço/lucro (P/L)**: O P/L é a relação entre o preço atual da ação e o lucro por ação. Ações com P/L baixo são consideradas de valor.
    - **Relação preço/valor contábil (P/VC)**: O P/VC compara o preço da ação com o valor contábil por ação da empresa. Um P/VC baixo é indicativo de valor.

- **Momentum (Momentum)**

    - **Retorno passado**: Esse fator leva em consideração o desempenho recente das ações. Os retornos passados, frequentemente mensais, são usados para avaliar o momentum.

- **Qualidade (Quality)**

    - **Margem de lucro**: A margem de lucro reflete a rentabilidade da empresa, medida como a relação entre o lucro líquido e a receita total.
    - **Endividamento**: O nível de dívida da empresa, muitas vezes medido pela relação entre dívida e patrimônio líquido ou pela relação entre dívida e EBITDA.
    - **Eficiência operacional**: Isso pode ser avaliado por métricas como o retorno sobre o patrimônio líquido (ROE) e o retorno sobre o ativo (ROA).

## 🗺 [Entidades](https://github.com/jose-andre-tebar-faria/financial-applications/tree/master/finapp/files)

O banco de dados usado nessas aplicações estão contidos em arquivos *.parquet* e serão discriminados a seguir.

    - cotacoes.parquet: cada linha representa a lista preços - incluindo preços ajustados - e quantidades negociadas de cada dia de cada ação.

        ['preco_abertura', 'preco_abertura_ajustado', 
        'preco_fechamento', 'preco_fechamento_ajustado', 
        'preco_maximo', 'preco_maximo_ajustado', 
        'preco_medio', 'preco_medio_ajustado', 
        'preco_minimo', 'preco_minimo_ajustado',
        'quantidade_negociada',
        'quantidade_negocios']

        data            preco_abertura  preco_fechamento  preco_maximo  preco_medio ...
    0   2010-01-04      11.50           11.50             11.50         11.50       ...
    1   2010-01-04      38.89           40.12             40.49         39.96       ...

    - ibov.parquet: cada linha representa o número de pontos do ibovespa por dia.
        data        fechamento
    0   2000-01-03  16930.42
    1   2000-01-04  15851.00

    - cdi.parquet: representa em cada linha a porcentagem de retorno da renda fixa no Brasil.
        data        retorno
    0   2000-01-03  0.000683
    1   2000-01-04  0.000682

    - market_premium.parquet: cada linha representa a proporção entre os retornos do mercado (ibov) e a renda fixa (cdi) por mês - último dia.
        data        mkt_premium
    0   2000-02-29  -0.464910
    1   2000-03-31  -0.331790

Todo arquivo contendo um indicador deve seguir minimamente o seguinte padrão de dados indicado abaixo.

    ['data', 'ticker', 'valor'] 

- **data**: *reprensenta uma data no formato YYYY-MM-DD.*
- **ticker**: *representa o código de negociação da ação no formato 4 letras 1 número (ex: PETR3).*
- **valor**: *número inteiro reprensentando o tamanho daquele indicador naquele dia praquela ação.*

Cada .parquet contido no database se refere ao seguinte indicador.
    
    *
    **
    *** DEMONSTRATIVOS ***
    **
    *
.

    - Ebit.parquet:
        ticker cnpj                 item                data        valor
    0   WEGE3  84.429.695/0001-11   Ebit                2023-10-29  1.581169e+09
    1   WEGE3  84.429.695/0001-11   Ebit                2023-10-30  1.581169e+09
.

    - Ebit_12m.parquet:
        ticker cnpj                 item                data        valor
    0   WEGE3  84.429.695/0001-11   Ebit12m             2023-10-29  6.206246e+09
    1   WEGE3  84.429.695/0001-11   Ebit12m             2023-10-30  6.206246e+09
.

    - DividaBruta.parquet:
        ticker cnpj                 item                data        valor
    0   WEGE3  84.429.695/0001-11   DividaBruta         2023-10-29  2.848572e+09
    1   WEGE3  84.429.695/0001-11   DividaBruta         2023-10-30  2.848572e+09
.

    - DividaLiquida.parquet:
        ticker cnpj                 item                data        valor
    0   WEGE3  84.429.695/0001-11   DividaLiquida       2023-10-29  -2.874738e+09
    1   WEGE3  84.429.695/0001-11   DividaLiquida       2023-10-30  -2.874738e+09
.

    - LucroLiquido12m.parquet:
        ticker cnpj                 item                data        valor
    0   WEGE3  84.429.695/0001-11   LucroLiquido12m     2023-10-29  5.298686e+09
    1   WEGE3  84.429.695/0001-11   LucroLiquido12m     2023-10-30  5.298686e+09
.

    - PatrimonioLiquido.parquet:
        ticker cnpj                 item                data        valor
    0   WEGE3  84.429.695/0001-11   PatrimonioLiquido   2023-10-29  1.659979e+10
    1   WEGE3  84.429.695/0001-11   PatrimonioLiquido   2023-10-30  1.659979e+10
.

    - ReceitaLiquida12m.parquet:
        ticker cnpj                 item                data        valor
    0   WEGE3  84.429.695/0001-11   ReceitaLiquida12m   2023-10-29  3.192195e+10
    1   WEGE3  84.429.695/0001-11   ReceitaLiquida12m   2023-10-30  3.192195e+10
.

    - Impostos.parquet:
        ticker cnpj                 item                data        valor
    0   WEGE3  84.429.695/0001-11   Impostos            2023-10-29 -268697000.0
    1   WEGE3  84.429.695/0001-11   Impostos            2023-10-30 -268697000.0
.

    - Impostos12m.parquet:
        ticker cnpj                 item                data        valor
    0   WEGE3  84.429.695/0001-11   Impostos12m         2023-10-29  -1.041531e+09
    1   WEGE3  84.429.695/0001-11   Impostos12m         2023-10-30  -1.041531e+09
.

    - AcoesEmCirculacao.parquet:
        ticker cnpj                 item                data        valor
    0   WEGE3  84.429.695/0001-11   AcoesEmCirculacao   2023-10-29  4.195234e+09
    1   WEGE3  84.429.695/0001-11   AcoesEmCirculacao   2023-10-30  4.195234e+09
.

    - TotalAcoes.parquet:
        ticker cnpj                 item                data        valor
    0   WEGE3  84.429.695/0001-11   TotalAcoes          2023-10-29  4.197318e+09
    1   WEGE3  84.429.695/0001-11   TotalAcoes          2023-10-30  4.197318e+09
.

    LucroLiquido.parquet
    ReceitaLiquida.parquet
    Disponibilidades.parquet
    LucroLiquidoSociosControladora.parquet
    LucroLiquidoSociosControladora12m.parquet
.

    *
    **
    *** INDICADORES ***
    **
    *
.

    - EV.parquet: O EV (Enterprise Value ou Valor da Firma), indica quanto custaria para comprar todos os ativos da companhia, descontando o caixa. 

        ticker cnpj                 indicador       data        valor
    0   WEGE3  84.429.695/0001-11   EV              2023-10-29  1.298864e+11
    1   WEGE3  84.429.695/0001-11   EV              2023-10-30  1.298864e+11
.

    - EBIT_EV.parquet: Este indicador mostra quanto tempo levaria para o valor calculado no EBIT pagar o investimento feito para compra-la.

    fórmula = (EV / Ebit)

        ticker cnpj                 indicador       data        valor
    0   WEGE3  84.429.695/0001-11   EBIT_EV         2023-10-29  0.04778
    1   WEGE3  84.429.695/0001-11   EBIT_EV         2023-10-30  0.04778
.

    - P_L.parquet: Dá uma ideia do quanto o mercado está disposto a pagar pelos lucros da empresa.

    fórmula: (Preço atual / Lucro por ação [LPA])

        ticker cnpj                 indicador       data        valor
    0   WEGE3  84.429.695/0001-11   P_L             2023-10-29  25.62993
    1   WEGE3  84.429.695/0001-11   P_L             2023-10-30  25.62993
.
 
    - L_P.parquet: P_L invertido para ajudar nos cálculos. Esse é o indicador usado pela aplicação.
    
        ticker cnpj                 indicador       data        valor
    0   WEGE3  84.429.695/0001-11   L_P             2023-10-29  0.03902
    1   WEGE3  84.429.695/0001-11   L_P             2023-10-30  0.03902
.

    - ROE.parquet: Mede a capacidade de agregar valor de uma empresa a partir de seus próprios recursos e do dinheiro de investidores. valor em porcentagem ?

    fórmula = (Lucro líquido / Patrimônio líquido)

        ticker cnpj                 indicador       data        valor
    0   WEGE3  84.429.695/0001-11   ROE             2023-10-29  0.31920
    1   WEGE3  84.429.695/0001-11   ROE             2023-10-30  0.31920
.

    - ROIC.parquet: Mede a rentabilidade de dinheiro o que uma empresa é capaz de gerar em razão de todo o capital investido, incluindo os aportes por meio de dívidas. em porcentagem ?

    fórmula = (Ebit - Impostos) / (Patrimônio líquido + Endividamento)

        ticker cnpj                 item            data        valor
    0   WEGE3  84.429.695/0001-11   ROIC            2023-10-29  0.26556
    1   WEGE3  84.429.695/0001-11   ROIC            2023-10-30  0.26556
.

    - LPA.parquet: Lucro por Ação.

    fórmula: (LucroLiquido / TotalAcoes)

        ticker cnpj                 item            data        valor
    0   WEGE3  84.429.695/0001-11   LPA             2023-10-29  1.23410
    1   WEGE3  84.429.695/0001-11   LPA             2023-10-30  1.23410
.

    - ValorDeMercado.parquet: Usado para se referir ao preço que o mercado está pagando por uma empresa.

    fórmula: (TotalAcoes * PreçoAtual)

        ticker cnpj                 item            data        valor
    0   WEGE3  84.429.695/0001-11   ValorDeMercado  2023-10-29  1.327612e+11
    1   WEGE3  84.429.695/0001-11   ValorDeMercado  2023-10-30  1.327612e+11
.

    *
    **
    *** INDICADORES CALCULADOS ***
    **
    *
.

    - momento_X_meses.parquet: cada linha representa a média móvel dos últimos X meses dos retornos para cada ação. ex = 1 mês

        data        ticker      valor
    0   2023-10-26  WEGE3       -0.096042
    1   2023-10-27  WEGE3       -0.123337
.

    - mm_X_Y.parquet: cada linha representa a proporção entre média móvel curta e média móvel longa. ex = 7 && 40 meses

    fórmula: (médiaCurta / médiaLonga)

        data        ticker      valor
    0   2023-10-26  WEGE3       0.952888
    1   2023-10-27  WEGE3       0.945331
.

    - volume_mediano.parquet: cada linha representa a mediana do volume negociado nos últimos 21 períodos para cada ação.

        data        ticker      valor
    0   2023-10-26  WEGE3       205862261.0
    1   2023-10-27  WEGE3       205862261.0
.

    - vol_X.parquet: volatilidade histórica anualizada dos retornos. cada linha representa a média, nos últimos X períodos, dos desvios padrões dos retornos de cada ação.
    
        data        ticker      valor
    0   2023-10-26  WEGE3       0.284484
    1   2023-10-27  WEGE3       0.286116
.

    - beta_X.parquet: 

        data        ticker      valor
    0   2023-10-26  WEGE3       0.527416
    1   2023-10-27  WEGE3       0.539298

.

    - pl_db.parquet: Proporção direta entre o Patrimônio Líquido e a Dívida Bruta de uma companhia.

    fórmula = (PatrimonioLiquido / DividaBruta)

        data        ticker      valor
    0   2023-10-29  WEGE3       5.827407
    1   2023-10-30  WEGE3       5.827407
.

    - ebit_dl.parquet: Proporção direta entre o EBIT e a Dívida Líquida da companhia. Quanto mais negativo, melhor.

    fórmula = (Ebit / DividaLiquida)

        data        ticker      valor
    0   2011-10-26  WEGE3       3.195411
    1   2011-10-27  WEGE3       3.195411


## 🎪 Fluxo de execução
    1) classe 'load_data_fintz.py' realiza atualização da base de dados
    2) classe 'making_indicators.py' cria indicadores e salva na base de dados
    4) classe 'premios_risco.py' cria o DataFrame dos retornos para o indicador selecionado. 
    5) rank companies monthly
    6) create montlhy_wallet

    ### BACK TESTING
    7) create monthly returns dataframe
    8) create returns heatmap plot for sns
    9) create acum returns heatmap plot for sns
    10) create ibov acum returns heatmap plot for sns 
    11) compare model & ibov monthly returns
    12) create compare ibov returns heatmap plot for sns
    13) configure heatmaps

### **1) load_data_fintz.py** - classe usada para criação e/ou atualização da base primária de dados
    - cotacoes()
    - cdi()
    - ibov()
    - *demonstrativos* / pegando_arquivo_contabil(demonstracao=True, nome_dado = 'X')
        - Ebit12m
        - DividaBruta
        - DividaLiquida
        - Ebit
        - LucroLiquido12m
        - PatrimonioLiquido
        - ReceitaLiquida12m
    - *indicadores* / pegando_arquivo_contabil(indicadores=True, nome_dado = 'X')
        - EV
        - EBIT_EV
        - L_P
        - P_L
        - ROE
        - ROIC
        - LPA
        - ValorDeMercado
### **2) fazendo_indicador.py** - classe usada para criação e/ou atualização de indicadores de análise.
    - fazer_indicador_momento(meses=X)
        - output: momento_X_meses.parquet
    - volume_mediano()
        - output: volume_mediano.parquet
    - media_movel_proporcao(X,Y)
        - output: mm_X_Y.parquet
    - beta(X)
        - output: beta_X.parquet
    - volatilidade(X)
        - output: vol_X.parquet
    - pl_divida_bruta()
        - output: pl_db.parquet
    - ebit_divida_liquida()
        - output: ebit_dl.parquet
### **3-a) premios_de_risco.py** - classe usada para cálculo dos prêmios de risco atrelado a cada combinação de fatores
    - pegando_dados_cotacoes()
    - pegando_datas_possiveis()
    - filtrando_volume()
    - pegando_indicadores()
    - descobrindo_mes_inicial()
    - calculando_premios()
        - output:
                ['df_premios', 'data', 'primeiro_quartil', 'segundo_quartil',
                'terceiro_quartil, 'quarto_quartil', 'universo', 'nome_premio',
                'liquidez', 'id_premio']

    - colocando_premio_na_base()
### **3-b) fator_mercado.py** - classe usada para cálculo do prêmio de risco do mercado
    - calculando_premio()
        - output: market_premium.parquet
### **4) avaliar_premios_de_risco.py** - classe
    - puxando_dados()
    - retorno_quartis()
    - fazer_pdf(
### **5) modelo_regressão.py** - classe
    -  OLS Regression Result
        ideal que:
            coef                Positivo (quanto maior, mais relevante na modelagem)
            R-squared           mais próximo de 1
            F-statistic         maior possível
            P-Valor (P>|t|)     menor possível (aceitável menor que 5%)
                queremos o ALPHA maior possível 'const'
    
                                OLS Regression Results Example
        ==============================================================================
        Dep. Variable:                   U_RF   R-squared:                       0.952
        Model:                            OLS   Adj. R-squared:                  0.950
        Method:                 Least Squares   F-statistic:                     495.6
        Date:                Tue, 31 Oct 2023   Prob (F-statistic):           2.05e-65
        Time:                        01:15:13   Log-Likelihood:                 294.70
        No. Observations:                 106   AIC:                            -579.4
        Df Residuals:                     101   BIC:                            -566.1
        Df Model:                           4
        Covariance Type:            nonrobust
        ============================================================================================
                                    coef    std err          t      P>|t|      [0.025      0.975]
        --------------------------------------------------------------------------------------------
        const                        0.0011      0.002      0.677      0.500      -0.002       0.004
        MOMENTO_R6M                  0.0589      0.028      2.086      0.039       0.003       0.115
        ALAVANCAGEM_EBIT_DL          0.1023      0.038      2.671      0.009       0.026       0.178
        TAMANHO_VALOR_DE_MERCADO     0.4513      0.034     13.420      0.000       0.385       0.518
        mkt_premium                  0.8485      0.029     29.262      0.000       0.791       0.906