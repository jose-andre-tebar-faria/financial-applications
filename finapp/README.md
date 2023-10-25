<h1 align="center">
    <img src=".\files\images\gear.svg" width="155" />
    <p>🙇🏽‍♂️🙇🏽‍♂️🙇🏽‍♂️ FINAPP 🙇🏽‍♂️🙇🏽‍♂️🙇🏽‍♂️ </p>
</h1>

## 🚨 ABOUT

### This **Project** intends to create an application that can optimize a stock wallet for long-term investments. Where are using here ywo types of analisys, first a Factor Investing modeling considering a 5 Factor Model by Eugene Fama & Kenneth French, and then a technical analisys.

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
Relação preço/valor contábil (P/VC): O P/VC compara o preço da ação com o valor contábil por ação da empresa. Um P/VC baixo é indicativo de valor.

- **Momentum (Momentum)**

    - **Retorno passado**: Esse fator leva em consideração o desempenho recente das ações. Os retornos passados, frequentemente mensais, são usados para avaliar o momentum.

- **Qualidade (Quality)**

    - **Margem de lucro**: A margem de lucro reflete a rentabilidade da empresa, medida como a relação entre o lucro líquido e a receita total.
    - **Endividamento**: O nível de dívida da empresa, muitas vezes medido pela relação entre dívida e patrimônio líquido ou pela relação entre dívida e EBITDA.
    - **Eficiência operacional**: Isso pode ser avaliado por métricas como o retorno sobre o patrimônio líquido (ROE) e o retorno sobre o ativo (ROA).

## 🗺 Relacionamento de entidades

    market_premium


    Beta: 
    EBIT_EV: 
    Momentos:
    L_P:
    ROE:
    ROI: 
    VOL:
    ValorDeMercado:
