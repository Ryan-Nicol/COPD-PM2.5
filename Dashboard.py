import pandas as pd
import streamlit as st

copd = pd.read_csv('COPD_PM2.5.csv', sep=',', parse_dates=[11], date_format="%Y/%m/%d")
copd_f = pd.read_csv('COPD_PM2.5_F.csv', sep=',', parse_dates=[9], date_format="%Y/%m/%d")

st.set_page_config(
    page_title="PM2.5 and hospitalisations in Chiang Mai",
    layout="wide",
    initial_sidebar_state="expanded")
st.write("# PM2.5 and hospitalisations in Chiang Mai")
st.markdown(''' :red[very low = 1-15ppm], :blue[low = 15.1-25ppm], :red[moderate = 25.1-37.5ppm],
            :blue[high = 37.6-75ppm], :green[very unsafe = 75.1-150ppm]''')

copd[]

col1, col2 = st.columns([3,3])

col1.write("##### The number of forecasted hospitalisations over the next 6 days")
col1.line_chart(copd_f,
                 y='count',
                 x='date',
                 color='violet')

col2.write("##### The forecasted PM2.5 levels over the next 6 days")
col2.line_chart(copd_f,
                 y='pm2_5_y',
                y_label = 'PM2.5 levels',
                 x='date',
                 color='violet')

col1.line_chart(copd,
                 x="date",
                 y='count',
                 color= 'pm2_5')
col2.bar_chart(copd,
                 x="pm2_5",
                 y='count',
                 color='pm2_5')
selected = col1.selectbox(
        "Select a variable for the x axis",
        options=['pm2_5_val', 'pm10'],
        index=1
    )
col1.scatter_chart(copd,
                 x=selected,
                 y='count',
                 color='violet')
selected2 = col2.selectbox(
        "Select a variable for the x axis",
        options=['humidity', 'tempF','ozone'],
        index=1
    )
col2.scatter_chart(copd,
                 x=selected2,
                 y='count',
                 color='violet')

