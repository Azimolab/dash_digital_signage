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


dash.register_page(__name__)

df_time = pd.read_csv('time.csv')


INTERVAL = df_time._get_value(0, 'x')
START = df_time._get_value(0, 'start')



def update_Start():
    df_time = pd.read_csv('time.csv')
    value = df_time._get_value(0, 'start')
    return value


layout = html.Div([
    dcc.Store(id='store-start', data=START),
    html.Div(id='app-container'),
    dcc.Interval(
        id='interval-component',
        interval=INTERVAL*1000,  # in milliseconds
        n_intervals=0,
        disabled=True,
    ),
    dcc.Interval(
        id='interval-componentx',
        interval=1000,  # in milliseconds
        n_intervals=0,
        disabled=False,
    )
])


@callback(Output('store-start', 'data'),
          [Input('interval-componentx', 'n_intervals')])
def CHANGE_PAGE6(n_intervals):
    SD = update_Start()
    return SD



@callback([Output('interval-component', 'interval'),
          Output('interval-component', 'disabled'),
          Output('app-container', 'children')],
          [Input('interval-component', 'n_intervals'),
          Input('store-start', 'data'),
          Input('store-receitas', 'data')],
          [State('interval-component', 'disabled'),
          State('interval-component', 'interval'),
          State('store-start', 'data')])
def CHANGE_PAGE3(n_intervalsInput, storedata, storedata2, disabled, interval, storedatastate):
    print('display1 ok')
    SD= storedata2
    LAYOUTS_TELA_1 = SD
    I = interval
    D = disabled
    I = update_refresh_rate(LAYOUTS_TELA_1)
    app = LAYOUTS_TELA_1[n_intervalsInput % len(LAYOUTS_TELA_1)]
    if storedata == True:
        I = update_refresh_rate(LAYOUTS_TELA_1)
        app = LAYOUTS_TELA_1[n_intervalsInput % len(LAYOUTS_TELA_1)]
        D = False
    else:
        D = True
    return [I, D, app]


def update_refresh_rate(x):
    df_time = pd.read_csv('time.csv')
    value = (df_time._get_value(0, 'x') / len(x))
    limited_value = (round(value, 2))*1000
    return limited_value



