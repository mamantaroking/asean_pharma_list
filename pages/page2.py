import dash
from dash import html, Dash, dcc, Output, Input, callback, State
import pandas as pd
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import plotly.express as px


dash.register_page(__name__)


# object definition for alternative row colors
getRowStyle = {
    "styleConditions": [
        {
            "condition": "params.rowIndex % 2 === 0",
            "style": {"backgroundColor": "whitesmoke", "color": "black"},
        },
    ]
}


# Load query of "Every data of the new registered products in the month of October
# from all national regulatory administration" for a table
with open('query_folder/new_table_query.txt', 'r') as file:
    new_table_query = file.read()
new_table_df = pd.read_sql(new_table_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')


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
    title="Products Registered in the Regulatory Administrations by Year")
bar.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})


layout = html.Div([
    html.Div(className='m-5 header_height'),
    html.Div([

        dbc.Row([
            dbc.Col([
                dbc.Breadcrumb(items=[{'label': 'New Products', 'href': '/', 'external_link': True}], itemClassName='center mitr-bigger'),
            ], width={'order': 'start'}, align='end', md=5),
            dbc.Col([
                html.A([
                    html.Img(id='header-logo', src=r'assets/dp_logo.png', alt='duopharma_logo', height='67px',
                             width='100px', className='center'),
                ], href='https://duopharmabiotech.com/about-duopharma-biotech/', target="_blank", className='center',
                    style={'width': '150px'}),
            ], width={'order': '2'}),
            dbc.Col([
                dbc.Breadcrumb(items=[{'label': 'All Products', 'active': True}], itemClassName='center mitr-bigger'),
            ], width={'order': 'last'}, align='end', md=5),
        ], className='fixed-top border shadow-sm dp_gradient p-1'
        ),

        html.Div([
            html.Div([
                'All Registered Products'
            ], className='p-3 rounded-top h2 border mitr-regular bg-white'
            ),
        ],),

        dbc.Row([
            dbc.Col([
                dbc.Stack([
                    html.Div([
                        dcc.Graph(figure=tree, style={'height': '237px'})
                    ], className='border bg-white rounded-3 shadow-sm'),
                    html.Div([
                        dcc.Graph(figure=bar, style={'height': '300px'})
                    ], className='border bg-white rounded-3 shadow-sm')
                ], gap=2)
            ], sm=3, className='ps-3'),
            dbc.Col([
                dbc.Stack([
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
                                ],
                                className="radio-group ms-2 my-1",
                            ),
                        ], sm=9, width={'order':'first'}),
                        dbc.Col([
                            dcc.Download(id='download-old'),
                            dbc.Button(["Download as .csv"],
                                       color="info",
                                       # className="d-flex justify-content-end",
                                       className='mx-1 my-1',
                                       id='btn-2',
                                       ),
                        ], sm=3, className='d-flex justify-content-end text-center', width={'order': 'last'}
                        ),
                    ]),
                    html.Div([
                        dag.AgGrid(
                            id='all_grid',
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
                            style={'height': '500px'},
                            className='ag-theme-balham'
                            # exportDataAsCsv=True,
                        )
                    ], className='mx-2'
                    ),
                ],  className='me-1 border bg-white rounded-3')
            ], sm=9, className=''),
        ]),
    ], className="dash_back border rounded-3 m-2 shadow"
    ),
])


@callback(
    Output("all_grid", "columnDefs",),
    Output("all_grid", "rowData"),
    [Input("new-radios", "value")]
)
def display_value(value):
    if value == 'new_all':
        call_query = "select * from test.all_product ap;"
        df = pd.read_sql(call_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        df_data = df.to_dict("records")
        columns = [{"field": i} for i in df.columns]
        return columns, df_data

    elif value == 'new_npra':
        call_query = "select * from test.npra;"
        df = pd.read_sql(call_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        df_data = df.to_dict("records")
        columns = [{"field": i} for i in df.columns]
        return columns, df_data

    elif value == 'new_hsa':
        call_query = "select * from test.hsa;"
        df = pd.read_sql(call_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        df_data = df.to_dict("records")
        columns = [{"field": i} for i in df.columns]
        return columns, df_data

    elif value == 'new_bpom':
        call_query = "select * from test.bpom;"
        df = pd.read_sql(call_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        df_data = df.to_dict("records")
        columns = [{"field": i} for i in df.columns]
        return columns, df_data

    elif value == 'new_ph_fda':
        call_query = "select * from test.ph_fda where classification = 'Prescription Drug (RX)';"
        df = pd.read_sql(call_query, 'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        df_data = df.to_dict("records")
        columns = [{"field": i} for i in df.columns]
        return columns, df_data


@callback(
    Output('download-old', 'data'),
    Input('btn-2', 'n_clicks'),
    State('new-radios', 'value'),
    prevent_initial_call=True
)
def download_btn(click, value):
    if value == 'new_all':
        call_query = "select * from test.all_product ap;"
        df = pd.read_sql(call_query,'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        return dcc.send_data_frame(df.to_csv, 'new_all.csv')

    elif value == 'new_npra':
        call_query = "select * from test.npra;"
        df = pd.read_sql(call_query,'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        return dcc.send_data_frame(df.to_csv, 'new_npra.csv')

    elif value == 'new_hsa':
        call_query = "select * from test.hsa;"
        df = pd.read_sql(call_query,'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        return dcc.send_data_frame(df.to_csv, 'new_hsa.csv')

    elif value == 'new_bpom':
        call_query = "select * from test.bpom';"
        df = pd.read_sql(call_query,'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        return dcc.send_data_frame(df.to_csv, 'new_bpom.csv')

    elif value == 'new_ph_fda':
        call_query = "select * from test.ph_fda;"
        df = pd.read_sql(call_query,'postgresql://dash_databse_postgres_user:UqrYMy14MaKSx4z65PkqtcpjRMXf1O6D@dpg-ct6hd7ilqhvc73aklbv0-a.singapore-postgres.render.com/trial1_aif8')
        return dcc.send_data_frame(df.to_csv, 'new_ph_fda.csv')

