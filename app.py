import pandas as pd
import plotly.express as px
import streamlit as st
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import lxml
from main import introduction, data_analysis, tests

car_data = pd.read_csv('notebooks/car_data.csv')

if __name__ == '__main__':
   introduction()
   data_analysis(car_data)
   tests(car_data)
