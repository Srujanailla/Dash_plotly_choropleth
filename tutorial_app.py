from distutils.log import debug
import pandas as pd # to read and perform data manipulation
import plotly.graph_objects as go #for charts
import json # for working with json data
import requests #to sent http requests
import numpy as np # for working with matrices and arrays
import geopandas as gpd #to work with geospatial data
import plotly.express as px # uses graph objects and creates figures at once 

import dash #Main package which is the backbone one the app
from dash import html #provides html tags
import dash_bootstrap_components as dbc #adds bootstrap functionality to Dash - provides options related to layout
from dash import dcc #dcc stands for dash core components - provides interactive components
from dash.dependencies import Input, Output # used in the call back function to add interactivity

#Requesting the geojson file
geojson = "https://raw.githubusercontent.com/datameet/maps/master/parliamentary-constituencies/india_pc_2019_simplified.geojson"
url_request = requests.get(geojson)
json_file = url_request.json()

#Reading India's Parliamentary constituency shape file 
shape_file = gpd.read_file('india_pc_2019.shp')
shape_file['PC_NAME'] = [x.replace('(ST)', '') for x in shape_file['PC_NAME']]
shape_file['PC_NAME'] = [x.replace('(SC)', '') for x in shape_file['PC_NAME']]
shape_file['PC_NAME'] = [x.strip() for x in shape_file['PC_NAME']]
shape_file['PC_NAME'] = [x.capitalize() for x in shape_file['PC_NAME']]

states_unique = shape_file.ST_NAME.unique()

# Initializing the dash app with dark theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Defining the layout of the app - which is the frontend
app.layout = html.Div(children=[

    html.H1("Indian General Elections 2019"),
    dbc.Tabs([
              dbc.Tab([html.P("Lok Sabha is the lower house of the Indian national parliament where members are elected through an adult universal suffrage first-past-the-post voting system to the 543 single member parliamentary constituencies in India. LokSabha elections are held once in five years and members are called Members of Parliament (MP)."), 
              html.P("  In the Indian Political System, reservation is provided to historically disadvantaged groups to boost their representation. Some of the constituencies are reserved for only those candidates falling under a certain reservation category. For example, in the general elections, a Scheduled Caste (SC) or Scheduled Tribe (ST) candidate will be able to contest from a general seat. However, from a SC/ST reserved parliamentary constituency, only a SC/STC candidate can contest."), "Data Sources:", 
              html.Ul(html.A("  Creative Commons Attribution-ShareAlike2.5 India", href='https://github.com/datameet/maps/tree/master/parliamentary-constituencies'))], label='Introduction'),

              dbc.Tab([

                dcc.Dropdown(id='state_dropdown',value='UTTAR PRADESH',options=[{'label': state, 'value':str(state)} for state in states_unique]),
                dcc.Graph(id='PC_Reservation_Status')], label="Reservation Status"),
          
            ])
    

])  


@app.callback(Output('PC_Reservation_Status', 'figure'),
Input('state_dropdown', 'value'))

def PC_RES(state_name):
    color_discrete_map = {'virginica': 'rgb(255,0,0)', 'setosa': 'rgb(0,255,0)', 'versicolor': 'rgb(0,0,255)'}
    fig = px.choropleth(shape_file[shape_file['ST_NAME']==state_name],geojson=json_file, featureidkey="properties.pc_name", 
                    locations="PC_NAME", color='Res',
                    height=500,
                   color_continuous_scale="Viridis")
    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_layout(title_text=f'{state_name.capitalize()} Parliamentary Constituency Reservation Status', 
    coloraxis_colorbar=dict(ticktext=['General', 'Scheduled Caste', 'Scheduled']))
    fig.update(layout = dict(title=dict(x=0.5)))
    fig.update_layout(
    margin={"r":0,"t":30,"l":10,"b":10},
    coloraxis_colorbar={'title':'Sum'})

    return fig


    


#Running the app
if __name__ == '__main__':
    app.run_server(debug=True)    