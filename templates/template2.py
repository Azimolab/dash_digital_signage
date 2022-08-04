import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash_extensions.enrich import html, dcc, Output, Input, DashProxy
import dash
from dash import html, dcc, callback, Input, Output
from flask_caching import function_namespace
from hamcrest import none
from matplotlib import dates
import pandas as pd
import plotly.express as px
from base64 import b64encode
from dash_svg import Svg, G, Path, Circle
from datetime import datetime, timedelta

config_graph={"displayModeBar": False, "showTips": False}

cor_fundo = "#E6E6EE"

card_icon = {
    "textAlign": "left",
    "fontSize": 60,
    "color": "#8B8CA8",
}
card_icon2 = {
    "textAlign": "left",
    "fontSize": 60,

}
card_text = {
    "textAlign": "right",
    "fontSize": 50,
    "margin": "auto",
    "color": "#8B8CA8",
}
card_text2 = {
    "textAlign": "right",
    "fontSize": 50,
    "margin": "auto", 
}

today = datetime.today()

def gerar_template_2(grupo,canal,posicao,titulo,template,data,filtro):
    TITULO = titulo
    g=str(grupo)
    c=str(canal)
    p=str(posicao)
    t=str(template)
    ID=g+c+p+t
    
    today = datetime.today()
    target = today - timedelta(days=int(filtro))
    df = pd.read_csv(data)
    df ['data'] = df['data'].astype('datetime64[ns]')
    df = df[lambda x: x['data'].between(datetime(target.year,target.month,1),today)]

    df["DIA"] = df["data"].apply(lambda x: str(x.day))
    df["MES"] = df["data"].apply(lambda x: str(x.month))
    df["ANO"] = df["data"].apply(lambda x: str(x.year))

    fig = px.line(df, x='DIA', y='valor', color='MES')

    fig2=fig.update_layout(
        xaxis=dict(
            title=None,
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=18,
                color='rgb(82, 82, 82)',
            ),
        ),

        yaxis=dict(
            title=None,
            tick0=10,
            dtick=20,
            showline=False,
            showgrid=False,
            showticklabels=True,
            tickfont=dict(
                family='Arial',
                size=18,
                color='rgb(82, 82, 82)',
            ),
        ),
        
        autosize=True,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )


    img_bytes = fig2.to_image(format="png", width=1340, height=900, scale=1)
    encoding = b64encode(img_bytes).decode()
    img_b64 = "data:image/png;base64," + encoding


    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.H1(),
                            style={
                        "min-height": "30px",
                        "background-color": "#CE0300", }),
                ],
                className="g-0",
            ),
            dbc.Row(
                [
                    dbc.Col(html.H1(TITULO, style={"font-size": "80px"}),
                            width="auto", style={
                            "padding-left": "60px",
                            "padding-right": "200px",
                            "margin-top": "-25px",
                            "background-color": "#CE0300",
                            'color': 'white',
                            "clip-path": "polygon(0 0, 100% 0, 84% 100%, 0% 100%)",
                            }),
                ],
                className="g-0",
            ),

            dbc.Row(
                [
                    dbc.Col(html.Img(src=img_b64),
                            width="9", style={'height': '100%'
                                              }),
                    dbc.Col([dbc.Row([
                        dbc.Col([
                            
                        ])
                    ], style={'padding-bottom': '7px', 'height': '50%'}),
                        dbc.Row([
                            dbc.Col([
                               
                            ])
                        ], justify='center', style={'height': '50%'})
                    ],)



                ], style={"margin-left": "60px",
                          "margin-right": "60px",
                          "margin-top": "40px",
                          "margin-botton": "40px",
                          }),
        ], style={"background-color": cor_fundo, "min-height": "100vh"}, id=ID),



