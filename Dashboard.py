from datetime import datetime as dt
import json
from pathlib import Path
from typing import List
import matplotlib.pyplot as plt
import openmeteo_requests

import requests_cache
from retry_requests import retry


import statsmodels.formula.api as smf
import statsmodels.api as sm

import pandas as pd
from pandas import DatetimeIndex
from requests import request

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback

import streamlit as st

import __main__ as main

import warnings
warnings.filterwarnings("ignore")


st.set_page_config(
    page_title="PM2.5 and hospitalisations in Chiang Mai",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

df_reshaped = pd.read_csv('COPD-PM2_5.csv')

