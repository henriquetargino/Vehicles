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
# css
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

car_data = pd.read_csv('notebooks/car_data.csv')

st.title("Vehicles Dataframe")

# mostrar o DataFrame interativo ocupando a largura total da pagina
st.dataframe(car_data, use_container_width=True)

# adicionar botão de download para o arquivo CSV
csv = car_data.to_csv(index=False)
st.download_button(
    label="Upload CSV",
    data=csv,
    file_name='car_data.csv',
    mime='text/csv'
)

st.markdown("---")

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
        'text': 'Median Price Distribution by Brand',
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

st.markdown("---")

car_data_grouped2 = car_data.groupby(['brand', 'type']).size().reset_index(name='count')
fig2 = px.bar(
    car_data_grouped2,
    x='brand', 
    y='count',  # A contagem será mostrada no eixo Y
    color='type',  # Cada tipo de carro será colorido
    labels={
        'brand': 'Car Brand',  # Marca do carro
        'count': 'Total Cars',  # Contagem de carros
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
fig2.update_layout(
    title={
        'text': 'Number of Vehicle Types Produced by Each Brand',
        'x': 0.5,  # centraliza o título
        'xanchor': 'center'
    },
    title_font_size=24,  # tamanho da fonte do título
    xaxis_title_font_size=18, 
    yaxis_title_font_size=18,# tamanho da fonte do título do eixo x# tamanho da fonte do título do eixo y
    legend_font_size=13.7,  # tamanho da fonte da legenda
    legend_title_font_size=19,  # tamanho da fonte do título da legenda
)
st.plotly_chart(fig2)

st.markdown("---")

# Criar widgets de seleção para os usuários escolherem as marcas
brand1 = st.selectbox("Select brand 1:", car_data['brand'].unique(), index=0)
brand2 = st.selectbox("Select brand 2:", car_data['brand'].unique(), index=1)

# Filtrar os dados com base nas marcas selecionadas
filtered_data = car_data[(car_data['brand'] == brand1) | (car_data['brand'] == brand2)]

# Calcular a mediana do preço a cada ano para as marcas selecionadas
median_price_per_year = filtered_data.groupby(['model_year', 'brand'])['price'].median().reset_index()

# Criar gráfico para comparar as medianas dos preços por ano das marcas selecionadas
fig3 = px.line(median_price_per_year, x='model_year', y='price', color='brand',
               labels={
                   'model_year': 'Model Year',
                   'price': 'Median Price',
                   'brand': 'Car Brand'
               },
               title='Median Price per Year for Selected Brands',
               color_discrete_sequence=['#85FFC7', '#FE5D26'], 
               )
fig3.update_layout(
    title_font_size=16.5,  # tamanho da fonte do título
    xaxis_title_font_size=18, 
    yaxis_title_font_size=18,# tamanho da fonte do título do eixo x# tamanho da fonte do título do eixo y
    legend_font_size=13.7,  # tamanho da fonte da legenda
    legend_title_font_size=15.5,  # tamanho da fonte do título da legenda
)
# Exibir o gráfico no Streamlit
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# distribuição de cores de carros sem "unknown" 
car_data_grouped4 = car_data[car_data['paint_color'] != 'unknown'].groupby('paint_color').size().reset_index(name='count').sort_values(by='count', ascending=False)

fig4 = px.bar(car_data_grouped4, x='paint_color', y='count', 
              labels={'paint_color': 'Paint Color', 'count': 'Total Cars'},
              title='Distribution of Car Colors',
              color='paint_color',
              color_discrete_sequence=['#ffffff', '#000000', '#C0C0C0', '#808080', '#0000FF', '#FF0000', 
                                       '#008000', '#582f0e', '#CD7F32', '#FFFF00', '#fb8500', '#800080'],
              )

st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")



# Organizar os valores da coluna 'condition'
condition_order = ['new', 'like new', 'excellent', 'good', 'fair', 'savage']
car_data['condition'] = pd.Categorical(car_data['condition'], categories=condition_order, ordered=True)

# fazer um gráfico para ver qual é a marca, cor, condição e transmissão mais facilmente vendida com a coluna days_listed
car_data_grouped5 = car_data.groupby(['brand', 'condition'])['days_listed'].median().reset_index()
fig5 = px.scatter(car_data_grouped5, x='days_listed', y='brand', color='condition',
                  labels={
                      'brand': 'Car Brand',  # Marca do carro
                      'days_listed': 'Median Days Listed',  # Mediana dos dias listados
                      'condition': 'Condition'  # Condição do carro
                  },
                  height=600,
                  hover_name='condition',
                  # Personalizar o hover
                  hover_data={'brand': True, 'days_listed': True, 'condition': True},
                  color_discrete_sequence=px.colors.qualitative.Set1
                  )

# Atualizar o layout do gráfico para aumentar o tamanho das legendas e centralizar o título
fig5.update_layout(
    title={
        'text': 'Impact of Brand and Condition on Median Days Listed',
        'x': 0.5,  # Centraliza o título
        'xanchor': 'center'
    },
    title_font_size=24,  # Tamanho da fonte do título
    xaxis_title_font_size=18,  # Tamanho da fonte do título do eixo x
    yaxis_title='Car Brand',  # Adiciona a legenda ao eixo y
    yaxis_title_font_size=18,  # Tamanho da fonte do título do eixo y
    legend_font_size=13.7,  # Tamanho da fonte da legenda
    legend_title_font_size=19,  # Tamanho da fonte do título da legenda
)

# tirando unknown
car_data_filtered = car_data[car_data['paint_color'] != 'unknown']

# Fazer um gráfico para ver qual é a marca, cor, condição e transmissão mais facilmente vendida com a coluna days_listed, substituindo condition por paint_color
car_data_grouped6 = car_data_filtered.groupby(['brand', 'paint_color'])['days_listed'].median().reset_index()
fig6 = px.scatter(car_data_grouped6, x='days_listed', y='brand', color='paint_color',
                  labels={
                      'brand': 'Car Brand',  # Marca do carro
                      'days_listed': 'Median Days Listed',  # Mediana dos dias listados
                      'paint_color': 'Paint Color'  # Cor do carro
                  },
                  height=600,
                  hover_name='paint_color',
                  # Personalizar o hover
                  hover_data={'brand': True, 'days_listed': True, 'paint_color': True},
                  color_discrete_sequence=px.colors.qualitative.Set1
                  )

# Atualizar o layout do gráfico para aumentar o tamanho das legendas e centralizar o título
fig6.update_layout(
    title={
        'text': 'Impact of Brand and Paint Color on Median Days Listed',
        'x': 0.5,  # Centraliza o título
        'xanchor': 'center'
    },
    title_font_size=24,  # Tamanho da fonte do título
    xaxis_title_font_size=18,  # Tamanho da fonte do título do eixo x
    yaxis_title='',  # Adiciona a legenda ao eixo y
    yaxis_title_font_size=18,  # Tamanho da fonte do título do eixo y
    legend_font_size=13.7,  # Tamanho da fonte da legenda
    legend_title_font_size=19,  # Tamanho da fonte do título da legenda
)

car_data_grouped7 = car_data.groupby(['brand', 'type'])['days_listed'].median().reset_index()
fig7 = px.scatter(car_data_grouped7, x='days_listed', y='brand', color='type',
                  labels={
                      'brand': 'Car Brand',  # Marca do carro
                      'days_listed': 'Median Days Listed',  # Mediana dos dias listados
                      'type': 'Car Type'  # Tipo do carro
                  },
                  height=600,
                  hover_name='type',
                  # Personalizar o hover
                  hover_data={'brand': True, 'days_listed': True, 'type': True},
                  color_discrete_sequence=px.colors.qualitative.Set1
                  )

# Atualizar o layout do gráfico para aumentar o tamanho das legendas e centralizar o título
fig7.update_layout(
    title={
        'text': 'Impact of Brand and Type on Median Days Listed',
        'x': 0.5,  # Centraliza o título
        'xanchor': 'center'
    },
    title_font_size=24,  # Tamanho da fonte do título
    xaxis_title_font_size=18,  # Tamanho da fonte do título do eixo x
    yaxis_title='Car Brand',  # Adiciona a legenda ao eixo y
    yaxis_title_font_size=18,  # Tamanho da fonte do título do eixo y
    legend_font_size=13.7,  # Tamanho da fonte da legenda
    legend_title_font_size=19,  # Tamanho da fonte do título da legenda
)

# Converter a coluna 'cylinders' para categoria
car_data['cylinders1'] = car_data['cylinders'].astype('category')

# Fazer um gráfico para ver qual é a marca, cilindros e transmissão mais facilmente vendida com a coluna days_listed
car_data_grouped8 = car_data.groupby(['brand', 'cylinders1'])['days_listed'].median().reset_index()
fig8 = px.scatter(car_data_grouped8, x='days_listed', y='brand', color='cylinders1',
                  labels={
                      'brand': 'Car Brand',  # Marca do carro
                      'days_listed': 'Median Days Listed',  # Mediana dos dias listados
                      'cylinders1': 'Cylinders'  # Cilindros do carro
                  },
                  height=600,
                  hover_name='cylinders1',
                  # Personalizar o hover
                  hover_data={'brand': True, 'days_listed': True, 'cylinders1': True},
                  color_discrete_sequence=px.colors.qualitative.Set1
                  )

# Atualizar o layout do gráfico para aumentar o tamanho das legendas e centralizar o título
fig8.update_layout(
    title={
        'text': 'Impact of Brand and Cylinders on Median Days Listed',
        'x': 0.5,  # Centraliza o título
        'xanchor': 'center'
    },
    title_font_size=24,  # Tamanho da fonte do título
    xaxis_title_font_size=18,  # Tamanho da fonte do título do eixo x
    yaxis_title='',  # Adiciona a legenda ao eixo y
    yaxis_title_font_size=18,  # Tamanho da fonte do título do eixo y
    legend_font_size=13.7,  # Tamanho da fonte da legenda
    legend_title_font_size=19,  # Tamanho da fonte do título da legenda
)

# Exibir os gráficos em 2x2
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig5, use_container_width=True, key="fig5")
    st.plotly_chart(fig7, use_container_width=True, key="fig7")
with col2:
    st.plotly_chart(fig6, use_container_width=True, key="fig6")
    st.plotly_chart(fig8, use_container_width=True, key="fig8")
    
    
# Agrupar os dados por tipo de carro e tipo de combustível e contar o número de veículos
car_data_grouped9 = car_data.groupby(['type', 'fuel']).size().reset_index(name='count')

# Criar o gráfico de barras empilhadas para distribuição de tipo de combustível por tipo de carro
fig9 = px.bar(car_data_grouped9, x='type', y='count', color='fuel',
              labels={
                  'type': 'Car Type',  # Tipo de carro
                  'count': 'Number of Cars',  # Contagem de carros
                  'fuel': 'Fuel Type'  # Tipo de combustível
              },
              height=580,
              hover_name='fuel',
              # Personalizar o hover
              hover_data={'type': True, 'count': True},
              color_discrete_sequence=px.colors.qualitative.Set1
              )

# Atualizar o layout do gráfico para aumentar o tamanho das legendas e centralizar o título
fig9.update_layout(
    title={
        'text': 'Distribution of Fuel Types by Car Type',
        'x': 0.5,  # Centraliza o título
        'xanchor': 'center'
    },
    title_font_size=24,  # Tamanho da fonte do título
    xaxis_title_font_size=18, # Tamanho da fonte do título do eixo x
    yaxis_title='Total Cars',  # Adiciona a legenda ao eixo y
    yaxis_title_font_size=18,# Tamanho da fonte do título do eixo y
    legend_font_size=13.7,  # Tamanho da fonte da legenda
    legend_title_font_size=19,  # Tamanho da fonte do título da legenda
)

st.plotly_chart(fig9)
