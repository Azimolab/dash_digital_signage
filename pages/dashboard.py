import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL, ALLSMALLER, dash_table, callback
from dash.dependencies import Input, Output, State
from dash_extensions.enrich import html, dcc, Output, Input, DashProxy
import dash
import pandas as pd
from components import channels

dash.register_page(__name__,path='/')

df = pd.read_csv('cartoes.csv')
df_aux = df.to_dict()

df_db = pd.read_csv('db.csv')
df_db_aux = df_db.to_dict()

tab1_content = dbc.Card(
    dbc.CardBody(
        [

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
                dbc.Tab(label="GRUPO DE TELAS", tab_id="tab-1"),
                dbc.Tab(label="CANAIS", tab_id="tab-2"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)

navbar = dbc.NavbarSimple(
    children=[
        dcc.Store(id='store_db_aux'),
        dcc.Store(id='store-canais'),
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

def render_table (dados):
    df = pd.read_csv(dados)
    #df = pd.read_csv('cartoes.csv')
    df = pd.DataFrame(df).sort_values(by='data', ascending=False)
    tables = dash_table.DataTable(id="modal_table1", editable=True, row_deletable=True ,page_size=10, 
                                    columns=[{'name': i, 'id': i} for i in df.columns], 
                                    data=df.to_dict('records'),
                                    style_cell_conditional=[
                                            {'if': {'column_id': 'unidade',},
                                            'display': 'None',}],
                                    sort_action='native',
                                )
    return  tables

def table2 (x):
    db = pd.read_csv('db.csv')
    db2 = db[db['id_slide'] == x] 
    #df = pd.read_csv('cartoes.csv')
    tables = dash_table.DataTable(id="modal_table2", editable=True, row_deletable=False ,page_size=10,
                                    columns=[{'name': i, 'id': i} for i in db2.columns], 
                                    data=db2.to_dict('records'),
                                    style_cell_conditional=[
                                            {'if': {'column_id': 'group',},
                                            'display': 'None',},
                                            {'if': {'column_id': 'channel',},
                                            'display': 'None',},
                                            {'if': {'column_id': 'id_slide',},
                                            'display': 'None',},
                                            {'if': {'column_id': 'position',},
                                            'display': 'None',},
                                            {'if': {'column_id': 'data',},
                                            'display': 'None',},
                                            {'if': {'column_id': 'value1',},
                                            'display': 'None',},
                                            {'if': {'column_id': 'value2',},
                                            'display': 'None',},
                                            {'if': {'column_id': 'value3',},
                                            'display': 'None',},
                                            {'if': {'column_id': 'template',},
                                            'display': 'None',}
                                            
                                            ]
                                )
    return  tables




body = dbc.Container(
    [
        dbc.Col(
            [
                dbc.Row([
                        dbc.Label("Campos de texto"),
                        html.Div(id='divtable2'),  # id=divtable2
                        ], style={"padding-bottom": "20px"}),
                dbc.Row([
                    
                        dbc.Col([
                            dbc.Button('Add Nova linha', id='editing-rows-button', color="success", className="me-1", n_clicks=0),
                            dbc.Button('Salvar', id='btn-save', color="success", className="me-1", n_clicks=0)
                                ])
                        ]),
                dbc.Row([
                    html.Div(id="divtable")
                ], style={"padding-bottom": "20px","padding-top": "20px"}),

            ]
        )])



modal=dbc.Modal([
                dbc.ModalHeader([ 
                        dbc.Col([
                                dbc.Label("Identificação do Slide"),
                                html.H5("asdas", id="slide_title")
                        ], width=2, style={"padding-left": "25px"}), 
                        dbc.Col([
                                dbc.Label("Template"),
                                html.H5("asdas", id="template")
                        ], width=2, style={"padding-left": "15px"}),
                        dbc.Col([
                                dbc.Label("Base de Dados"),
                                html.H5("asdas", id="db")
                        ], width=2, style={"padding-left": "15px"}),
                        dbc.Col([
                                dbc.Label("id"),
                                html.H5("asdas", id="id")
                        ], width=2, style={"padding-left": "15px"}),
                        dbc.Col([
                                dbc.Label("Filtro"),
                                html.H5("asdas", id="valor")
                        ], width=2, style={"padding-left": "15px"})
                ]),
                dbc.ModalBody([
                    dbc.Row([
                            dbc.Col([
                                html.Div([body])
                            ], width=3),
                            dbc.Col([
                                html.Div(id='slide_preview')
                        ], width=9)  
                    ]),           
                ])
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
def render_tab_content(pathname):
    if pathname == "/" or pathname == "/dashboard":
        return channels.layout

 #   if pathname == "/extratos":

 #       return channels.layout


# Pop-up despesa



@callback(
    [Output("modal_editor", "is_open"),
    Output("slide_title", "children"),
    Output("id", "children"),
    Output("template", "children"),
    Output("valor", "children"),
    Output("db", "children"),
    Output('divtable', 'children'),
    Output('divtable2', 'children')],
    Input({'type': 'btn_edit_card_slide', 'id': ALL}, 'n_clicks'),
    State("modal_editor", "is_open")
)
def toggle_modal(n1, is_open):

    ctx = dash.callback_context
    #button_dict = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    button_id = ctx.triggered_id if not None else 'No clicks yet'

    if n1:
        if n1:
            btn_id = button_id['id']
            btn_split = btn_id.split("_")
            db = pd.read_csv('db.csv')
            db2 = db[db['id_slide'] == btn_split[2]] 
            db2.reset_index(inplace=True)
            id_slide = db2._get_value(0, 'id_slide')
            title = db2._get_value(0, 'title')
            template = db2._get_value(0, 'template')
            data = db2._get_value(0, 'data')
            filter = db2._get_value(0, 'filter')
            div_table = render_table (data)
            div_table2 = table2 (id_slide)
            print(div_table2)
            print(title)
            print(btn_split[2])
            is_open = True
            return [is_open,title,id_slide,template,filter,data,div_table,div_table2]
    print(n1)
    return is_open




#ATUALIZACAO TABELA DINAMICA
@callback(
    [Output("modal_table1", "data"),
    Output("modal_table1", "columns"),
    Output('store_render_new_layout', 'data')],
    [Input("btn-save", "n_clicks"), 
    Input('editing-rows-button', 'n_clicks'),
    Input("db", "children")],
    [State('modal_table1', 'data'), 
    State('modal_table1', 'columns')]
)
def update_modal_table_and_preview(button, clicked,db,table_data,columns):
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #print (changed_id)
    store_update_new_layout = [changed_id]

    if 'btn-save' in changed_id:  
        #grava novos dados da tabela
        df = pd.DataFrame(table_data)
        df.to_csv(db, encoding='utf-8', index=False)
        #Retorna nova tabela
        columns = [{'name': i, 'id': i} for i in df.columns]
        table_data = df.to_dict('records')
        store_update_new_layout = [changed_id]
        return table_data, columns,store_update_new_layout

    if 'editing-rows-button' in changed_id:
        if clicked > 0:              
             data2=({c['id']: '' for c in columns})
             table_data.insert(0,data2)
             #print(table_data)
             #table_data.append({c['id']: '' for c in columns})

        return table_data, columns,store_update_new_layout
    return table_data, columns,store_update_new_layout


#UPDATE PARA PREVIEW LAYOUT
@callback(
    [Output("slide_preview", "children"),
    Output("store_update_new_layout", "data")],
    [Input('cache_layout_c1', 'children'),
    Input('cache_layout_c2', 'children'),
    Input('cache_layout_c3', 'children'),
    Input("id", "children")],
    State('store_render_new_layout', 'data'),
    State("slide_preview", "children"),
    State("store_layouts_c1", "data"),
    State("store_layouts_c2", "data"),
    State("store_layouts_c3", "data")
)
def toggle_modal2(cache_layout_c1,cache_layout_c2,cache_layout_c3,slide_id,cache_layout_Y2,state,state2,state3,state1):
    datapre=[]
    print ("callcack update grafico")
    db = pd.read_csv('db.csv')
    db2 = db[db['id_slide'] == slide_id] 
    db2.reset_index(inplace=True)
    TEMPLATE = db2._get_value(0, 'template')
    POSITION = db2._get_value(0, 'position')-1
    print (slide_id)

    if TEMPLATE == 1:
            datapre = cache_layout_c1[slide_id]
    elif TEMPLATE == 2:
            datapre = cache_layout_c2[slide_id]
    elif TEMPLATE == 3:
            datapre = cache_layout_c3[slide_id]


    #print (cache_layout_c1)

    return datapre, datapre

