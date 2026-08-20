#!/usr/bin/env python
# coding: utf-8

# In[107]:


pip show jupyter_core


# In[108]:


pip show jupyter_client


# In[110]:


pip show jupyterlab


# In[111]:


pip show notebook


# In[46]:


pip install plotly


# In[61]:


pip show plotly


# In[47]:


pip install openmeteo-requests


# In[2]:


pip show openmeteo-requests


# In[48]:


pip install requests-cache retry-requests


# In[6]:


pip show requests-cache retry-requests


# In[ ]:


pip install pandas scikit-learn


# In[108]:


pip show pandas scikit-learn


# In[4]:


pip install "dash[cloud]"


# In[74]:


pip show dash


# In[1]:


pip install streamlit


# In[160]:


pip show streamlit


# In[1]:


pip install jupytext


# In[155]:


from datetime import datetime as dt
import json
from pathlib import Path
from typing import List
import seaborn as sns
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


# In[2]:


pip show seaborn


# In[82]:


pip show statsmodels


# In[3]:


pip show matplotlib


# In[5]:


client_id = "jqtVbnB0bfi8PqPOhHcwQ"
client_secret = "QHoY9BO4K57P78WjhcsVhUkeZKG0vudDaGNVNLIW"

location_list = [
    "18.6951714,98.4462684"
]

request_fields = []


request_fields = [
    'periods.dateTimeISO',
    'place.name',
    'periods.tempF',
    'periods.humidity'
]


# In[6]:


dt_list = pd.date_range(start='2023-01-01', end='2025-12-31')
print(dt_list)


# In[7]:


def aeris_api_dataframe(location: str, custom_fields: List[str] = None, from_date: dt = None) -> pd.DataFrame:
    formatted_fields = []

    if custom_fields is not None:
        formatted_fields = ','.join(custom_fields)

    print(f"retrieving data for {location} on {from_date.strftime('%Y-%m-%d')}...")
    res = request(
        method="GET",
        url=f"https://api.aerisapi.com/conditions/{location}",
        params={
            "client_id": client_id,
            "client_secret": client_secret,
            "fields": formatted_fields,
            "from": from_date,
            "to": from_date.strftime('%Y-%m-%d')
        }
    )
    
    if res.status_code != 200:
        raise Exception(f"status code was not 200: {res.status_code}")
          
    api_response_body = json.loads(res.text)

    try:
        df_pre_period = pd.json_normalize(api_response_body['response'][0]).drop("periods", axis=1)
        df_periods = pd.json_normalize(api_response_body['response'][0], "periods", record_prefix="periods.")
        return df_pre_period.join(df_periods, how="cross")
    except IndexError:
        print(f"API Response did not contain periods. Verify request parameters are correct.\n\nRequest:\n{res.url}\n\nResponse:\n{api_response_body}")


# In[8]:


output_dir = Path('csv')
output_dir.mkdir(exist_ok=True)


# In[95]:


def loop_single(dt_list: DatetimeIndex):
    sorted_dates = dt_list.sort_values()
    filename = f"Chiang_Mai_Weather_hist.csv"
    all_locs = []
    for date in sorted_dates:
        for loc in location_list:
            all_locs.append(aeris_api_dataframe(location="18.6951714,98.4462684", custom_fields=request_fields, from_date=date))
        full_day_df = pd.concat(all_locs, ignore_index=True)
        full_day_df.to_csv(output_dir / filename, encoding="utf-8")
        print(f"csv for {date.strftime('%Y%m%d')}")
    print("all csv's complete!")

loop_single(dt_list)


# In[110]:


weather_data = pd.read_csv('csv/Chiang_Mai_Weather_hist.csv')
weather_data


# In[111]:


weather_slim = weather_data.drop(columns = ['Unnamed: 0', 'place.name'])


# In[112]:


weather_slim['periods.dateTimeISO'] = pd.to_datetime(weather_slim['periods.dateTimeISO']).dt.date


# In[113]:


weather_final = weather_slim.rename(columns={"periods.dateTimeISO": "date"})


# In[114]:


weather_final


# In[115]:


diag_data = pd.read_csv('csv/ChiangMai_HospitalVisits_COPD_2023-2025.csv')

diag_data


# In[116]:


diag_slim = diag_data.drop(columns = ['RACE', 'OCCUPATION_NEW', 'NATION', 'EDUCATION', 'FSTATUS', 'MOVEIN', 'LABOR', 'TYPEAREA','P_ADDRESS', 'BIRTH'])


# In[117]:


loc_data = pd.read_csv('csv/ChiangMai_Hospitals_Locations.csv')


# In[118]:


loc_slim = loc_data.drop(columns = 'HOSPCODE')


# In[119]:


hosp_data = pd.merge(diag_slim, loc_slim, how="right", on="DISTRICT")

hosp_data


# In[120]:


cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
	"latitude": 18.7904,
	"longitude": 98.9847,
	"hourly": ["pm10", "pm2_5", "carbon_monoxide", "carbon_dioxide", "nitrogen_dioxide", "sulphur_dioxide", "ozone"],
	"forecast_days": 6,
}
responses = openmeteo.weather_api(url, params = params)

