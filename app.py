#from re import I
#from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
import dash
import json
#from sqlalchemy import true
from dash_extensions import WebSocket
from dash_extensions.enrich import html, dcc, Output, Input, DashProxy
import pandas as pd
import plotly.express as px
from regex import X
from templates import template1, template2

estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", "https://fonts.googleapis.com/icon?family=Material+Icons", dbc.themes.LITERA, dbc.icons.BOOTSTRAP]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"


app = Dash(__name__, use_pages=True ,external_stylesheets=estilos + [dbc_css])
app.config['suppress_callback_exceptions'] = True
app.scripts.config.serve_locally = True
server = app.server


def gerar_slides(x):
    my_list = []
    db = pd.read_csv('db.csv')
    db2 = db[db['canal'] == x] 
    #db2 = db.loc[db['canal'] == 1]  
    db2.reset_index(inplace=True)
    db2.info
    db4= len(db2.index)
    for i in range(db4):
        id_slide = db2._get_value(i, 'id_slide')
        grupo = db2._get_value(i, 'grupo')
        canal = db2._get_value(i, 'canal')
        posicao = db2._get_value(i, 'posicao')
        titulo = db2._get_value(i, 'titulo')
        template = db2._get_value(i, 'template')
        data = db2._get_value(i, 'data')
        filtro = db2._get_value(i, 'filtro')

        if template == 1:
            Layout1 = template1.gerar_template_1(grupo,canal,posicao,titulo,template,data,filtro) 
            my_list.append(Layout1) 
        if template == 2:
            Layout2 = template2.gerar_template_2(grupo,canal,posicao,titulo,template,data,filtro) 
            my_list.append(Layout2) 
        
    return my_list

APP_LAYOUTS2 = gerar_slides(2)

APP_LAYOUTS = gerar_slides(1)

app.layout = html.Div([
    html.Div(
        [
            html.Div(
            )
        ]
    ),
    dcc.Store(id='store-receitas', data=APP_LAYOUTS),
    dcc.Store(id='store-receitas2', data=APP_LAYOUTS2),
    dcc.Interval(
        id='interval-componenty',
        interval=10000,  # in milliseconds
        n_intervals=0,
        disabled=False,
    ),
	dash.page_container
])

@app.callback([Output('store-receitas', 'data'), 
              Output('store-receitas2', 'data')],
          [Input('interval-componenty', 'n_intervals')])
def CHANGE_PAGE6(n_intervals):
    APP_LAYOUTS = gerar_slides(1)
    APP_LAYOUTS2 = gerar_slides(2)
    return [APP_LAYOUTS,APP_LAYOUTS2]



if __name__ == '__main__':
    app.run_server(host= '192.168.3.12',port=8051, debug=True)
