import pandas as pd
import plotly.express as px
import streamlit as st


def app():

    # layout da página
    st.set_page_config(
        page_title="Vehicles Dataframe",
        page_icon="🚗",
        layout="wide",  # tela inteira
        initial_sidebar_state="expanded",
        menu_items={  # tres pontinhos
            'Get Help': 'https://www.globo.com',
            'Report a bug': 'https://www.example.com/bug',
            'About': '## Testando'
        }
    )
    # css
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    car_data = pd.read_csv('notebooks/car_data.csv')
    # me apresentando e apresentando o projeto
    st.markdown("""
        <div class="custom-title">
            👋 Hi! My name is <strong>Henrique Targino</strong>.<br>
        &emsp;&nbsp;&nbsp;&nbsp;Welcome to my Web App! 🚗
        </div>
        """, unsafe_allow_html=True)
    st.header("About the Project:")
    st.markdown("""
        <div class="about-project">
        This project is a Streamlit Web App that uses the data of car sales platform to create interactive visualizations with the Plotly Express library.
        The dataset contains over 51,000 rows information about vehicles, which we will unpack later.
        The purpose of this project is to explore the data and create visualizations to help understand the dataset better.
        If you like my insights, consider giving a star to my project on <a href="https://github.com/henriquetargino/Vehicles">GitHub</a> 
        (all my comments and issues faced are in the repository's README). 
        And if you are interested in my work, here is my <a href="https://www.linkedin.com/in/henriquetargino/">Linkedin</a>! Now let's dive into analyzing this data.
        </div>
        """, unsafe_allow_html=True)

    st.title("Vehicles Dataframe Overview")

    # dataFrame interativo ocupando a largura total da pagina
    st.dataframe(car_data, use_container_width=True)

    # criar em ingles um cabeçalho "legenda do dataframe"
    st.header("Columns Legend:")

    left_column, right_column = st.columns(2)

    with left_column:
        st.markdown("""
    > - "Price": Price of the vehicle.
    > - "Model Year": Year the vehicle was manufactured.
    > - "Model": Model of the vehicle.
    > - "Condition": Condition of the vehicle.
    > - "Cylinders": Number of cylinders in the vehicle's engine.
    > - "Fuel": Type of fuel used by the vehicle.
    > - "Odometer": Number of miles the vehicle has been driven.
    > - "Transmission": Type of transmission used by the vehicle.
    > - "Type": Type of vehicle.
        """)

    with right_column:
        st.markdown("""
    > - "Paint Color": Color of the vehicle.
    > - "Is_4wd": Whether the vehicle has 4-wheel drive (1 = True and 0 = False).
    > - "Date Posted": Date the vehicle was posted for sale.
    > - "Days Listed": Number of days the vehicle was listed for sale.
    <br><br>My column contributions:
    >>- "Year_posted": Year the vehicle was posted for sale.
    >>- "Brand": Brand of the vehicle.
    >>- "Car Age": Age of the vehicle.
        """, unsafe_allow_html=True)
    # botão de download para o arquivo CSV
    csv = car_data.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='car_data.csv',
        mime='text/csv'
    )

    st.markdown("---")

    st.header("Start the Analysis:")

    st.markdown("""After using Jupyter Notebook to perform the initial part of the Exploratory Data Analysis (EDA),
                we can start exploring the data and creating interactive visualizations to better understand the dataset. 
                Since this is a car sales platform, let's analyze which brand costs the most for the consumer. 
                Then, let's take a look at the distribution of vehicle prices by brand:""", unsafe_allow_html=True)

    # agrupar os dados por marca e calcular a média do preço
    car_data_grouped = car_data.groupby('brand')['price'].median(
    ).reset_index().sort_values(by='price', ascending=False)
    fig = px.bar(car_data_grouped, x='price', y='brand',
                color='brand',
                labels={'price': 'Price ($)', 'brand': 'Car Brand'},
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

    st.caption("""<div class="legends"> 
            All charts are interactive. Hover over the points to see more information.
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    st.header("Cars Type Distribution:")

    st.markdown("""Now, I want to analyze which type of car is most manufactured by each brand 
                listed in the dataset and determine the most produced type overall. At first glance, 
                the chart might seem a bit overwhelming, but, like all charts in this application, 
                it is interactive. To make the most of it, simply double-click on the right legend to 
                highlight a specific car type and analyze it individually.""", unsafe_allow_html=True)


    car_data_grouped2 = car_data.groupby(['brand', 'type']).size().reset_index(name='count')
    
    car_data_grouped2 = car_data_grouped2.sort_values(by='count', ascending=False)
    
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
        xaxis={'categoryorder': 'total descending'} 
    )
    st.plotly_chart(fig2)

    st.caption("""<div class="legends"> 
                When double-clicking on the legend, pay attention to the change on the Y-axis.
            </div>""", unsafe_allow_html=True)
    
    st.markdown("---")

    st.header("Brand X Brand:")

    st.markdown("""The following line chart compares the median vehicle prices of two selected brands 
                based on their manufacturing year. For example, if you select 'Cadillac' and 'BMW,' the 
                chart shows that cars manufactured between 2000 and 2014 maintain a low price, but from 2015 onwards,
                the chart rises exponentially. This could indicate that cars from these brands experience high depreciation, 
                and in a short period, they lose significant value. It’s an interesting hypothesis — we can test it! Use the 
                select box to freely explore the chart (just keep in mind that the X-axis represents the manufacturing year, 
                not the number of cars sold that year).
                """, unsafe_allow_html=True)
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
                    'price': 'Price ($)',
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

    st.caption("""<div class="legends"> 
            Disclaimer: The data is exclusively from the car 
            sales platform in question and does not reflect the market as a whole.
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    st.header("What's the Most Popular Car Color?")

    st.markdown("""Analyzing the data, we can see that the color of the car is an important factor 
                in the purchase decision. Therefore, we will examine the distribution of car colors and 
                identify the most popular color among consumers. Additionally, understanding these preferences 
                can provide valuable insights for manufacturers and sellers to align with market demands.""", unsafe_allow_html=True)

    # distribuição de cores de carros sem "unknown" 
    car_data_grouped4 = car_data[car_data['paint_color'] != 'unknown'].groupby('paint_color').size().reset_index(name='count').sort_values(by='count', ascending=False)

    fig4 = px.bar(car_data_grouped4, x='paint_color', y='count', 
                labels={'paint_color': 'Paint Color', 'count': 'Total Cars'},
                title='Distribution of Car Colors',
                color='paint_color',
                color_discrete_sequence=['#ffffff', '#181818', '#C0C0C0', '#808080', '#0000FF', '#FF0000', 
                                        '#008000', '#582f0e', '#CD7F32', '#FFFF00', '#fb8500', '#800080'],
                )

    fig4.update_layout(
        title_font_size=17)
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    st.header("Distribution of Fuel Types by Car Type:")

    st.markdown("""Analyzing the distribution of fuel types by car type is essential to understanding the vehicle market. 
                Beyond providing valuable insights for manufacturers and sellers, this analysis can help identify trends in the fuel market. 
                The stacked bar chart below illustrates the distribution of fuel types across car categories, showing which type of fuel is 
                most commonly used for each car type. Use the interactive chart in the same way you explored the second chart.
                """, unsafe_allow_html=True)
    

    # Agrupar os dados por tipo de carro e tipo de combustível e contar o número de veículos
    car_data_grouped4= car_data.groupby(['type', 'fuel']).size().reset_index(name='count').sort_values(by='count', ascending=False)

    # Criar o gráfico de barras empilhadas para distribuição de tipo de combustível por tipo de carro
    fig4 = px.bar(car_data_grouped4, x='type', y='count', color='fuel',
                labels={
                    'type': 'Car Type',  # Tipo de carro
                    'count': 'Number of Cars',  # Contagem de carros
                    'fuel': 'Fuel Type'  # Tipo de combustível
                },
                height=580,
                hover_name='fuel',
                # Personalizar o hover
                hover_data={'type': True, 'count': True},
                color_discrete_sequence=['#1f77b4', '#d62728', '#2ca02c', '#ff7f0e', '#9467bd']
                )

    # Atualizar o layout do gráfico para aumentar o tamanho das legendas e centralizar o título
    fig4.update_layout(
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

    st.plotly_chart(fig4)
    
    st.caption("""<div class="legends"> 
                The cars in the dataset range from 1908 to 2019, which is why the number of electric cars is low.
            </div>""", unsafe_allow_html=True)    
    
    st.markdown("---")
    st.header("Which Brand is Easiest to Sell? And Which is the Most Difficult?")
    st.markdown("""Do you know what a boxplot is? It's a chart that provides an overview of the data distribution. 
                It displays the median (the line in the middle), Q1 (the lower boundary of the box, representing 25% 
                of the data), Q3 (the upper boundary of the box, representing 75% of the data), and the <u>outliers</u> (points 
                outside the box). What are outliers? They are values that fall outside the range of 1.5 times the IQR 
                (Q3 - Q1), meaning they are extreme values that can potentially skew our analysis. Check out the chart 
                below and learn how to deal with outliers:""", unsafe_allow_html=True)


    # tirando unknown para o gráfico fig6
    car_data_filtered = car_data[car_data['paint_color'] != 'unknown']

    # Remover outliers da coluna 'days_listed'
    Q1 = car_data['days_listed'].quantile(0.25)
    Q3 = car_data['days_listed'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    car_data_filtered2 = car_data_filtered[(car_data['days_listed'] >= lower_bound) & (car_data['days_listed'] <= upper_bound)]

    # ordem alfabetica no boxplot
    ordem_alfabetica = sorted(car_data_filtered2['brand'].unique())

    # Gráfico para comparar quantos dias cada marca demora para ser vendida (sem contar com os outliers)
    fig5 = px.box(car_data, x='brand', y='days_listed', color='brand',height=600,  labels={
                        'brand': 'Car Brand',  # Marca do carro
                        'days_listed': 'Days  Listed',  # Mediana dos dias listados
                        },
                        category_orders={'brand': ordem_alfabetica})
    fig5.update_layout(
        title={
            'text': 'How Many Days Does it Take For a Car of Each Brand to be Sold',
            'x': 0.5,  # Centraliza o título
            'xanchor': 'center'
        },
        title_font_size=24,  # Tamanho da fonte do título
        xaxis_title_font_size=18,  # Tamanho da fonte do título do eixo x
        xaxis_title='',  # Adiciona a legenda ao eixo y
        yaxis_title_font_size=18,  # Tamanho da fonte do título do eixo y
        legend_font_size=13.7,  # Tamanho da fonte da legenda
        legend_title_font_size=18, 
        
    )

    st.plotly_chart(fig5)
    
    st.markdown("---")

    st.header("Does it Really Take 271 Days to Sell a Chevrolet Car?")
    st.markdown("""If you look at the graph above, you’ll see that there is a Chevrolet 
                car that took 271 days to be sold. But is that normal? NO! The median time 
                for a car of this brand to be sold is 33 days, while the average rises to 39.6 
                days. In other words, values like this 271-day outlier skew the data analysis by 
                increasing the average value. When analyzing the graph below, you’ll notice that 
                the out-of-box points decreased considerably, indicating that the outliers were 
                removed. Check the y-axis, it changed from 250 to 100, which means there are no 
                longer values significantly above 100 days. If you hover over the points, you’ll 
                see that Chevrolet’s median dropped from 33 to 32 days, while the average decreased 
                from 39.6 to 36.6 days. This reveals two things: the average is more sensitive to 
                outliers than the median, and handling outliers is crucial in this case.
                """, unsafe_allow_html=True)

    # faça um gráfigo igual o do fig9, mas com o dataframe car_data_filtered2
    fig5_filtered = px.box(car_data_filtered2, x='brand', y='days_listed', color='brand',height=600,  labels={
                        'brand': 'Car Brand',  # Marca do carro
                        'days_listed': 'Days  Listed',  # Mediana dos dias listados
                        },
                        category_orders={'brand': ordem_alfabetica})

    fig5_filtered.update_layout(
        title={
            'text': 'How Many Days Does it Take For a Car of Each Brand to be Sold (without outliers)',
            'x': 0.5,  # Centraliza o título
            'xanchor': 'center'
        },
        title_font_size=24,  # Tamanho da fonte do título
        xaxis_title_font_size=18,  # Tamanho da fonte do título do eixo x
        xaxis_title='',  # Adiciona a legenda ao eixo y
        yaxis_title_font_size=18,  # Tamanho da fonte do título do eixo y
        legend_font_size=13.7,  # Tamanho da fonte da legenda
        legend_title_font_size=18, 
        
    )
    st.plotly_chart(fig5_filtered)

    st.markdown("""If you think that removing outliers is a bad practice that might distort the analysis, 
                keep in mind that only <strong>3.1%</strong> of the data was removed. So, just 3% of the data 
                inflated the average selling time by almost 10% (from 36.6 to 39.6 days), which negatively 
                impacts our analysis.""", unsafe_allow_html=True)

    st.markdown("""The code below demonstrates how to calculate the 
                percentage of outliers for each car brand:""", unsafe_allow_html=True)
    st.code("""q1 = car_data['days_listed'].quantile(0.25)
    q3 = car_data['days_listed'].quantile(0.75)
    iqr = q3 - q1

    outliers = car_data[(car_data['days_listed'] < (q1 - 1.5 * iqr)) | (car_data['days_listed'] > (q3 + 1.5 * iqr))]
    outliers['brand'].value_counts() / car_data['brand'].value_counts() * 100
    """)

    st.markdown("---")