response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

f_hourly = response.Hourly()
f_hourly_pm10 = f_hourly.Variables(0).ValuesAsNumpy()
f_hourly_pm2_5 = f_hourly.Variables(1).ValuesAsNumpy()
f_hourly_carbon_monoxide = f_hourly.Variables(2).ValuesAsNumpy()
f_hourly_carbon_dioxide = f_hourly.Variables(3).ValuesAsNumpy()
f_hourly_nitrogen_dioxide = f_hourly.Variables(4).ValuesAsNumpy()
f_hourly_sulphur_dioxide = f_hourly.Variables(5).ValuesAsNumpy()
f_hourly_ozone = f_hourly.Variables(6).ValuesAsNumpy()

f_hourly_data = {
	"date": pd.date_range(
		start = pd.to_datetime(f_hourly.Time(), unit = "s", utc = True),
		end =  pd.to_datetime(f_hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = f_hourly.Interval()),
		inclusive = "left"
	)
}

f_hourly_data["pm10"] = f_hourly_pm10
f_hourly_data["pm2_5"] = f_hourly_pm2_5
f_hourly_data["carbon_monoxide"] = f_hourly_carbon_monoxide
f_hourly_data["carbon_dioxide"] = f_hourly_carbon_dioxide
f_hourly_data["nitrogen_dioxide"] = f_hourly_nitrogen_dioxide
f_hourly_data["sulphur_dioxide"] = f_hourly_sulphur_dioxide
f_hourly_data["ozone"] = f_hourly_ozone

f_hourly_dataframe = pd.DataFrame(data = f_hourly_data)
print("\nF_Hourly data\n", f_hourly_dataframe)


# In[121]:


f_hourly_dataframe['date'] = pd.to_datetime(f_hourly_dataframe['date']).dt.date
f_hourly_dataframe


# In[122]:


f_daily_dataframe = f_hourly_dataframe.groupby(f_hourly_dataframe.date).mean()
f_daily_dataframe


# In[123]:


f_air = f_daily_dataframe['pm2_5']


# In[124]:


cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
	"latitude": 18.7904,
	"longitude": 98.9847,
	"hourly": ["pm10", "pm2_5", "carbon_monoxide", "carbon_dioxide", "sulphur_dioxide", "nitrogen_dioxide", "ozone", "methane"],
    "start_date": "2023-01-01",
	"end_date": "2025-12-31",
}
responses = openmeteo.weather_api(url, params = params)
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
hourly = response.Hourly()
hourly_pm10 = hourly.Variables(0).ValuesAsNumpy()
hourly_pm2_5 = hourly.Variables(1).ValuesAsNumpy()
hourly_carbon_monoxide = hourly.Variables(2).ValuesAsNumpy()
hourly_carbon_dioxide = hourly.Variables(3).ValuesAsNumpy()
hourly_sulphur_dioxide = hourly.Variables(4).ValuesAsNumpy()
hourly_nitrogen_dioxide = hourly.Variables(5).ValuesAsNumpy()
hourly_ozone = hourly.Variables(6).ValuesAsNumpy()

hourly_data = {
	"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)
}

hourly_data["pm10"] = hourly_pm10
hourly_data["pm2_5"] = hourly_pm2_5
hourly_data["carbon_monoxide"] = hourly_carbon_monoxide
hourly_data["carbon_dioxide"] = hourly_carbon_dioxide
hourly_data["sulphur_dioxide"] = hourly_sulphur_dioxide
hourly_data["nitrogen_dioxide"] = hourly_nitrogen_dioxide
hourly_data["ozone"] = hourly_ozone

hourly_dataframe = pd.DataFrame(data = hourly_data)
print("\nHourly data\n", hourly_dataframe)


# In[125]:


hourly_dataframe['date'] = pd.to_datetime(hourly_dataframe['date']).dt.date
hourly_dataframe


# In[126]:


daily_dataframe = hourly_dataframe.groupby(hourly_dataframe.date).mean()
daily_dataframe


# In[127]:


weather_slim


# In[128]:


env_data = pd.merge(weather_final, daily_dataframe, how="right", on="date")

env_data


# In[129]:


env_final = env_data.rename(columns={"date": "DIAGDATE"})


# In[130]:


env_final


# In[131]:


full_data = pd.merge(hosp_data, env_final.astype(str), on='DIAGDATE', how='left')
full_data


# In[132]:


pat_num = full_data.value_counts('DIAGDATE')
pat_num = pd.DataFrame(pat_num)
pat_num


# In[133]:


full_data2 = pd.merge(full_data, pat_num, on= 'DIAGDATE')
full_data2


# In[134]:


full_data2.dtypes


# In[135]:


full_data2["pm2_5"]=full_data2["pm2_5"].astype(float)
full_data2["pm10"]=full_data2["pm10"].astype(float)
full_data2["periods.tempF"]=full_data2["periods.tempF"].astype(float)
full_data2["periods.humidity"]=full_data2["periods.humidity"].astype(float)
full_data2["carbon_monoxide"]=full_data2["carbon_monoxide"].astype(float)
full_data2["carbon_dioxide"]=full_data2["carbon_dioxide"].astype(float)
full_data2["sulphur_dioxide"]=full_data2["sulphur_dioxide"].astype(float)
full_data2["nitrogen_dioxide"]=full_data2["nitrogen_dioxide"].astype(float)
full_data2["ozone"]=full_data2["ozone"].astype(float)


