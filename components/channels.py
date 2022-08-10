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


def render_card_slide(id_slide, position, title):
    ID_BTN_EDI_SLIDE = ("btn_e_" + id_slide)
    ID_BTN_DEL_SLIDE = ("btn_d_" + id_slide)
    ID_CONTAINER = (id_slide)
    ID_DOWNLOAD = ("download_" + id_slide)
    POSITION = position
    TITLE = title

    return dbc.Col([
                dcc.Download(id=ID_DOWNLOAD),
                dbc.Card([
                    dbc.CardHeader(TITLE),
                    dbc.CardBody(
                        [
                            html.P(
                                 POSITION,
                                 className="card-text",
                             ),
                             dbc.Button(
                                 "V", color="success", id={'type': 'btn_edit_card_slide','id': ID_BTN_EDI_SLIDE}
                             ),
                             dbc.Button(
                                 "X", color="danger", id={'type': 'btn_delete_card_slide','id': ID_BTN_DEL_SLIDE}
                             ),
                        ]
                    ),
                ], color="light", outline=True, id=ID_CONTAINER)
            ],width=3, style={"padding": "5px"})          



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

#store_canais = [{'props': {'children': [{'props': {'id': 'download_s1111'}, 'type': 'Download', 'namespace': 'dash_core_components'}, {'props': {'children': [{'props': {'children': 'CARTÕES'}, 'type': 'CardHeader', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': [{'props': {'children': 1, 'className': 'card-text'}, 'type': 'P', 'namespace': 'dash_html_components'}, {'props': {'children': 'V', 'id': {'type': 'btn_edit_card_slide', 'id': 'btn_e_s1111'}, 'color': 'success'}, 'type': 'Button', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': 'X', 'id': {'type': 'btn_delete_card_slide', 'id': 'btn_d_s1111'}, 'color': 'danger'}, 'type': 'Button', 'namespace': 'dash_bootstrap_components'}]}, 'type': 'CardBody', 'namespace': 'dash_bootstrap_components'}], 'id': 'container_s1111', 'color': 'light', 'outline': True}, 'type': 'Card', 'namespace': 'dash_bootstrap_components'}], 'style': {'padding': '5px'}, 'width': 3}, 'type': 'Col', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': [{'props': {'id': 'download_s1131'}, 'type': 'Download', 'namespace': 'dash_core_components'}, {'props': {'children': [{'props': {'children': 'CARTÕES PJ'}, 'type': 'CardHeader', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': [{'props': {'children': 3, 'className': 'card-text'}, 'type': 'P', 'namespace': 'dash_html_components'}, {'props': {'children': 'V', 'id': {'type': 'btn_edit_card_slide', 'id': 'btn_e_s1131'}, 'color': 'success'}, 'type': 'Button', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': 'X', 'id': {'type': 'btn_delete_card_slide', 'id': 'btn_d_s1131'}, 'color': 'danger'}, 'type': 'Button', 'namespace': 'dash_bootstrap_components'}]}, 'type': 'CardBody', 'namespace': 'dash_bootstrap_components'}], 'id': 'container_s1131', 'color': 'light', 'outline': True}, 'type': 'Card', 'namespace': 'dash_bootstrap_components'}], 'style': {'padding': '5px'}, 'width': 3}, 'type': 'Col', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': [{'props': {'id': 'download_s1141'}, 'type': 'Download', 'namespace': 'dash_core_components'}, {'props': {'children': [{'props': {'children': 'ACORDOS PJ'}, 'type': 'CardHeader', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': [{'props': {'children': 4, 'className': 'card-text'}, 'type': 'P', 'namespace': 'dash_html_components'}, {'props': {'children': 'V', 'id': {'type': 'btn_edit_card_slide', 'id': 'btn_e_s1141'}, 'color': 'success'}, 'type': 'Button', 'namespace': 'dash_bootstrap_components'}, {'props': {'children': 'X', 'id': {'type': 'btn_delete_card_slide', 'id': 'btn_d_s1141'}, 'color': 'danger'}, 'type': 'Button', 'namespace': 'dash_bootstrap_components'}]}, 'type': 'CardBody', 'namespace': 'dash_bootstrap_components'}], 'id': 'container_s1141', 'color': 'light', 'outline': True}, 'type': 'Card', 'namespace': 'dash_bootstrap_components'}], 'style': {'padding': '5px'}, 'width': 3}, 'type': 'Col', 'namespace': 'dash_bootstrap_components'}]


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
    def delete_children(n_clicks, id):
     
        print(id)
        df_db = pd.read_csv('db.csv')
        df_db = df_db.set_index("id_slide")
        df_db = df_db.drop(id)
        df_db.to_csv("db.csv")
        return None
