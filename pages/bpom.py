import dash
from dash import html, Dash, dcc, Output, Input, callback, State
import pandas as pd
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

dash.register_page(__name__)

df = pd.read_csv('full_bpom2.csv')

columnDefs =[
    {'field': 'Column1'},
    {
        'field': 'Nomor Registrasi',
        'minWidth': 150,
        'tooltipField': 'Nomor Registrasi',
        'tooltipComponentParams': {'color': 'crimson'}
    },
    {'field': 'Tanggal Terbit'},
    {'field': 'Masa Berlaku S/d'},
    {'field': 'Diterbitkan Oleh (1)'},
    {'field': 'Diterbitkan Oleh (2)'},
    {'field': 'Produk'},
    {
        'field': 'Nama Produk',
        'minWidth': 150,
        'tooltipField': 'Nama Produk',
        'tooltipComponentParams': {'color': 'crimson'}
    },
    {'field': 'Bentuk Sediaan'},
    {'field': 'Komposisi'},
    {'field': 'Merk'},
    {'field': 'Kemasan'},
    {'field': 'Pendaftar'},
    {'field': 'Diproduksi Oleh'},
]

layout = html.Div([
    html.Hr(),
    # html.H1('There should be a BPOM table here'),
    dag.AgGrid(
        id="table-1",
        rowData=df.to_dict("records"),
        columnDefs=[{"field": i} for i in df.columns],
        # columnDefs=columnDefs,
        dashGridOptions={
            'rowSelection': 'single',
            'pagination': True,
            'animateRows': False,
        },
        # columnSize='responsiveSizeToFit',
        defaultColDef={"filter": True,
                       "sortable": True,
                       "floatingFilter": True,
                       },
        # exportDataAsCsv=True,
    ),
    dcc.Download(id='download-bpom'),
    dbc.Button("Download as .csv", color="primary", className="me-1", id='btn-1'),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Header")),
            dbc.ModalBody("This is the content of the modal", id='modal-body'),
            dbc.ModalFooter(
                dbc.Button("Close",
                           id="modal-close",
                           className="ms-auto",
                           n_clicks=0,
                           color='danger')
            ),
        ],
        id="row-select-modal",
        is_open=False,
    ),
])

@callback(
    Output('download-bpom', 'data', allow_duplicate=True),
    Input('btn-1', 'n_clicks'),
    prevent_initial_call=True
)
def download_btn(click):
    return dcc.send_data_frame(df.to_csv, 'bpom_df.csv')

'''@callback(
    Output("row-select-modal", "is_open"),
    [Input("table-1", "selectedRows"),
     Input("modal-close", "n_clicks")],
    [State("row-select-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_modal(n1, n2, is_open):
    if n1:
        return not is_open
        content_to_display = "You selected " + ", ".join(
            [
                f"{s['make']} (model {s['model']} and price {s['price']})"
                for s in selection
            ]
        )
    elif n2:
        return not is_open
    return is_open'''
