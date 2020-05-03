import numpy as np
import pandas as pd
# install folium before importing it
import folium

data = pd.read_csv("../input/us-counties-covid-19-dataset/us-counties.csv")


# measuring the total cases of US states as of April 25th, 2020
# Green = More total cases; Yellow = Less total cases
april25 = data[data["date"] == "2020-04-25"]
april25 = april25.groupby(['state'])['cases'].sum()
april25 = april25.reset_index()

url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
state_geo = f'{url}/us-states.json'

m = folium.Map(location=[48, -102], zoom_start=3)

folium.Choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=april25,
    columns=['state', 'cases'],
    key_on='feature.properties.name',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='COVID19',
).add_to(m)

folium.LayerControl().add_to(m)

# Prints out the map
m


# measuring the total cases of states other than New York as of April 25th, 2020
# Green = More total cases; Yellow = Less total cases
april25_wo_ny = april25[april25.state != 'New York']

m = folium.Map(location=[48, -102], zoom_start=3)

folium.Choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=april25_wo_ny,
    columns=['state', 'cases'],
    key_on='feature.properties.name',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='COVID19',
).add_to(m)

folium.LayerControl().add_to(m)

# Prints out the map
m

# Result:
# New York is shaded out, which means it is not included in this map. 
# Therefore, the greener the state is, the more total cases it has as of April 25th, 2020.
