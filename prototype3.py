from dash import Dash, Input, Output, State, dash_table, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
import psycopg2
import dash
import gunicorn
import sqlalchemy
import flask_sqlalchemy
import flask
import flask_caching


# Define external stylesheets
external_stylesheets = ["https://fonts.googleapis.com/css2?family=Passion+One:wght@400;700;900&display=swap",
                        dbc.themes.LITERA]

# ------------------------------------------------- App Initialization -------------------------------------------------
app = Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets)
server = app.server
# print(new_count_df.to_dict("records"))


# ----------------------------------------------------- App Layout -----------------------------------------------------
app.layout = html.Div([
    dash.page_container
], className='home_back')


if __name__ == '__main__':
    app.run(debug=True, port=8020)
