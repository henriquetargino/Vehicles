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

car_data = pd.read_csv('notebooks/car_data.csv')

st.title("Vehicles Dataframe")

# mostrar o DataFrame interativo ocupando a largura total da pagina
st.dataframe(car_data, use_container_width=True)


# agrupar os dados por marca e calcular a média do preço
car_data_grouped = car_data.groupby('brand')['price'].median().reset_index().sort_values(by='price', ascending=False)
fig = px.bar(car_data_grouped, x='price', y='brand', 
                               color='brand',  
                               title='Median Price X Car Brand', 
                               labels={'price': 'Median Price', 'brand': 'Car Brand'},
                               height=580,
                               hover_name='brand',
                               hover_data={'price': ':.f', 'brand': False},  # personalizar o hover
)

fig.update_layout(
    title={
        'text': 'Median Price X Car Brand',
        'x': 0.5,  # Centraliza o título
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

