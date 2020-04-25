import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

us_loc = pd.read_csv("us-counties.csv", parse_dates=['date'], index_col=['date'])
us_loc.tail()

new_york = us_loc[us_loc["county"] == "New York City"]
new_york.tail()

# Line chart for all New York cases of COVID-19
# Figure and plotspace size
fig, ax = plt.subplots(figsize=(10, 5))
# x-axis and y-axis
ax.plot(new_york.index.values,
        new_york['cases'],
        color='purple')
# Title and labels for axes
ax.set(xlabel="Date",
       ylabel="Cases",
       title="Cases of COVID-19 in New York")
# Show the chart
plt.show()

# Creating the all new cases chart
new_york_new_cases = new_york['cases'] - new_york['cases'].shift()

# Line chart for all New York new cases of COVID-19
# Figure and plotspace size
fig, ax = plt.subplots(figsize=(10, 5))
# x-axis and y-axis
ax.plot(new_york_new_cases.index.values,
        new_york_new_cases,
        color='purple')
# Title and labels for axes
ax.set(xlabel="Date",
       ylabel="Cases",
       title="New Cases of COVID-19 in New York")
# Show the chart
plt.show()

# Filtering the last 10 days recorded in New York
last_ten_ny = new_york.tail(10)
last_ten_ny

# Line chart for last 10 days of COVID-19 recorded in New York
# Create figure and plot space
fig, ax = plt.subplots(figsize=(10, 5))
# x-axis and y-axis
ax.plot(last_ten_ny.index.values,
        last_ten_ny['cases'],
        color='purple')
# Title and labels for axes
ax.set(xlabel="Date",
       ylabel="Cases",
       title="Recent 10 Day All Recorded Cases of COVID-19 in New York")
# Show the chart
plt.show()

# Creating the last 10 days new cases chart
ny_top_ten_new_cases = last_ten_ny['cases'] - last_ten_ny['cases'].shift()

# Line chart for last 10 days of new COVID-19 cases recorded in New York
# Figure and plotspace size
fig, ax = plt.subplots(figsize=(10, 5))
# x-axis and y-axis
ax.plot(ny_top_ten_new_cases.index.values,
        ny_top_ten_new_cases,
        color='purple')
# Title and labels for axes
ax.set(xlabel="Date",
       ylabel="Cases",
       title="New Cases of COVID-19 in New York")
# Show the chart
plt.show()
