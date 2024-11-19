import dash
from dash import html, Dash, dcc, callback, Output, Input
import pandas as pd
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import plotly.express as px
import json

dash.register_page(__name__)


data = {'name': ['Sabah', 'Perlis', 'Kedah', 'Kelantan', 'Perak', 'Sarawak',
                 'Pulau Pinang', 'Selangor', 'Negeri Sembilan', 'Melaka', 'Johor',
                 'Pahang', 'Terengganu', 'Labuan', 'Kuala Lumpur', 'Putrajaya'],
        'Sales': [95, 50, 80, 43, 64, 70, 31, 74, 57, 45, 78, 69, 21, 12, 0o5, 66]
        }

df = pd.DataFrame(data)

geojson = json.load(open('malaysia_cloropeth_geojson.json'))

fig = px.choropleth(df, geojson=geojson, color="Sales",
                    locations="name", featureidkey="properties.name",
                    projection="mercator", range_color=(0, 100), color_continuous_scale=px.colors.sequential.ice)
fig.update_geos(fitbounds="locations", visible=True, showframe=True,
                showcoastlines=False, resolution=50, bgcolor='lightsteelblue',
                lonaxis_showgrid=True, lataxis_showgrid=True)
# fig.update_traces(showlegend=True)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


layout = html.Div([
    html.Hr(),
    html.Div([
        dcc.Graph(id='graph-1', figure=fig)
    ]
    ),
])
