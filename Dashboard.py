from datetime import datetime as dt
import json
from pathlib import Path
from typing import List
import pandas as pd
import streamlit as st

copd = pd.read_csv('COPD_PM2.5.csv', sep=',')
copd.date.apply(lambda x: x.strftime('%Y%m%d')).astype(int)

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
    options=['pm2_5_val', 'pm10', 'count'],
    index=1
)
st.scatter_chart(copd,
                 x=selected,
                 y='date',
                 color='blue')
copd
