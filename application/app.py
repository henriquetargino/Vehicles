import pandas as pd
import plotly.express as px
import streamlit as st
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import lxml
from streamlit_option_menu import option_menu
from main import introduction, data_analysis, tests

# layout da página
st.set_page_config(
    page_title="Vehicles Dataframe",
    page_icon="🚗",
    layout="wide", 
    initial_sidebar_state="expanded",
    menu_items={  # tres pontinhos
        'Get Help': 'mailto:henriquetarginoalbuquerque@gmail.com',
        'Report a bug': 'mailto:henriquetarginoalbuquerque@gmail.com',
        'About': """This web application is designed to provide an interactive and insightful 
        analysis of vehicle data. Built using Streamlit, Plotly Express, and Pandas, it allows 
        users to explore various aspects of car sales data through dynamic visualizations and 
        statistical analyses. The app covers a range of topics, including price distribution by brand, 
        car type distribution, fuel type analysis, and sales performance metrics. Additionally, it offers 
        tools for downloading the dataset and performing advanced statistical tests like ANOVA and Tukey's HSD. 
        Whether you're a car enthusiast, data analyst, or just curious about vehicle trends, this app provides 
        a comprehensive platform for exploring and understanding car sales data."""
    }
)

# CSS personalizado
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

car_data = pd.read_csv('notebooks/datasets/car_data.csv')

# Menu de navegação na barra lateral usando streamlit-option-menu
with st.sidebar:
    page = option_menu(
        "Menu",
        ["Introduction", "Data Analysis", "Tests", "I.A. Model"],
        icons=["database", "bar-chart", "clipboard-check", "robot"],
        menu_icon="cast",
        default_index=0,

    )

# Exibir a página selecionada
if page == "Introduction":
    introduction()
elif page == "Data Analysis":
    data_analysis(car_data)
elif page == "Tests":
    tests(car_data) 
elif page == "I.A. Model":
    model(car_data) 
