import streamlit as st
import pandas as pd
import plotly.express as px

# Configurando a página
st.set_page_config(page_title='Gerenciamento de Estratégia de Investimento', page_icon=':chart_with_upwards_trend:')

# Adicionando abas à página
tabs = ['Visão Geral', 'Inputs', 'Gráficos']
selected_tab = st.sidebar.radio('Navegação', tabs)

# Dados fictícios para exemplo
data = pd.DataFrame({
    # 'Data': pd.date_range('2022-01-01', '2022-01-31'),
    # 'Preço': [100, 105, 110, 95, 102, 98, 115, 120, 125, 130, 128, 135, 140, 138, 145, 150, 155, 152, 160, 165, 170]
})

# Lógica para diferentes abas
if selected_tab == 'Visão Geral':
    st.title('Visão Geral da Estratégia de Investimento')
    st.write('Insira informações sobre a estratégia aqui.')

elif selected_tab == 'Inputs':
    st.title('Configurações e Parâmetros')
    # Adicione seus inputs aqui
    investment_amount = st.number_input('Quantidade de Investimento:', min_value=0.0)
    risk_tolerance = st.slider('Tolerância ao Risco:', min_value=0, max_value=10, value=5, step=1)

elif selected_tab == 'Gráficos':
    st.title('Análise Gráfica')
    # Adicione gráficos interativos aqui usando Plotly ou outras bibliotecas
    fig = px.line(data, x='Data', y='Preço', title='Preços ao longo do tempo')
    st.plotly_chart(fig)

# Executar o aplicativo
if __name__ == '__main__':
    st.write('')