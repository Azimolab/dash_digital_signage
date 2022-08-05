from distutils.command.sdist import sdist
import dash_bootstrap_components as dbc
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


def render_card_slide(id_slide, position, title):
    ID = id_slide
    ID_BTN_EDI_SLIDE = ("btn_e_" + ID)
    ID_BTN_DEL_SLIDE = ("btn_d_" + ID)
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
                                 "V", color="success", id={'type': 'btn_edit_card_slide','index': ID_BTN_EDI_SLIDE}
                             ),
                             dbc.Button(
                                 "X", color="danger", id={'type': 'btn_delete_card_slide','index': ID_BTN_DEL_SLIDE}
                             ),
                        ]
                    ),
                ], color="light", outline=True, id=ID)
            ],width=3, style={"padding": "5px"})          



def render_channel_cards(x):
    my_list = []
    db = pd.read_csv('db.csv')
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


layout = html.Div([
    dcc.Store(id='store-canais', data=channel1),
    dbc.Row([
            dbc.Col([
                    dbc.CardGroup(id='app-container6')
                    ], width=10),
            dbc.Col([
                    dbc.Label("Identificação: "),
                    dbc.Input(placeholder="channel 1", id="txt-receita"),
                    dbc.Button(color="success", id="add_slide1",
                            children=["add Slide"])
                    ], width=2),
            ], style={"margin": "10px"}
        ),
    dbc.Row([
            dbc.Col([
                    dbc.CardGroup(id='app-container7')
                    ], width=10),
            dbc.Col([
                    dbc.Label("Identificação: "),
                    dbc.Input(placeholder="channel 2", id="txt-receita2"),
                    dbc.Button(color="success", id="open-novo-despesa",
                            children=["add Slide"])
                    ], width=2),
            ], style={"margin": "10px"}
        )       
])

@callback([Output('app-container6', 'children'),
           Output('app-container7', 'children')],
          [Input('store-canais', 'data')])
def updaterowchannels (data):
    SD = render_channel_cards(1)
    SD2 = render_channel_cards(2)
    return [SD, SD2]


