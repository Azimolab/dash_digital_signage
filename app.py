from dash import Dash, html, dcc
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_extensions.enrich import html, dcc, Output, Input
import pandas as pd
from templates import template1, template2,template3
import json 
import pickle
import os
import datetime
from flask_caching import Cache
from globals import *

estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", "https://fonts.googleapis.com/icon?family=Material+Icons", dbc.themes.LITERA, dbc.icons.BOOTSTRAP]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"


app = Dash(__name__, use_pages=True ,external_stylesheets=estilos + [dbc_css])
app.scripts.config.serve_locally = True
server = app.server

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})
app.config.suppress_callback_exceptions = True

timeout = 5


def render_slides(x):
    my_list = []
    my_dict = {}
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
            my_dict[id_slide] = Layout1

        elif template == 2:
            Layout2 = template2.render_template2(group,channel,position,title,template,data,filter) 
            my_dict[id_slide] = Layout2

        elif template == 3:
            Layout3 = template3.render_template3(group,channel,position,title,template,data,filter) 
            my_dict[id_slide] = Layout3

    #array = [ {'key' : i, 'value' : my_dict[i]} for i in my_dict]
    #print (array)
    
    #f = open("dict.txt","w")
    #f.write( str(my_dict) )
    #f.close()
    return my_dict

#Renderiza novos Layouts

    
              #State('cache_layout_c1', 'children'),
              #State('store_layouts_c2', 'data'),

app.layout = dbc.Container(children=[
    html.Div(id='cache_layout_c1'),
    html.Div(id='cache_layout_c2'),
    html.Div(id='cache_layout_c3'),
    html.Div(id='teste'),
    html.Div(id='time'),
    dcc.Store(id='store_layouts_c1'),
    dcc.Store(id='store_layouts_c11'),
    dcc.Store(id='store_layouts_c2'),
    dcc.Store(id='store_layouts_c3'),
    dcc.Store(id='store_update_new_layout'),
    dcc.Store(id='store_render_new_layout'),
    dcc.Store(id='store_timer'),
    dcc.Store(id='start_stop'),
   	dash.page_container   
], fluid=True, style={"padding": "0px"}, className="dbc")

@callback([Output('store_layouts_c1', 'data'),
          Output('store_layouts_c2', 'data'),
          Output('store_layouts_c3', 'data')],
          [Input('store_render_new_layout', 'data')],
          State('store_render_new_layout', 'data'),
         State('cache_layout_c1', 'children'),
         State('cache_layout_c2', 'children'),
         State('cache_layout_c3', 'children'))
def render_channel_layouts(n_intervals,W,d,q,tt):

    APP_LAYOUTS1 = render_slides(1)
    APP_LAYOUTS2 = render_slides(2)
    APP_LAYOUTS3 = render_slides(3)
    print("Novos slides renderizados")
    #print(APP_LAYOUTS1)
    #print(APP_LAYOUTS1)
    #json_object = json.dumps(APP_LAYOUTS1, indent = 4) 
    #print(json_object)

    return [APP_LAYOUTS1,APP_LAYOUTS2,APP_LAYOUTS3]


@app.callback(
    Output('cache_layout_c1', 'children'),
    Input('store_layouts_c1', 'data'),
    State('store_layouts_c1', 'data'))
@cache.memoize(timeout=timeout)  # in seconds
def render(value,store_layouts_c1):
    print('cache1 atualizado')
    with open('filepk.txt', 'wb') as handle:
        pickle.dump(value, handle)
    return value

@app.callback(
    Output('cache_layout_c2', 'children'),
    Input('store_layouts_c2', 'data'),
    State('store_layouts_c2', 'data'))
@cache.memoize(timeout=timeout)  # in seconds
def render2(value,store_layouts_c1):
    print('cache2 atualizado')
    with open('filepk2.txt', 'wb') as handle:
        pickle.dump(value, handle)
    return value

@app.callback(
    Output('cache_layout_c3', 'children'),
    Input('store_layouts_c3', 'data'),
    State('store_layouts_c3', 'data'))
@cache.memoize(timeout=timeout)  # in seconds
def render3(value,store_layouts_c3):
    print('cache3 atualizado')
    with open('filepk3.txt', 'wb') as handle:
        pickle.dump(value, handle)
    return value





if __name__ == '__main__':
   # app.run_server(host= '192.168.3.12',port=8051, debug=False)
    app.run_server(debug=True)



