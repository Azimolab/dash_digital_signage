from distutils.command.sdist import sdist
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State, ALL
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


card = dbc.Card(
    [
        dbc.CardImg(
            src="/static/images/placeholder286x180.png",
            top=True,
            style={"opacity": 0.3},
        ),
        dbc.CardImgOverlay(
            dbc.CardBody(
                [
                    html.H4("Card title", className="card-title"),
                    html.P(
                        "An example of using an image in the background of "
                        "a card.",
                        className="card-text",
                    ),
                    dbc.Button("Go somewhere", color="primary"),
                ],
            ),
        ),
    ],
    style={"width": "18rem"},
)


def render_card_slide(id_slide, position, title):
    ID_BTN_EDI_SLIDE = ("btn_e_" + id_slide)
    ID_BTN_DEL_SLIDE = ("btn_d_" + id_slide)
    ID_CONTAINER = (id_slide)
    ID_DOWNLOAD = ("download_" + id_slide)
    POSITION = position
    TITLE = title

    return dbc.Col([
                dbc.Card([
                    dbc.CardHeader(TITLE),
                    dbc.CardBody(
                        [
                            html.P(
                                 POSITION,
                                 className="card-text",
                             ),
                             dbc.Button(
                                 "Editar", outline=True, color="success", className="me-1", id={'type': 'btn_edit_card_slide','id': ID_BTN_EDI_SLIDE}
                             ),
                             dbc.Button(
                                 "Deletar", outline=True, color="warning", className="me-1", id={'type': 'btn_delete_card_slide','id': ID_BTN_DEL_SLIDE}
                             ),
                        ]
                    ),
                ], color="light", outline=True, id=ID_CONTAINER, style={"justify":"center", "align":"center"})
            ],width=3, style={"padding": "5px"})          

def render_card_slide2():

    return dbc.Col([
                dbc.Card([
                    dbc.CardHeader('IDENTIFICAÇÃO'),
                    dbc.CardBody(
                        [
                            html.P(
                                 'Chanal 1',
                                 className="card-text",
                             ),
                             dbc.Button(
                                 "Novo Slide", outline=True, color="success", className="me-1"
                             )
                        ]
                    ),
                ], color="light", outline=True)
            ],width=2, style={"padding": "5px"})          


def render_channel_cards(x):
    my_list = []
    db = pd.read_csv('db.csv', index_col=0)
    db2 = db[db['channel'] == x] 
    #db2 = db.loc[db['channel'] == 1]  
    db2.reset_index(inplace=True)
    db2.info
    db4= len(db2.index)
    for i in range(db4):
        id_slide = db2._get_value(i, 'id_slide')
        position = db2._get_value(i, 'position')
        title = db2._get_value(i, 'title')
        Layout1 = render_card_slide(id_slide,position,title) 
        my_list.append(Layout1) 
    return my_list

channel1 = render_channel_cards(1)
channel2 = render_channel_cards(2)
channel3 = render_channel_cards(3)
channel4 = render_channel_cards(4)