# In[136]:


full_data2 = full_data2.groupby('DIAGDATE').mean(numeric_only=True)
full_data2 = full_data2.reset_index()
full_data2


# In[137]:


full_data2=full_data2.rename(columns={"periods.tempF": "periods_tempF"})
full_data2=full_data2.rename(columns={"periods.humidity": "periods_humidity"})


# In[138]:


pm_full_d = full_data2.drop(columns = ['DIAGDATE'])


# In[139]:


corr_matrix = pm_full_d.corr()
plt.figure(figsize=(11,9))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap")
plt.show()


# In[140]:


full_data2.dtypes


# In[141]:


full_data2[['carbon_dioxide','AGE_Y']]=full_data2[['carbon_dioxide','AGE_Y']].fillna(full_data2[['carbon_dioxide','AGE_Y']].mean())
full_data2


# In[142]:


air = full_data2['pm2_5']


# In[143]:


full_data2['pm2_5'] = pd.cut(full_data2['pm2_5'], bins=[0, 15, 25, 37.5, 75, 150], labels=['very low', 'low', 'moderate', 'high','very unsafe'])


# In[144]:


f_daily_dataframe["pm2_5"]=f_daily_dataframe["pm2_5"].astype(float)
f_daily_dataframe['pm2_5'] = pd.cut(f_daily_dataframe['pm2_5'], bins=[0, 15, 25, 37.5, 75, 150], labels=['very low', 'low', 'moderate', 'high','very unsafe'])


# In[145]:


full_cat = full_data2


# In[146]:


full_cat.isnull().any()


# In[147]:


split_date = '2024-12-31'

df_training = full_cat.loc[full_cat['DIAGDATE'] <= split_date]
df_test = full_cat.loc[full_cat['DIAGDATE'] > split_date]


# In[148]:


X_training = df_training.iloc[:, 0:-1] 
y_training = df_training.loc[:, 'count']


# In[149]:


X_test = df_test.iloc[:, 0:-1] 
y_test = df_test.loc[:, 'count']  


# In[150]:


model_logistic_simple = smf.glm(
    'count ~ pm2_5', 
    data = full_cat,
    family = sm.families.Gaussian()
).fit()

model_logistic_simple.summary()


# In[151]:


model_logistic = smf.glm(
    'count ~ pm2_5+carbon_monoxide+carbon_dioxide+sulphur_dioxide+nitrogen_dioxide+ozone', 
    data = full_cat,
    family = sm.families.Gaussian()
).fit()

model_logistic.summary()


# In[54]:


model_logistic.predict(X_test)


# In[55]:


predictions = pd.DataFrame({'Actual': y_test, 'Predicted': model_logistic.predict(X_test)})
print(predictions.head())


# In[57]:


mae = mean_absolute_error(y_test, model_logistic.predict(X_test))
mse = mean_squared_error(y_test, model_logistic.predict(X_test))
r2 = r2_score(y_test, model_logistic.predict(X_test))

print("Mean Absolute Error (MAE):", mae)
print("Mean Squared Error (MSE):", mse)
print("R-squared Score:", r2)


# In[58]:


predictions = pd.DataFrame({'Actual': y_test, 'Predicted': model_logistic_simple.predict(X_test)})
print(predictions.head())


# In[60]:


mae_simple = mean_absolute_error(y_test, model_logistic_simple.predict(X_test))
mse_simple = mean_squared_error(y_test, model_logistic_simple.predict(X_test))
r2_simple = r2_score(y_test, model_logistic_simple.predict(X_test))

print("Mean Absolute Error (MAE):", mae_simple)
print("Mean Squared Error (MSE):", mse_simple)
print("R-squared Score:", r2_simple)


# In[62]:


f_count = model_logistic.predict(f_daily_dataframe)
f_count = f_count.to_frame('count')
f_count


# In[63]:


f_daily_dataframe


# In[64]:


forecast = pd.merge(f_daily_dataframe, f_count, how='left',on='date')
forecast


# In[65]:


full_cat = full_cat.assign(Index=range(len(full_cat))).set_index('DIAGDATE')
full_cat


# In[79]:


full_forecast = pd.concat([full_cat,forecast])
full_forecast.drop(columns = ['HOSPCODE','PID','SEX','AGE_Y','lat','long','periods_tempF','Index'])


# In[80]:


full_forecast.rename_axis(index=None, columns = 'DIAGDATE')


# In[99]:


air2 = pd.concat([air,f_air])
air2


# In[100]:


full_forecast['pm2_5_val'] = air2.values


# In[103]:


full_forecast['date'] = full_forecast.index


# In[104]:


full_forecast


# In[105]:


fig1 = px.scatter(full_forecast, x='date', y= 'count', color = 'pm2_5')
fig1.show()


# In[ ]:




