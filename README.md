<h1 align="center">
    <img src=".\files\images\colored_eye.svg" width="155" />
    <p>🙇🏽‍♂️ financial-applications 🙇🏽 </p>
</h1>

## 🚨 ABOUT

<div style="text-align: justify;">

### This repository, financial-applications, contains a wealth of Python code for downloading and analyzing stock market data. Our flagship application, ***FINAPP***, aims to create an end-to-end system capable of manipulating an extensive database of market information to optimize, suggest, and execute the best indices and assets for stock investments in the Brazilian market.
</div>

#

<h1 align="center">
    <img src=".\files\images\gear.svg" width="142" />
    <p>FINAPP</p>
</h1>

## 🚨 ABOUT

<div style="text-align: justify;">

### This **Project** intends to create an application that can optimize a stock wallet rebalances for long-term investments. Using a Factor Investiment methology to rate indices that represent companies, we're trying to develop an application that full-automatizate - from ana
</div>

#

## 🧭 Factor Investing

O modelo de 5 fatores, desenvolvido por Eugene Fama e Kenneth French, é uma extensão do modelo de três fatores original (CAPM) que visa explicar os retornos de ações com base em cinco fatores diferentes. Esses cinco fatores são:

- **Retorno do Mercado (Market Risk Premium)**: Este fator representa o retorno do mercado como um todo e é frequentemente capturado pelo retorno de um índice de mercado amplo, como o S&P 500. Ele mede o prêmio de risco associado a investir em ações em vez de um ativo livre de risco.

- **Capitalização de Mercado (Market Capitalization)**: Esse fator captura o prêmio associado a investir em ações de diferentes tamanhos de capitalização. As ações de pequena capitalização tendem a ter retornos diferentes das ações de grande capitalização. Portanto, esse fator leva em consideração as ações com base em sua capitalização de mercado.

- **Valor (Value)**: O fator de valor mede o prêmio de risco associado a investir em ações com baixas relações preço/lucro (P/L), baixas relações preço/valor contábil (P/VC) e outras métricas de valor. Em termos simples, ele procura identificar ações que estão subvalorizadas em relação aos seus fundamentos.

- **Momentum (Momentum)**: Este fator reflete a tendência recente dos preços das ações. Ações que tiveram um forte desempenho no passado tendem a continuar a ter um desempenho forte no curto prazo, enquanto ações que tiveram um desempenho fraco tendem a continuar com desempenho fraco.

- **Qualidade (Quality)**: O fator de qualidade considera métricas de qualidade financeira das empresas, como a estabilidade dos lucros, a força do balanço e a eficiência operacional. Ações de empresas com alta qualidade financeira tendem a ter um desempenho melhor.

Esses cinco fatores são usados para analisar os retornos das ações e entender melhor as fontes de risco e retorno no mercado de ações. O modelo de 5 fatores é uma extensão significativa em relação ao modelo de três fatores original (CAPM), que considerava apenas o mercado, o tamanho e o valor. A incorporação de fatores como momentum e qualidade torna o modelo mais robusto na explicação dos retornos das ações e é frequentemente usado no contexto de factor investing para criar estratégias de investimento baseadas em fatores específicos.

## 🪒 Equation
<h1 align="center">
    <img src=".\files\images\fama-french-5-factor-model-equation.png" width="1550" />
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

## 🎪 Fluxo de execução
A aplicação tem 4 grandes núcleos de execução e tratamento de dados, conforme indicado abaixo:

<div style="text-align: justify;">

1. **Gerenciamento de dados**: o objetivo aqui é possuir uma base de dados concisa e confiável para que toda a metodologia aplicada não seja comprometida por dados errados. Parte dos dados tem como origem a plataforma Fintz (Curso Código.py) através de uma API disponibilizada por eles (classe ***FintzData*** provinda do arquivo ***download_by_fintz.py***). Também foram criadas classes para download de dados via API (classe ***DownloadByApi*** provinda do arquivo ***download_by_api.py***) e Webscraping (classe ***DownloadByWebscrapping*** provinda do arquivo ***download_by_webscraping.py***). Além das classes de download de dados também foram criadas classes para tratamento de dados de cadastro de empresas para que possa ser usado no momento de apresentar resultados de forma informativa. Para isso existem as classes ***UpdateAssetProfile***, provinda do arquivos ***update_asset_profile.py***, e ***BcgMatrix*** provinda do arquivo ***create_bcg_matrix.py***.

___
#### **download_by_fintz.py** - classe usada para criação e/ou atualização da base primária de dados
    download_quotations() - método usado para baixar os dados históricos de cotação.

    download_cdi(initial_date) - método usado para baixar os dados históricos dos retornos do CDI.

    download_ibov(initial_date) - método usado para baixar os dados históricos dos retornos do índice do Ibovespa.

    download_accounting_files(demonstration = True, data_name = 'X')
        - Ebit12m
        - DividaBruta
        - DividaLiquida
        - Ebit
        - LucroLiquido12m
        - PatrimonioLiquido
        - ReceitaLiquida12m

    download_accounting_files(indicators = True, data_name = 'X')
        - EV
        - EBIT_EV
        - L_P
        - P_L
        - ROE
        - ROIC
        - LPA
        - ValorDeMercado
