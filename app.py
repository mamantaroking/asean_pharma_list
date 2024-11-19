from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import dash_ag_grid as dag
import plotly.express as px
import dash

df = pd.read_csv('full_bpom2.csv')

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LITERA])
server = app.server

nav_contents = [
    dbc.NavItem(dbc.NavLink("All", href="/all", disabled=True)),
    dbc.NavItem(dbc.NavLink("NPRA", href="/npra", active='exact')),
    dbc.NavItem(dbc.NavLink("HSA", href="/hsa", active='exact')),
    dbc.NavItem(dbc.NavLink("PH FDA", href="/ph", active='exact')),
    dbc.NavItem(dbc.NavLink("BPOM", href="/bpom", active='exact')),
    dbc.NavItem(dbc.NavLink("Vietnam FDA", href="#", disabled=True)),
]
# nav = dbc.Nav(nav_contents, pills=True, justified=True)

app.layout = dbc.Container(
    html.Div([
        # html.Div(id="my-title", children="Us Agricultural Exports in 2011"),
        html.H1(
            children='List of Registered Products',
            id='title',
            style={'font-size': '48px',
                   'font-family': 'verdana',
                   'font-weight': 'bold',
                   'text-align': 'center',
                   'color': 'white',
                   'background-color': 'crimson',
                   'height': '100px',
                   'padding': '20px'}
        ),
        html.H2(
            children="Indonesia's BPOM",
            id='subtitle',
            style={'font-size': '24px',
                   'font-family': 'verdana',
                   'text-align': 'center'}
        ),
        html.Hr(),
        html.Div([
            dbc.Nav(nav_contents, pills=True, justified=False)
            ]),
        dash.page_container
    ]),
)

if __name__ == '__main__':
    app.run(debug=True, port=8011)
