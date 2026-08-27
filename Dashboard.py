import pandas as pd
import streamlit as st

copd = pd.read_csv('COPD_PM2.5.csv', sep=',', parse_dates=[11], date_format="%Y/%m/%d")
copd_f = pd.read_csv('COPD_PM2.5_F.csv', sep=',', parse_dates=[9], date_format="%Y/%m/%d")

st.set_page_config(
    page_title="PM2.5 and hospitalisations in Chiang Mai",
    layout="wide",
    initial_sidebar_state="expanded")
st.write("# PM2.5 and hospitalisations in Chiang Mai")

col1, col2 = st.columns([3,3])

selectedf = st.selectbox(
        "Select a variable for forecasted data",
        options=['pm10', 'pm2_5_y','carbon_monoxide','carbon_dioxide',
                                'nitrogen_dioxide','sulphur_dioxide','ozone','count'],
        index=1
    )
fig, ax1 = plt.subplots(figsize=(8, 8))
ax2 = ax1.twinx()

ax1.plot(copd_f, date, count)
ax2.plot(copd_f, date, pm2_5_y)


col1.line_chart(copd_f,
                 y=selectedf,
                 x='date',
                 color='blue')

col1.line_chart(copd,
                 x="date",
                 y='count',
                 color='pm2_5')
col2.bar_chart(copd,
                 x="pm2_5",
                 y='count',
                 color='pm2_5')
selected = st.selectbox(
        "Select a variable for x axis date",
        options=['pm2_5_val', 'pm10', 'tempF'],
        index=1
    )
col1.scatter_chart(copd,
                 y=selected,
                 x='date',
                 color='blue')
selected2 = st.selectbox(
        "Select a variable for y axis count",
        options=['humidity', 'tempF','ozone'],
        index=1
    )
col2.scatter_chart(copd,
                 x=selected2,
                 y='count',
                 color='blue')

