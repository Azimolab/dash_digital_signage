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

def render_slides(x):
    my_list = []
    df_db = pd.read_csv('db.csv',index_col=0)
    db2 = df_db[df_db['channel'] == x] 
    #db2 = db.loc[db['channel'] == 1]  
    db2.reset_index(inplace=True)
    db4= len(db2.index)
    for i in range(db4):
        id_slide = db2._get_value(i, 'id_slide')
        group = db2._get_value(i, 'group')
        channel = db2._get_value(i, 'channel')
        position = db2._get_value(i, 'position')
        title = db2._get_value(i, 'title')
        template = db2._get_value(i, 'template')
        data = db2._get_value(i, 'data')
        filter = db2._get_value(i, 'filter')

        if template == 1:
            Layout1 = template1.render_template1(group,channel,position,title,template,data,filter) 
            my_list.append(Layout1) 
        if template == 2:
            Layout2 = template2.render_template2(group,channel,position,title,template,data,filter) 
            my_list.append(Layout2) 
        
    return my_list

APP_LAYOUTS1 = render_slides(1)
APP_LAYOUTS2 = render_slides(2)


app.layout = html.Div([
    html.Div(
        [
            html.Div(
            )
        ]
    ),
    dcc.Store(id='store-receitas', data=APP_LAYOUTS1),
    dcc.Store(id='store-receitas2', data=APP_LAYOUTS2),
    dcc.Interval(
        id='interval-componenty',
        interval=10000,  # in milliseconds
        n_intervals=0,
        disabled=True,
    ),
	dash.page_container
])

@app.callback([Output('store-receitas', 'data'), 
              Output('store-receitas2', 'data')],
          [Input('interval-componenty', 'n_intervals')])
def CHANGE_PAGE6(n_intervals):
    APP_LAYOUTS1 = render_slides(1)
    APP_LAYOUTS2 = render_slides(2)
    print(APP_LAYOUTS1)
    return [APP_LAYOUTS1,APP_LAYOUTS2]



if __name__ == '__main__':
   # app.run_server(host= '192.168.3.12',port=8051, debug=False)
    app.run_server(debug=False)
