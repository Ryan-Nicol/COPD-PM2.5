import pandas as pd
import streamlit as st

copd = pd.read_csv('COPD-PM2_5_processed.csv', sep=',', parse_dates=[11], date_format="%Y/%m/%d")
copd_f = pd.read_csv('COPD-PM2_5_F_processed.csv', sep=',', parse_dates=[0], date_format="%Y/%m/%d")

st.set_page_config(
    page_title="PM2.5 and hospitalisations in Chiang Mai",
    layout="wide",
    initial_sidebar_state="expanded")
st.write("# PM2.5 and hospitalisations in Chiang Mai")
st.markdown(''' :red[very low = 1-15ppm], :blue[low = 15.1-25ppm], :red[moderate = 25.1-37.5ppm],
            :blue[high = 37.6-75ppm], :green[very unsafe = 75.1-150ppm]''')


col1, col2 = st.columns([1,1])

col1.write("##### The number of forecasted hospitalisations over the next 6 days")
col1.line_chart(copd_f,
                 y='count',
                y_label='Count',
                 x='date',
                x_label='Date',
                 color='violet')

col2.write("##### The forecasted PM2.5 levels over the next 6 days")
col2.line_chart(copd_f,
                 y='pm2_5_y',
                y_label = 'PM2.5 levels',
                 x='date',
                x_label='Date',
                 color='violet')

st.write("##### The number of historical and forecasted hospitalisations between 2023-2025 and the next 6 days, coloured by PM2.5 level")
st.line_chart(copd,
                 x="date",
               x_label='Date',
                 y='count',
              y_label='Count',
                 color= 'pm2_5',
               width= 'stretch')

col3, col4 = st.columns([2,2])

col4.write("##### Interaction between both types of PM and the hospitalisation count")
selected = col4.selectbox(
        "Select a variable for the x axis",
        options=['pm2_5_val', 'pm10'],
        index=0
    )
col4.scatter_chart(copd,
                 x=selected,
                 y='count',
                   y_label='Count',
                 color='violet')

col3.write("##### Interaction between other environmental factors and the hospitalisation count")
selected2 = col3.selectbox(
        "Select a variable for the x axis",
        options=['tempF','humidity','ozone','carbon_monoxide','carbon_dioxide','sulphur_dioxide','nitrogen_dioxide'],
        index=0
    )
col3.scatter_chart(copd,
                 x=selected2,
                 y='count',
                   y_label='Count',
                 color='violet')

col3.write("##### The total number of historical and forecasted hospitalisations sorted by PM2.5 level")
col3.bar_chart(copd,
                 x="pm2_5",
               x_label='PM2.5 Categories',
                 y='count',
               y_label='Count',
                 color='pm2_5')

