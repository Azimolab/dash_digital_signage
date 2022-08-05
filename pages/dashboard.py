from asyncio import proactor_events
from re import X
from sqlite3 import dbapi2
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL, dash_table
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash_extensions.enrich import html, dcc, Output, Input, DashProxy
import dash
from dash import html, dcc, callback, Input, Output
from flask_caching import function_namespace
import pandas as pd
import plotly.express as px
from dash_svg import Svg, G, Path, Circle
from dash_extensions import WebSocket
from dash_bootstrap_templates import ThemeChangerAIO
from datetime import datetime, timedelta 
from datetime import datetime, date

from sqlalchemy import true
from components import channels

dash.register_page(__name__)

df = pd.read_csv('cartoes.csv')

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)


tab2_content = dbc.Card(
    dbc.Row([
        dbc.Col([
            html.Div(id="page-content5")
        ], md=12)
    ])
)

tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Tab 1", tab_id="tab-1"),
                dbc.Tab(label="Tab 2", tab_id="tab-2"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)

navbar = dbc.NavbarSimple(
    children=[
        dcc.Location(id="url"),
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Grupo de telas", header=True),
                dbc.DropdownMenuItem("Dados Gerais", href="#"),
                dbc.DropdownMenuItem("Ajuda", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="DIGITAL SIGNAGE",
    brand_href="#",
    color="#363740",
    dark=True,
)

def table (dados):
    df = pd.read_csv(dados)
    return  dash_table.DataTable(id="dash_neu", editable=True, row_deletable=True, columns=[
                                     {'name': i, 'id': i} for i in df.columns], data=df.to_dict('records')),


body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Label("Titulo"),
                dbc.Input(placeholder="Título do Slide", id="txt-despesa"),
                html.Div(id="divtable"),
                dbc.Col(html.Button('+', id='editing-rows-button', n_clicks=0)),
                dbc.Col(html.Button('update', id='btn-save', n_clicks=0)),
                html.H5("MyBudget", id="template",
                        className="text-primary"),
                html.H5("MyBudget", id="valor",
                        className="text-primary"),
                html.H5("MyBudget", id="db",
                        className="text-primary"),
            ]
        )])



modal=dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Adicionar Slide")),
                dbc.ModalBody([
                    dbc.Row([
                            dbc.Col([
                                html.Div([body])
                            ], width=3),
                            dbc.Col([
                                html.Div(id='app-container8')
                        ], width=9, style={})  
                    ]),           
#                    dbc.Row([                                                 
#                        dbc.ModalFooter([
#                            dbc.Button("Adicionar despesa", color="error", id="salvar_despesa", value="despesa"),
#                            dbc.Popover(dbc.PopoverBody("Despesa Salva"), target="salvar_despesa", placement="left", trigger="click"),
#                        ]
#                        )
#                    ], style={"margin-top": "25px"}),
                ], style={})
            ],
            style={"background-color": "rgba(17, 140, 79, 0.05)"},
            id="modal-novo-despesa",
            fullscreen=True,
            is_open=False,
            centered=True,
            backdrop=True)


layout = navbar,modal,dbc.Container(children=[tabs  
], fluid=True, style={"padding": "0px"}, className="dbc")


@callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return tab1_content
    elif at == "tab-2":
        return tab2_content
    return html.P("This shouldn't ever be displayed...")


@callback(Output("page-content5", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/" or pathname == "/dashboard":
        return channels.layout

    if pathname == "/extratos":

        return channels.layout


# Pop-up despesa
@callback(
    [Output("modal-novo-despesa", "is_open"),
    Output("txt-despesa", "placeholder"),
    Output("template", "children"),
    Output("valor", "children"),
    Output("db", "children"),
    Output('app-container8', 'children'),
    Output("divtable", "children")
    ],
    Input({'type': 'output-ex3', 'index': ALL}, 'n_clicks'),
    Input('store-receitas', 'data'),
    State("modal-novo-despesa", "is_open"), prevent_initial_call=True
)
def toggle_modal(n1, dataprev,is_open):
    ctx = dash.callback_context
    #changed_id = ctx.triggered[0]['prop_id'].split('.')[0]
    button_id = ctx.triggered_id if not None else 'No clicks yet'
    btid=(button_id.index).split("_")

    print(btid)
    print(button_id.index)

    print(n1)
    datapre = dataprev[0]
    if n1 is not None:
        db = pd.read_csv('db.csv')
        db2 = db[db['id_slide'] == btid[2]] 
        db2.reset_index(inplace=True)
        title = db2._get_value(0, 'title')
        template = db2._get_value(0, 'template')
        data = db2._get_value(0, 'data')
        filter = db2._get_value(0, 'filter')
        div_table = table (data)
        print(n1)
        print(title)
        is_open = True
        return [is_open,title,template,filter,data,datapre,div_table]


@callback(
    [Output("dash_neu", "data"),
    Output("dash_neu", "columns")],
    [Input("btn-save", "n_clicks"), 
    Input('editing-rows-button', 'n_clicks'),
    Input('db', 'children')],
    [State('dash_neu', 'data'), 
    State('dash_neu', 'columns')]
)
def update(button, clicked, dataframetemp, data, columns):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-save' in changed_id:
        df = pd.DataFrame(data)
        df.to_csv(dataframetemp, encoding='utf-8', index=False)
        columns = [{'name': i, 'id': i} for i in df.columns]
        data = df.to_dict('records')
        return data, columns
    if 'editing-rows-button' in changed_id:
        if clicked > 0:
             data.append({c['id']: '' for c in columns})
        return data, columns
    return data, columns
