import dash
from dash import html, Dash, dcc, Output, Input, callback
import pandas as pd
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

dash.register_page(__name__)

df = pd.read_csv('ph_full.csv')

layout = html.Div([
    html.Hr(),
    # html.H1('There should be a BPOM table here'),
    dag.AgGrid(
        id="table-1",
        rowData=df.to_dict("records"),
        columnDefs=[{"field": i} for i in df.columns],
        dashGridOptions={
            'rowSelection': 'single',
            'pagination': True,
            'animateRows': False},
        # columnSize='responsiveSizeToFit',
        defaultColDef={"filter": True,
                       "sortable": True,
                       "floatingFilter": True},
        # exportDataAsCsv=True,
    ),
    dcc.Download(id='download-phfda'),
    dbc.Button("Download as .csv", color="primary", className="me-1", id='btn-1'),
])

@callback(
    Output('download-phfda', 'data'),
    Input('btn-1', 'n_clicks'),
    prevent_initial_call=True
)
def download_btn(click):
    return dcc.send_data_frame(df.to_csv, 'phfda_df.csv')