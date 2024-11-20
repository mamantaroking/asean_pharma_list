import dash
from dash import html, Dash, dcc, callback, Output, Input
import pandas as pd
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import plotly.express as px
import json

dash.register_page(__name__)


data = {'States': ['Sabah', 'Perlis', 'Kedah', 'Kelantan', 'Perak', 'Sarawak',
                 'Pulau Pinang', 'Selangor', 'Negeri Sembilan', 'Melaka', 'Johor',
                 'Pahang', 'Terengganu', 'Labuan', 'Kuala Lumpur', 'Putrajaya'],
        'Sales Values': [849684, 565425, 907854, 438645, 646845, 709482, 318131, 771655, 578645, 425581, 784745, 698152,
                         218413, 128421, 58465, 662444],
        'Sales Units': [40652, 15258, 80842, 10328, 20485, 59831, 9461, 67417, 38513, 15846, 76641, 51046,
                        8813, 7461, 5682, 29513],
        }

button_group = html.Div(
    [
        dbc.RadioItems(
            id="radio-btn",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "Sales Values", "value": 'Sales Values'},
                {"label": "Sales Units", "value": 'Sales Units'},
            ],
            value='Sales Values',
        ),
        # html.Div(id="output"),
    ],
    className="radio-group",
)

df = pd.DataFrame(data)

geojson = json.load(open('malaysia_cloropeth_geojson.json'))


# layout = html.Div([
#     html.Hr(),
#    html.Div([
#         button_group,
#         dcc.Graph(id='graph-1')
#     ]
#     ),
# ])

app.layout = dbc.Container([
    html.Hr(),
    html.Div([button_group], className='mb-3'),
    dbc.Row(
        [
            dbc.Col([dcc.Graph(id='graph-1')], md=6),
            dbc.Col(id='table-map', md=6),
        ]),
])


@callback(
    Output("graph-1", "figure"),
    Output('table-map', 'children'),
    Input("radio-btn", "value"),
)
def change_column(value):
    fig = px.choropleth(df, geojson=geojson, color=value,
                        locations="States", featureidkey="properties.name",
                        projection="mercator", color_continuous_scale=px.colors.sequential.ice)

    fig.update_geos(fitbounds="locations", visible=True, showframe=True,
                    showcoastlines=False, resolution=50, bgcolor='lightsteelblue',
                    lonaxis_showgrid=True, lataxis_showgrid=True)

    # fig.update_traces(showlegend=True)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=500)

    grid = dag.AgGrid(
        rowData=df[['States', value]].to_dict("records"),
        # columnDefs=[{"field": i} for i in df.columns],
        columnDefs=[
            {'headerName': 'States', 'field': 'States'},
            {'headerName': value, 'field': value}],
        dashGridOptions={
            'rowSelection': 'single',
            # 'pagination': True,
            # 'animateRows': False,
        },
        # columnSize='responsiveSizeToFit',
        defaultColDef={"filter": True,
                       "sortable": True,
                       "floatingFilter": True,
                       },
        style={"height": 500, "width": 400}
        # exportDataAsCsv=True,
    ),

    return fig, grid