#store_canais = [{'props': {'children': [{'props': {'id': 'download_s1111'}, 'type': 'Download', 'namespace': 'dash_core_components'}, {'props': {'children': [{'props': {'children': 'CARTÕES'}, 'type': 'CardHeader', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': [{'props': {'children': 1, 'className': 'card-text'}, 'type': 'P', 'namespace': 'dash_html_components'}, {'props': {'children': 'V', 'id': {'type': 'btn_edit_card_slide', 'id': 'btn_e_s1111'}, 'color': 'success'}, 'type': 'Button', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': 'X', 'id': {'type': 'btn_delete_card_slide', 'id': 'btn_d_s1111'}, 'color': 'danger'}, 'type': 'Button', 'namespace': 'dash_bootstrap_components'}]}, 'type': 'CardBody', 'namespace': 'dash_bootstrap_components'}], 'id': 'container_s1111', 'color': 'light', 'outline': True}, 'type': 'Card', 'namespace': 'dash_bootstrap_components'}], 'style': {'padding': '5px'}, 'width': 3}, 'type': 'Col', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': [{'props': {'id': 'download_s1131'}, 'type': 'Download', 'namespace': 'dash_core_components'}, {'props': {'children': [{'props': {'children': 'CARTÕES PJ'}, 'type': 'CardHeader', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': [{'props': {'children': 3, 'className': 'card-text'}, 'type': 'P', 'namespace': 'dash_html_components'}, {'props': {'children': 'V', 'id': {'type': 'btn_edit_card_slide', 'id': 'btn_e_s1131'}, 'color': 'success'}, 'type': 'Button', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': 'X', 'id': {'type': 'btn_delete_card_slide', 'id': 'btn_d_s1131'}, 'color': 'danger'}, 'type': 'Button', 'namespace': 'dash_bootstrap_components'}]}, 'type': 'CardBody', 'namespace': 'dash_bootstrap_components'}], 'id': 'container_s1131', 'color': 'light', 'outline': True}, 'type': 'Card', 'namespace': 'dash_bootstrap_components'}], 'style': {'padding': '5px'}, 'width': 3}, 'type': 'Col', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': [{'props': {'id': 'download_s1141'}, 'type': 'Download', 'namespace': 'dash_core_components'}, {'props': {'children': [{'props': {'children': 'ACORDOS PJ'}, 'type': 'CardHeader', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': [{'props': {'children': 4, 'className': 'card-text'}, 'type': 'P', 'namespace': 'dash_html_components'}, {'props': {'children': 'V', 'id': {'type': 'btn_edit_card_slide', 'id': 'btn_e_s1141'}, 'color': 'success'}, 'type': 'Button', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': 'X', 'id': {'type': 'btn_delete_card_slide', 'id': 'btn_d_s1141'}, 'color': 'danger'}, 'type': 'Button', 'namespace': 'dash_bootstrap_components'}]}, 'type': 'CardBody', 'namespace': 'dash_bootstrap_components'}], 'id': 'container_s1141', 'color': 'light', 'outline': True}, 'type': 'Card', 'namespace': 'dash_bootstrap_components'}], 'style': {'padding': '5px'}, 'width': 3}, 'type': 'Col', 'namespace': 'dash_bootstrap_components'}]


layout = html.Div([
    dbc.Row([
            dbc.Col([
                    dbc.CardGroup(channel1, id='app-container6')
                    ], width=10),
            (render_card_slide2()),
            ], style={"margin": "10px"}
        ),
    dbc.Row([
            dbc.Col([
                    dbc.CardGroup(channel2, id='app-container7')
                    ], width=10),
            (render_card_slide2()),
            ], style={"margin": "10px"}
        ),
         dbc.Row([
            dbc.Col([
                    dbc.CardGroup(channel3, id='app-container8')
                    ], width=10),
            (render_card_slide2())
                    ,
            ], style={"margin": "10px"}
        ),
         dbc.Row([
            dbc.Col([
                    dbc.CardGroup(channel4, id='app-container9')
                    ], width=10),
            (render_card_slide2())
                    ,
            ], style={"margin": "10px"}
        )                         
])

@callback([Output('app-container6', 'children'),
           Output('app-container7', 'children'),
           Output('app-container8', 'children'),
           Output('app-container9', 'children')],
          [Input('store-canais', 'data')])
def update_row_channels (data):
    SD = render_channel_cards(1)
    SD2 = render_channel_cards(2)
    SD3 = render_channel_cards(3)
    SD4 = render_channel_cards(4)
    return [SD,SD2,SD3,SD4]


db = pd.read_csv('db.csv')
id_list = db['id_slide'].tolist()
size = (len(id_list))-1


for i in range(size):

    n = id_list[i]

    @callback(
        Output(f"{n}", "children"),
        Input({"type": "btn_delete_card_slide", "id": f"btn_d_{n}"}, "n_clicks"),
        State(f"{n}", "id"),
        prevent_initial_call=True,
    )
    def delete_children_card(n_clicks, id):
     
        print(id)
        #df_db = pd.read_csv('db.csv')
        #df_db = df_db.set_index("id_slide")
        #df_db = df_db.drop(id)
        #df_db.to_csv("db.csv")
        return None
