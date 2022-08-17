from dash import Dash, html, dcc, callback, Input, Output
from dash.dependencies import Input, Output, State
from dash_extensions.enrich import html, dcc, Output, Input
import dash
import pandas as pd
import pickle

dash.register_page(__name__)

df_time = pd.read_csv('time.csv')


INTERVAL3 = df_time._get_value(0, 'x')
START3 = df_time._get_value(0, 'start')



def update_Start():
    df_time = pd.read_csv('time.csv')
    value = df_time._get_value(0, 'start')
    return value


layout = html.Div([
    dcc.Store(id='store-start3', data=START3),
    html.Div(id='app-container3'),
    dcc.Interval(
        id='interval-component3',
        interval=INTERVAL3*1000,  # in milliseconds
        n_intervals=0,
        disabled=True,
    ),
    dcc.Interval(
        id='interval-componentx3',
        interval=1000,  # in milliseconds
        n_intervals=0,
        disabled=False,
    )
])

@callback(Output('store-start3', 'data'),
          [Input('interval-componentx3', 'n_intervals')])
def CHANGE_PAGE6(n_intervals):
    SD = update_Start()
    return SD

@callback([Output('interval-component3', 'interval'),
          Output('interval-component3', 'disabled'),
          Output('app-container3', 'children')],
          [Input('interval-component3', 'n_intervals'),
          Input('store-start3', 'data')],
          [State('interval-component3', 'disabled'),
          State('interval-component3', 'interval'),
          State('store-start3', 'data')])
def CHANGE_PAGE3(n_intervalsInput, storedata, disabled, interval, storedatastate):
    print('display3 ok')
    
    with open('filepk3.txt', 'rb') as handle:
        b = pickle.loads(handle.read())

    SD = list(b.values())

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