#### **download_by_api.py** - classe usada para criação e/ou atualização da base primária de dados através de métodos que invocam APIs
    getting_bc_data(bc_dict) - método usado para baixar dados provindos da base de dados do Banco Central através da dos códigos de cada dado.

#### **download_by_webscraping.py** - classe usada para criação e/ou atualização da base primária de dados através de métodos que usam técnica de webscraping em websites
    getting_b3_assets_sector_by_site() - método usado para fazer webscraping do website da B3 para pegar os setores das empresas listadas na bolsa brasileira.

    getting_asset_logos_google_by_site() - método usado para fazer webscraping dos logos (.png) das empresas existentes no database pelo site do Google.

#### **update_asset_profile.py** - classe usada para criação e/ou atualização da base cadastral das empresas.
    getting_assets_database() - método usado para leitura da base de empresas - sectors_assets_b3_webscraping.parquet - providas do webscraping do website da B3.

    getting_assets_from_quotation() - método usado para busca das empresas distintas presentes na base de cotações para iniciar a criação do banco de dados cadastral das empresas.

    calculationg_growth_rate() - método usado para busca e preparo dos dados para cálculo da taxa de crescimento aplicando a função de variação percentual do valores de mercado ANUAL de cada empresa e captura da última taxa de crescimento das empresas. essa busca é feita na base de ValorDeMercado.

    calculationg_marketshare() - método usado para cálculo de marketshare das empresas presentes na base de cotações com relação ao Setor e Subsetor identificado a partir do webscraping no website da B3.

    save_profile_database() - método usado para salvar o dataframe criado, e concatenado, a partir dos métodos anteriores no arquivo asset_database.parquet.

    read_profile_database() - método usado para leitura do banco de dados cadastral e informativo de empresas no arquivo asset_database.parquet. o método retorna um dataframe com os dados para trabalho.

#### **create_bcg_matrix.py** - classe usada para criação e/ou atualização da base de dados contendo a classificação referente a metodologia da Matriz BCG.
    create_bcg_matrix() - método usado para criação do arquivo bcg_matrix.parquet na qual contém a classificação BCG das empresas listadas na B3 em 4 grupos, Estrela / Vaca Leitera / Ponto de Interrogação / Abacaxi. essa classificação é feita por Setor e Subsetor para que consigamos segregar melhor os dados, para definir os limites de classificação de cada quadrante foi feita a média aritimética de taxas de crescimento e marketshare de cada Setor ou Subsetor.

    read_bcg_matrix_database() - método usado para leitura da base de dados de classificação BCG contida no arquivo bcg_matrix.parquet.

#### **make_indicators.py** - classe usada para criação e/ou atualização da base de dados contendo indicadores calculados pela própria aplicação a partir de dados já baixados anteriormente.
    making_momentum(months) - método usado para cálculo da média de rentabilidade dos últimos 'months' meses referente exclusivamente a variação dos preços de fechamentos mensal de cada empresa. é criado como output desse método um arquivo chamado momento_{months}_meses.parquet.

    median_volume(months) - método usado para cálculo do volume mediano transacionado mensalmente por cada ticker criando o arquivo volume_mediano.parquet como output.

    ebit_divida_liquida() - método usado para cálculo a proporção entre EBIT e Dívida Líquida de cada empres, criando o arquivo ebit_dl.parquet como output.

    pl_divida_bruta() - método usado para cálculo da proporção entre o Patrimônio Líquido e a Dívida Bruta de uma empresa, criando o arquivo pl_db.parquet como output.

    volatility(years) - método usado para cálculo da volatilidade (variância) do preço de cada empresa num período de 'years' anos, criando o arquivo vol_{int(252 * years)}.parquet como output.

    beta(years) - método usado para cálculo do Beta das empresas da bolsa realizando uma regressão linear contra o Ibovespa, criando o arquivo beta_{int(252 * years)}.parquet como output.

    ratio_moving_mean(mm_curta, mm_longa) - método usado para cálculo da proporção entre as médias móveis de dois períodos (longo e curto) para identificar o cruzamento dessas médias, como feito na análise técnica. Caso a média menor for maior que a média longa apresenta uma tendência de alta, criando o arquivo mm_{mm_curta}_{mm_longa}.parquet como output.

</div>


___
2. **Cálculo e Avaliação de prêmios de risco associados aos indicadores**: 

___
3. **Execução de backtests com parâmetros realistas**: 

___
4. **Automatização do rebalanceamento de carteiras**:




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

#


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

