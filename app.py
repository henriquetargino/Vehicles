import pandas as pd
import plotly.express as px
import streamlit as st
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import lxml
from main import app

if __name__ == '__main__':
   app()