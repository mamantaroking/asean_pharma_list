from dash import Dash, Input, Output, State, dash_table, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
import psycopg2
import gunicorn
import sqlalchemy
import flask_sqlalchemy
import flask
import flask_caching


# ------------------------------ (Optional) Psycopg2 PostgreSQL driver Database Connection -----------------------------
conn = psycopg2.connect(
    dbname='trial1_aif8',
    user='dash_databse_postgres_user',
    password='UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D',
    host='dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com',
    port='5432',
)


# Column Definitions for count of new product table
columnDefs = [
    {'headerName': 'Regulatory Administrations', 'field': 'regs_admins'},
    {'headerName': 'Number of New Registered Products', 'field': 'count'},
]


# object definition for alternative row colors
getRowStyle = {
    "styleConditions": [
        {
            "condition": "params.rowIndex % 2 === 0",
            "style": {"backgroundColor": "whitesmoke", "color": "black"},
        },
    ]
}


# ------------------------------ Load SQL query scripts into dataframes -----------------------------

# Load query of "Count of new registered products in each national regulatory administration" for a table
with open('query_folder/new_count_query.txt', 'r') as file:
    new_count_query = file.read()
new_count_df = pd.read_sql(new_count_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')


# Load query of "Every data of the new registered products in the month of October
# from all national regulatory administration" for a table
with open('query_folder/new_table_query.txt', 'r') as file:
    new_table_query = file.read()
new_table_df = pd.read_sql(new_table_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')


# Load "Count of new registered products in each national regulatory administration" for a pie chart
with open('query_folder/new_graph_query.txt', 'r') as file:
    new_graph_query = file.read()
new_graph_df = pd.read_sql(new_graph_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')


# Pie chart definition
pie = px.pie(new_graph_df, values='count', names='regs_admin',) #  title='New Registered Drugs')
pie.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)', 'height': 350, 'width': 550})


# Load query of "Count of all products in the database from each national regulatory administration" for a tree mao
with open('query_folder/tree_map_query.txt', 'r') as file:
    tree_map_query = file.read()
dfgraph = pd.read_sql_query(tree_map_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
dfcount = dfgraph['count'].tolist()
# print(dfcount)


# Tree map definition
tree = px.treemap(dfgraph, path=['region', 'regs_admin'], values='count', color='count', color_continuous_scale='RdBu',
                  title='Total Registered Products in the Database')
tree.update_traces(textinfo="label+value")
# fig.update_traces(root_color="lightgrey")
tree.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'}, margin=dict(t=50, l=25, r=25, b=25))
# tree = px.pie(dfgraph, values='count', names='regs_admin')


# Load query of "Count of all products in the database from each national regulatory admin ordered by year"
# for a bar chart
with open('query_folder/bar_chart_query.txt', 'r') as file:
    bar_chart_query = file.read()
bardf = pd.read_sql_query(bar_chart_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')

# Bar chart definition
bar = px.bar(
    bardf, x="year", y="count", color="table_name",
    title="Products Registered in the Regulatory Administrations by Year", barmode='group')
bar.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})


# Define external stylesheets
external_stylesheets = ["https://fonts.googleapis.com/css2?family=Passion+One:wght@400;700;900&display=swap",
                        dbc.themes.LITERA]

# ------------------------------------------------- App Initialization -------------------------------------------------
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
# print(new_count_df.to_dict("records"))


# ----------------------------------------------------- App Layout -----------------------------------------------------
app.layout = html.Div([
    html.Div([
        html.Div([
            html.A([
                html.Img(id='header-logo', src=r'assets/dp_logo.png', alt='duopharma_logo', height='67px', width='100px', className='center'),
            ], href='https://duopharmabiotech.com/about-duopharma-biotech/', target="_blank", className='center', style={'width': '150px'}),
        ], className='fixed-top border shadow-sm dp_gradient p-1'
        ),
        html.Div(className='m-5 header_height'),
        html.Div([
            dbc.Row([
                # dbc.Col(['NEW PRODUCTS REGISTERED IN OCTOBER 2024'],
                dbc.Col(['New Products Registered in October 2024'],
                        className='mx-5 my-4 border shadow text-center h2 py-4 rounded-3 mitr-regular', md=10, align='center',
                        style={
                            # 'font-family': 'Passion One',
                            # 'font-weight': 'bold',
                        }
                        ),
                dbc.Col(
                    [
                     dag.AgGrid(
                        rowData=new_count_df.to_dict("records"),
                        # columnDefs=[{"field": i} for i in new_count_df.columns],
                        columnDefs=columnDefs,
                        getRowStyle=getRowStyle,
                        dashGridOptions={
                            'rowSelection': 'single',
                            'pagination': False,
                            'animateRows': False,
                            "domLayout": "autoHeight",
                            "suppressColumnMoveAnimation": True,
                            "enableCellTextSelection": True
                        },
                        # columnSize='responsiveSizeToFit',
                        defaultColDef={"filter": False,
                                       "sortable": False,
                                       "floatingFilter": False,
                                       "resizable": False
                                       },
                        style={'height': '75%', 'width': '100%'},
                        # columnSize='sizeToFit'
                        columnSize='autoSize'
                        # exportDataAsCsv=True,
                     )],
                    md=5, className='m-5 px-4', align='center'
                ),
                dbc.Col(
                    [dcc.Graph(
                        figure=pie
                    )], md=5, className='mx-5 my-3 bg-light '
                )
            ], justify='center'
            ),
            # Button Group Definition for new products
            dbc.Row([
                dbc.Col([
                    html.Div(
                        [
                            dbc.RadioItems(
                                id="new-radios",
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-outline-primary",
                                labelCheckedClassName="active",
                                options=[
                                    {"label": "All New Products", "value": 'new_all'},
                                    {"label": "Malaysia NPRA", "value": 'new_npra'},
                                    {"label": "Singapore HSA", "value": 'new_hsa'},
                                    {"label": "Indonesia BPOM", "value": 'new_bpom'},
                                    {"label": "Philippines FDA", "value": 'new_ph_fda'}
                                ],
                                value='new_all',
                            ),
                            html.Div(id="output"),
                        ],
                        className="radio-group mt-5 ms-5 mb-2",
                    ),
                ], md=7
                ),
                dbc.Col([
                    dcc.Download(id='download-new'),
                    dbc.Button(["Download as .csv"],
                               color="info",
                               className="d-flex justify-content-end",
                               id='btn-1',
                               ),
                ], md=4, className='d-flex justify-content-end mt-5 ms-5 mb-2'
                ),
            ]),
            html.Div([
                dag.AgGrid(
                    id='new_grid',
                    rowData=new_table_df.to_dict("records"),
                    columnDefs=[{"field": i} for i in new_table_df.columns],
                    # columnDefs=columnDefs,
                    getRowStyle=getRowStyle,
                    dashGridOptions={
                        'rowSelection': 'single',
                        'pagination': True,
                        'animateRows': False,
                        "enableCellTextSelection": True
                    },
                    # columnSize='responsiveSizeToFit',
                    defaultColDef={"filter": True,
                                   "sortable": True,
                                   "floatingFilter": True,
                                   },
                    style={'height': '500px'}
                    # exportDataAsCsv=True,
                )
            ], className='mx-5 mb-5 shadow'
            ),
        ], className="m-5 bg-light border rounded-3"
        ),

        html.Hr(className='my-5'),

        html.Div([
            dbc.Row(['All Registered Products'],
                    className='mx-5 my-4 border shadow text-center h2 py-4 rounded-3 ', align='center', justify='center'
                    ),
            dbc.Row([
                dbc.Col([dcc.Graph(figure=tree)], md=5, className='m-4 bg-light'),
                dbc.Col([dcc.Graph(figure=bar)], md=6, className='m-4 bg-light')
            ], className='m-4 shadow-sm'
            ),

            html.Hr(className='my-5'),
            html.Div(['List of All Registered Products by Tables'],
                     className='mx-5 my-4 shadow-sm text-center h4 py-4 rounded-3 text-align-center'
                    ),
            html.Div([
                dbc.DropdownMenu(
                    [
                        dbc.DropdownMenuItem("All", id="dropdown-all", n_clicks=0),
                        dbc.DropdownMenuItem("Malaysia's NPRA", id="dropdown-npra", n_clicks=0),
                        dbc.DropdownMenuItem("Indonesia' BPOM", id="dropdown-bpom", n_clicks=0),
                        dbc.DropdownMenuItem("Singapore's HSA", id="dropdown-hsa", n_clicks=0),
                        dbc.DropdownMenuItem("Philippine's FDA", id="dropdown-ph_fda", n_clicks=0),
                    ],
                    label="Choose a Regulatory Administration...", className='m-2 d-flex justify-content-center', id='dropdown-dbc'
                    ),
                ], className='m-5'
            ),
            html.Div(id='place-container', className="m-5 shadow"),
        ], className='m-5 bg-light border rounded-3'
        ),


    ])
])


# --------------------------------------------------- App Callbacks ----------------------------------------------------

@app.callback(
    Output('place-container', 'children', allow_duplicate=True),
    Output('dropdown-dbc', 'label', allow_duplicate=True),
    Input('dropdown-all', 'n_clicks'), prevent_initial_call=True
)
def update_table_all(click):
    if click > 0:
        value = 'all_product'
        labelling = "All"
        df = pd.read_sql_table(value, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8', 'test')
        grid = dag.AgGrid(
            rowData=df.to_dict("records"),
            columnDefs=[{"field": i} for i in df.columns],
            # columnDefs=columnDefs,
            dashGridOptions={
                'rowSelection': 'single',
                'pagination': True,
                'animateRows': False,
                "enableCellTextSelection": True
            },
            # columnSize='responsiveSizeToFit',
            defaultColDef={"filter": True,
                           "sortable": True,
                           "floatingFilter": True,
                           },
            style={'height': '600px'}
            # exportDataAsCsv=True,
        ),
        return grid, labelling


@app.callback(
    Output('place-container', 'children', allow_duplicate=True),
    Output('dropdown-dbc', 'label', allow_duplicate=True),
    Input('dropdown-npra', 'n_clicks'), prevent_initial_call=True
)
def update_table_npra(click):
    if click > 0:
        value = 'npra'
        labelling = "Malaysia's NPRA"
        df = pd.read_sql_table(value, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8', 'test')
        grid = dag.AgGrid(
            rowData=df.to_dict("records"),
            columnDefs=[{"field": i} for i in df.columns],
            # columnDefs=columnDefs,
            dashGridOptions={
                'rowSelection': 'single',
                'pagination': True,
                'animateRows': False,
                "enableCellTextSelection": True
            },
            # columnSize='responsiveSizeToFit',
            defaultColDef={"filter": True,
                           "sortable": True,
                           "floatingFilter": True,
                           },
            style={'height': '600px'}
            # exportDataAsCsv=True,
        ),
        return grid, labelling


@app.callback(
    Output('place-container', 'children', allow_duplicate=True),
    Output('dropdown-dbc', 'label', allow_duplicate=True),
    Input('dropdown-bpom', 'n_clicks'), prevent_initial_call=True
)
def update_table_bpom(click):
    if click > 0:
        value = 'bpom'
        labelling = "Indonesia's BPOM"
        df = pd.read_sql_table(value, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8', 'test')
        grid = dag.AgGrid(
            rowData=df.to_dict("records"),
            columnDefs=[{"field": i} for i in df.columns],
            # columnDefs=columnDefs,
            dashGridOptions={
                'rowSelection': 'single',
                'pagination': True,
                'animateRows': False,
                "enableCellTextSelection": True
            },
            # columnSize='responsiveSizeToFit',
            defaultColDef={"filter": True,
                           "sortable": True,
                           "floatingFilter": True,
                           },
            style={'height': '600px'}
            # exportDataAsCsv=True,
        ),
        return grid, labelling


@app.callback(
    Output('place-container', 'children', allow_duplicate=True),
    Output('dropdown-dbc', 'label', allow_duplicate=True),
    Input('dropdown-hsa', 'n_clicks'), prevent_initial_call=True
)
def update_table_hsa(click):
    if click > 0:
        value = 'hsa'
        labelling = "Singapore's HSA"
        df = pd.read_sql_table(value, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8', 'test')
        grid = dag.AgGrid(
            rowData=df.to_dict("records"),
            columnDefs=[{"field": i} for i in df.columns],
            # columnDefs=columnDefs,
            dashGridOptions={
                'rowSelection': 'single',
                'pagination': True,
                'animateRows': False,
                "enableCellTextSelection": True
            },
            # columnSize='responsiveSizeToFit',
            defaultColDef={"filter": True,
                           "sortable": True,
                           "floatingFilter": True,
                           },
            style={'height': '600px'}
            # exportDataAsCsv=True,
        ),
        return grid, labelling


@app.callback(
    Output('place-container', 'children', allow_duplicate=True),
    Output('dropdown-dbc', 'label', allow_duplicate=True),
    Input('dropdown-ph_fda', 'n_clicks'), prevent_initial_call=True
)
def update_table_ph_fda(click):
    if click > 0:
        value = 'ph_fda'
        labelling = "Philippine's FDA"
        df = pd.read_sql_table(value, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8', 'test')
        grid = dag.AgGrid(
            rowData=df.to_dict("records"),
            columnDefs=[{"field": i} for i in df.columns],
            # columnDefs=columnDefs,
            dashGridOptions={
                'rowSelection': 'single',
                'pagination': True,
                'animateRows': False,
                "enableCellTextSelection": True
            },
            # columnSize='responsiveSizeToFit',
            defaultColDef={"filter": True,
                           "sortable": True,
                           "floatingFilter": True,
                           },
            style={'height': '600px'}
            # exportDataAsCsv=True,
        ),
        return grid, labelling


# callback for button group
@app.callback(
    Output("new_grid", "columnDefs"),
    Output("new_grid", "rowData"),
    [Input("new-radios", "value")])
def display_value(value):
    if value == 'new_all':
        call_query = "select * from test.all_product ap where date_of_issuance >= '2024-10-01' and date_of_issuance <= '2024-11-01';"
        df = pd.read_sql(call_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        df_data = df.to_dict("records")
        columns = [{"field": i} for i in df.columns]
        return columns, df_data

    elif value == 'new_npra':
        call_query = "select * from test.npra where date_of_issuance >= '2024-10-01' and date_of_issuance <= '2024-11-01';"
        df = pd.read_sql(call_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        df_data = df.to_dict("records")
        columns = [{"field": i} for i in df.columns]
        return columns, df_data

    elif value == 'new_hsa':
        call_query = "select * from test.hsa where date_of_issuance >= '2024-10-01' and date_of_issuance <= '2024-11-01';"
        df = pd.read_sql(call_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        df_data = df.to_dict("records")
        columns = [{"field": i} for i in df.columns]
        return columns, df_data

    elif value == 'new_bpom':
        call_query = "select * from test.bpom where date_of_issuance >= '2024-10-01' and date_of_issuance <= '2024-11-01';"
        df = pd.read_sql(call_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        df_data = df.to_dict("records")
        columns = [{"field": i} for i in df.columns]
        return columns, df_data

    elif value == 'new_ph_fda':
        call_query = "select * from test.ph_fda where date_of_issuance >= '2024-10-01' and date_of_issuance <= '2024-11-01' and classification = 'Prescription Drug (RX)';"
        df = pd.read_sql(call_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        df_data = df.to_dict("records")
        columns = [{"field": i} for i in df.columns]
        return columns, df_data


@app.callback(
    Output('download-new', 'data'),
    Input('btn-1', 'n_clicks'),
    State('new-radios', 'value'),
    prevent_initial_call=True
)
def download_btn(click, value):
    if value == 'new_all':
        call_query = "select * from test.all_product ap where date_of_issuance >= '2024-10-01' and date_of_issuance <= '2024-11-01';"
        df = pd.read_sql(call_query,'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        return dcc.send_data_frame(df.to_csv, 'new_all.csv')

    elif value == 'new_npra':
        call_query = "select * from test.npra where date_of_issuance >= '2024-10-01' and date_of_issuance <= '2024-11-01';"
        df = pd.read_sql(call_query,'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        return dcc.send_data_frame(df.to_csv, 'new_npra.csv')

    elif value == 'new_hsa':
        call_query = "select * from test.hsa where date_of_issuance >= '2024-10-01' and date_of_issuance <= '2024-11-01';"
        df = pd.read_sql(call_query,'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        return dcc.send_data_frame(df.to_csv, 'new_hsa.csv')

    elif value == 'new_bpom':
        call_query = "select * from test.bpom where date_of_issuance >= '2024-10-01' and date_of_issuance <= '2024-11-01';"
        df = pd.read_sql(call_query,'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        return dcc.send_data_frame(df.to_csv, 'new_bpom.csv')

    elif value == 'new_ph_fda':
        call_query = "select * from test.ph_fda where date_of_issuance >= '2024-10-01' and date_of_issuance <= '2024-11-01';"
        df = pd.read_sql(call_query,'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        return dcc.send_data_frame(df.to_csv, 'new_ph_fda.csv')


if __name__ == '__main__':
    app.run(debug=True, port=8018)