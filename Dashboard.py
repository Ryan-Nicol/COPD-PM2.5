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

df_reshaped = pd.read_csv('COPD-PM2_5.csv')

