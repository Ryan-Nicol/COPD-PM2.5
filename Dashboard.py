from datetime import datetime as dt
import json
from pathlib import Path
from typing import List
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="PM2.5 and hospitalisations in Chiang Mai",
    layout="wide",
    initial_sidebar_state="expanded")

copd = pd.read_csv('Full_data.csv', sep='comma')

st.write("### 5. Scatter Chart")
st.scatter_chart(copd,
                 x="date",
                 y='count',
                 color='pm2_5')
