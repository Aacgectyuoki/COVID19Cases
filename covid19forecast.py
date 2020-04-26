# fbprophet needs to be installed first
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet

file_source = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
us_loc = pd.read_csv(file_source, parse_dates=['date'], index_col=['date'])
us_loc.tail()

new_york = us_loc[us_loc["county"] == "New York City"]
new_york.tail()

# the dates will not become a index
df = new_york.reset_index()
from datetime import datetime
mask = (df['date'] > '2020-03-16')
df = df.loc[mask]
df=df.rename(columns={'date':'ds', 'cases':'y'})

# creating the predictions
m = Prophet(mcmc_samples=300)
m.fit(df)
future = m.make_future_dataframe(periods=36, freq='D')
forecast = Prophet(interval_width=0.95).fit(df).predict(future)
fig = m.plot_components(forecast)


# Creating the all new cases chart
new_york_new_cases = new_york['cases'] - new_york['cases'].shift()

# the dates will not become a index
df1 = new_york_new_cases.reset_index()
mask = (df1['date'] > '2020-03-16')
df1 = df1.loc[mask]
df1=df1.rename(columns={'date':'ds', 'cases':'y'})

# creating the predictions
m = Prophet(mcmc_samples=300)
m.fit(df1)
future = m.make_future_dataframe(periods=36, freq='D')
forecast = Prophet(interval_width=0.95).fit(df1).predict(future)
fig = m.plot_components(forecast)


# Filtering the last 10 days recorded in New York
last_ten_ny = new_york.tail(10)
last_ten_ny

# the dates will not become a index
df2 = last_ten_ny.reset_index()
df2=df2.rename(columns={'date':'ds', 'cases':'y'})

# creating the predictions
m = Prophet(mcmc_samples=300)
m.fit(df2)
future = m.make_future_dataframe(periods=36, freq='D')
forecast = Prophet(interval_width=0.95).fit(df2).predict(future)
fig = m.plot_components(forecast)


# Creating the last 10 days new cases chart
ny_top_ten_new_cases = last_ten_ny['cases'] - last_ten_ny['cases'].shift()

# the dates will not become a index
df3 = ny_top_ten_new_cases.reset_index()
df3=df3.rename(columns={'date':'ds', 'cases':'y'})

# creating the predictions
m = Prophet(mcmc_samples=300)
m.fit(df3)
future = m.make_future_dataframe(periods=36, freq='D')
forecast = Prophet(interval_width=0.95).fit(df3).predict(future)
fig = m.plot_components(forecast)
