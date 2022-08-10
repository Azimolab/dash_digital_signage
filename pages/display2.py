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


INTERVAL2 = df_time._get_value(0, 'x')
START2 = df_time._get_value(0, 'start')



def update_Start():
    df_time = pd.read_csv('time.csv')
    value = df_time._get_value(0, 'start')
    return value


layout = html.Div([
    dcc.Store(id='store-start2', data=START2),
    html.Div(id='app-container2'),
    dcc.Interval(
        id='interval-component2',
        interval=INTERVAL2*1000,  # in milliseconds
        n_intervals=0,
        disabled=True,
    ),
    dcc.Interval(
        id='interval-componentx2',
        interval=1000,  # in milliseconds
        n_intervals=0,
        disabled=False,
    )
])


@callback(Output('store-start2', 'data'),
          [Input('interval-componentx2', 'n_intervals')])
def CHANGE_PAGE6(n_intervals):
    SD = update_Start()
    return SD



@callback([Output('interval-component2', 'interval'),
          Output('interval-component2', 'disabled'),
          Output('app-container2', 'children')],
          [Input('interval-component2', 'n_intervals'),
          Input('store-start2', 'data'),
          Input('store-receitas2', 'data')],
          [State('interval-component2', 'disabled'),
          State('interval-component2', 'interval'),
          State('store-start2', 'data')])
def CHANGE_PAGE3(n_intervalsInput, storedata, storedata2, disabled, interval, storedatastate):
    SD= storedata2
    print('display2 ok')
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



