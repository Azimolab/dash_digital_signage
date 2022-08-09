from asyncio import proactor_events
from imaplib import Internaldate2tuple
from re import X
import json
from sqlite3 import dbapi2
from termios import NL1
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL, ALLSMALLER, dash_table
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
from dash.exceptions import PreventUpdate

from sqlalchemy import true
from components import channels

dash.register_page(__name__)

df = pd.read_csv('cartoes.csv')

df_db = pd.read_csv('db.csv')
df_db_aux = df_db.to_dict()

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
        dcc.Store(id='store_db_aux', data=df_db_aux),
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
    
    tables = dash_table.DataTable(id="modal_table1", editable=True, row_deletable=True, columns=[
                                           {'name': i, 'id': i} for i in df.columns], data=df.to_dict('records')),
    return  tables

def getData():
    return pd.read_csv().to_dict('records')

def getData2():
    return pd.read_csv().to_dict('records')
    
def back_to_df(dictio):
    return pd.DataFrame.from_dict(dictio)

#tblcols  =[{"name": i, "id": i} for i in back_to_df(getData()).columns]
#tblcols2 =[{"name": i, "id": i} for i in back_to_df(getData2()).columns]




body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Label("Titulo"),
                dbc.Input(placeholder="Título do Slide", id="slide_title"),
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
                dbc.ModalHeader(dbc.ModalTitle("Slide X")),
                dbc.ModalBody([
                    dbc.Row([
                            dbc.Col([
                                html.Div([body])
                            ], width=3),
                            dbc.Col([
                                html.Div(id='slide_preview')
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
            id="modal_editor",
            fullscreen=True,
            is_open=False,
            centered=True,
            backdrop=True)


layout = navbar,modal,dbc.Container(children=[
    tabs  
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

 #   if pathname == "/extratos":

 #       return channels.layout


# Pop-up despesa



@callback(
    [Output("modal_editor", "is_open"),
    Output("slide_title", "placeholder"),
    Output("template", "children"),
    Output("valor", "children"),
    Output("db", "children"),
    Output('slide_preview', 'children'),
    Output("divtable", "children")],
    Input({'type': 'btn_edit_card_slide', 'id': ALL}, 'n_clicks'),
    Input('store-receitas', 'data'),Input('store-receitas2', 'data'),
    State("modal_editor", "is_open")
)
def toggle_modal(n1, store_receitas,store_receitas2,is_open):

    ctx = dash.callback_context
    #button_dict = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    button_id = ctx.triggered_id if not None else 'No clicks yet'

    if n1:
        if n1[0]!=None:
            btn_id = button_id['id']
            btn_split = btn_id.split("_")

            db = pd.read_csv('db.csv')
            db2 = db[db['id_slide'] == btn_split[2]] 
            db2.reset_index(inplace=True)
            TEMPLATE = db2._get_value(0, 'template')
            POSITION = db2._get_value(0, 'position')-1

            if TEMPLATE == 1:
                    datapre = store_receitas[POSITION]
            if TEMPLATE == 2:
                    datapre = store_receitas2[POSITION]

            title = db2._get_value(0, 'title')
            template = db2._get_value(0, 'template')
            data = db2._get_value(0, 'data')
            filter = db2._get_value(0, 'filter')
            div_table = table (data)
            print(n1)
            print(title)
            print(btn_split[2])
            is_open = True
            return [is_open,title,template,filter,data,datapre,div_table]
    print(n1)
    return is_open









'''

@callback(
    [Output("store_db_aux", "data")],
    Input({'type': 'btn_delete_card_slide', 'index': ALL}, 'n_clicks'),
    State("store_db_aux", "data")
)
def toggle_modal2(n1,store_db_aux):
    ctx = dash.callback_context
    button_id = ctx.triggered_id if not None else 'No clicks yet'
    store_db_aux2 = store_db_aux

    input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    
    if "index" in input_id: 
        print(button_id)
        print(n1)
    else:
        print("No clicks yet")
    return [store_db_aux2]


     

    #if n1:
    #    if clicked > 0:

    #import pdb
    #pdb.set_trace()
    
'''


'''

@callback(
    [Output("modal_editor", "is_open"),
    Output("slide_title", "placeholder"),
    Output("template", "children"),
    Output("valor", "children"),
    Output("db", "children"),
    Output('slide_preview', 'children'),
    Output("divtable", "children")],
    Input({'type': 'btn_edit_card_slide', 'index': ALL}, 'n_clicks'), 
    prevent_initial_call=True
)
def toggle_modal(n1, store_receitas,store_receitas2,is_open,update_btn):
    ctx = dash.callback_context
    #changed_id = ctx.triggered[0]['prop_id'].split('.')[0]
    button_id = ctx.triggered_id if not None else 'No clicks yet'
    btid=(button_id.index)

    print(button_id)
    db = pd.read_csv('db.csv')
    db2 = db[db['id_slide'] == button_id] #recupera o id do botao
    db2.reset_index(inplace=True)

    print(n1)

    if n1:
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

'''
'''
@callback(
    [Output("modal_table1", "data"),
    Output("modal_table1", "columns")],
    [Input("btn-save", "n_clicks"), 
    Input('editing-rows-button', 'n_clicks'),
    Input('db', 'children')],
    [State('modal_table1', 'data'), 
    State('modal_table1', 'columns')]
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
'''


    #if n1:
    #    if clicked > 0:

    #import pdb
    #pdb.set_trace()
    

