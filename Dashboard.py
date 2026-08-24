pip install plotly
from datetime import datetime as dt
import json
from pathlib import Path
from typing import List
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="PM2.5 and hospitalisations in Chiang Mai",
    layout="wide",
    initial_sidebar_state="expanded")

copd = pd.read_csv('COPD-PM2_5.csv', sep='comma')

st.write("### 5. Scatter Chart")
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=[1, 2, 3, 4, 5],
        y=[1, 3, 2, 5, 4]))
st.scatter_chart(copd,
                 x='date',
                 y='count',
                 color='pm2_5')
