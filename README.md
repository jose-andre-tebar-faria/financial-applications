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

    *cotacoes*: cada linha representa a lista preços - incluindo preços ajustados - e quantidades negociadas de cada dia de cada ação.

        ['preco_abertura', 'preco_abertura_ajustado', 
        'preco_fechamento', 'preco_fechamento_ajustado', 
        'preco_maximo', 'preco_maximo_ajustado', 
        'preco_medio', 'preco_medio_ajustado', 
        'preco_minimo', 'preco_minimo_ajustado',
        'quantidade_negociada',
        'quantidade_negocios']

                  data  preco_abertura  preco_fechamento  preco_maximo  preco_medio ...
    0       2010-01-04           11.50             11.50         11.50        11.50 ...
    67071   2010-01-04           38.89             40.12         40.49        39.96 ...

    *ibov*: cada linha representa o número de pontos do ibovespa por dia.
                data  fechamento
    0     2000-01-03  16930.42
    1     2000-01-04  15851.00

    *cdi*: representa em cada linha a porcentagem de retorno da renda fixa no Brasil.
                data  retorno
    0     2000-01-03  0.000683
    1     2000-01-04  0.000682

    *market_premium*: cada linha representa a proporção entre os retornos do mercado (ibov) e a renda fixa (cdi) por mês - último dia.
                data  mkt_premium
    1    2000-02-29   -0.464910
    2    2000-03-31   -0.331790

Todo arquivo contendo um indicador deve seguir o seguinte padrão de dados indicado abaixo.

    ['data', 'ticker', 'valor'] 

- **data**: *reprensenta uma data no formato YYYY-MM-DD.*
- **ticker**: *representa o código de negociação da ação no formato 4 letras 1 número (ex: PETR3).*
- **valor**: *número inteiro reprensentando o tamanho daquele indicador naquele dia praquela ação.*

Cada .parquet contido no database se refere ao seguinte indicador.

    *EBIT_EV*: 

    *L_P ou P_L*:

    *ValorDeMercado*:

    *ROE*: 

    *ROIC*: 

    *EV*: 

    *LPA*: 

    *momento_X_meses*: cada linha representa a média móvel dos últimos X meses dos retornos para cada ação.

    *mm_X_Y*: cada linha representa a proporção entre média móvel curta e média móvel longa. (mmCurta/mmLonga)

    *volume_mediano*: cada linha representa a mediana do volume negociado nos últimos 21 períodos para cada ação.

    *vol_X*: volatilidade histórica anualizada dos retornos. cada linha representa a média, nos últimos X períodos, dos desvios padrões dos retornos de cada ação.

    *beta_X*:

    *pl_db*:

    *Ebit_12m*:

## 🎪 Fluxo de execução

### **1) load_data_fintz.py** - classe usada para criação da base primária de dados
    - cotacoes()
    - cdi()
    - ibov()
    - *demonstrativos* / pegando_arquivo_contabil(demonstracao=True, nome_dado = 'X')
        - Ebit12m
        - DividaBruta
        - DividaLiquida
        - Ebit12m
        - LucroLiquido12m
        - PatrimonioLiquido
        - ReceitaLiquida12m
    - *indicadores* / pegando_arquivo_contabil(indicadores=True, nome_dado = 'X')
        - EBIT_EV
        - L_P
        - ROE
        - ROIC
        - ValorDeMercado
### **2) fazendo_indicador.py** - classe usada para criação de indicadores de análise.
    - fazer_indicador_momento()
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
    - colocando_premio_na_base()
### **3-b) fator_mercado.py** - classe usada para cálculo do prêmio de risco do mercado
    - calculando_premio()
        - output: market_premium.parquet
### **4) avaliar_premios_de_risco.py** - classe
    - puxando_dados()
    - retorno_quartis()
    - fazer_pdf()
    - test