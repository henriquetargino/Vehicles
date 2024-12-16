import pandas as pd
import plotly.express as px
import streamlit as st

# configuração do layout da página
st.set_page_config(
    page_title="Vehicles Dataframe",
    page_icon="🚗",
    layout="wide",  # tela inteira
    initial_sidebar_state="expanded",
    menu_items={  # personalização dos itens do menu de hambúrguer
        'Get Help': 'https://www.globo.com.br',
        'Report a bug': 'https://www.example.com/bug',
        'About': '## Testando'
    }
)

# CSS personalizado
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

car_data = pd.read_csv('notebooks/car_data.csv')

st.title("Vehicles Dataframe")


st.markdown(
    """
    <style>
    .stDataframe {
        border-bottom: 0px;

    }
    </style>
    """,
    unsafe_allow_html=True
)
# mostrar o DataFrame interativo ocupando a largura total da pagina
st.dataframe(car_data, use_container_width=True)

# adicionar botão de download para o arquivo CSV
csv = car_data.to_csv(index=False)
st.markdown(
    """
    <style>
    .stDownloadButton {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
        margin-top: 0px;

    }
    </style>
    """,
    unsafe_allow_html=True
)

st.download_button(
    label="Upload CSV",
    data=csv,
    file_name='car_data.csv',
    mime='text/csv'
)
# agrupar os dados por marca e calcular a média do preço
car_data_grouped = car_data.groupby('brand')['price'].median(
).reset_index().sort_values(by='price', ascending=False)
fig = px.bar(car_data_grouped, x='price', y='brand',
             color='brand',
             labels={'price': 'Median Price', 'brand': 'Car Brand'},
             height=580,
             hover_name='brand',
             # personalizar o hover
             hover_data={'price': ':.f', 'brand': False},
             )

fig.update_layout(
    title={
        'text': 'Average Price Distribution by Brand',
        'x': 0.5,  # centraliza o título
        'xanchor': 'center'
    },
    title_font_size=24,  # tamanho da fonte do título
    xaxis_title_font_size=18,  # tamanho da fonte do título do eixo x
    yaxis_title=None,  # tamanho da fonte do título do eixo y
    legend_font_size=13.7,  # tamanho da fonte da legenda
    legend_title_font_size=19,  # tamanho da fonte do título da legenda
)

# personalizar o hover usando update_traces
fig.update_traces(
    hovertemplate='Brand:  %{y}<br>Price:  %{x:.2f}<extra></extra>'
)

st.plotly_chart(fig)


car_data_grouped2 = car_data.groupby(['brand', 'type']).size().reset_index(name='count')
fig2 = px.bar(
    car_data_grouped2,
    x='brand', 
    y='count',  # A contagem será mostrada no eixo Y
    color='type',  # Cada tipo de carro será colorido
    labels={
        'brand': 'Car Brand',  # Marca do carro
        'count': 'Number of Cars',  # Contagem de carros
        'type': 'Car Type'  # Tipo de carro
    },
    height=580,
    hover_name='type',  # Nome do tipo do carro no hover
    hover_data={'brand': True, 'count': True},  # Exibe informações adicionais no hover
    color_discrete_sequence = [
    '#0FD2AB',  # verde agua
    '#F17105',  # laranja
    '#D62728',  # Vermelho
    '#569866',  # verde pantano
    '#4C78A8'   # azul meio roxo
])

st.plotly_chart(fig2)
