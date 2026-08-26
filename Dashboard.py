from datetime import datetime as dt
import json
from pathlib import Path
from typing import List
import pandas as pd
import streamlit as st

copd = pd.read_csv('COPD_PM2.5.csv', sep=',', parse_dates=[11], date_format="%Y/%m/%d")
copd_f = pd.read_csv('COPD_PM2.5_F.csv', sep=',', parse_dates=[9], date_format="%Y/%m/%d")

st.set_page_config(
    page_title="PM2.5 and hospitalisations in Chiang Mai",
    layout="wide",
    initial_sidebar_state="expanded")
st.write("# PM2.5 and hospitalisations in Chiang Mai")

st.scatter_chart(copd,
                 x="date",
                 y='count',
                 color='pm2_5')

st.bar_chart(copd,
                 x="pm2_5",
                 y='count',
                 color='pm2_5')

selected = st.selectbox(
    "Select a variable",
    options=['pm2_5_val', 'pm10', 'tempF'],
    index=1
)
st.scatter_chart(copd,
                 y=selected,
                 x='date',
                 color='blue')

selected2 = st.selectbox(
    "Select a variable",
    options=['humidity', 'tempF','ozone'],
    index=1
)
st.scatter_chart(copd,
                 x=selected2,
                 y='count',
                 color='blue')
