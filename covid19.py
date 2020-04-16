import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

us_loc = pd.read_csv("us-counties.csv", parse_dates=['date'],
                                index_col=['date'])
us_loc.tail()

new_york = us_loc[us_loc["county"] == "New York City"]
new_york.tail()

# Create figure and plot space
fig, ax = plt.subplots(figsize=(10, 10))
# Add x-axis and y-axis
ax.plot(new_york.index.values,
        new_york['cases'],
        color='purple')
# Set title and labels for axes
ax.set(xlabel="Date",
       ylabel="Cases",
       title="Cases of COVID-19 in New York")
plt.show()

last_ten_ny = new_york.tail(10)
last_ten_ny

# histogram for last 10 days in New York
# Create figure and plot space
fig, ax = plt.subplots(figsize=(10, 10))
# Add x-axis and y-axis
ax.plot(last_ten_ny.index.values,
        last_ten_ny['cases'],
        color='purple')
# Set title and labels for axes
ax.set(xlabel="Date",
       ylabel="Cases",
       title="Cases of COVID-19 in New York")
plt.show()
