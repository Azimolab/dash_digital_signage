import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash_extensions.enrich import html, dcc, Output, Input, DashProxy
from dash import html, dcc, callback, Input, Output
from flask_caching import function_namespace
from matplotlib import dates
import pandas as pd
import plotly.express as px
from base64 import b64encode
from dash_svg import Svg, G, Path, Circle
from datetime import datetime, timedelta

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
    "fontSize": "2.5rem",
    "margin": "auto",
    "color": "#8B8CA8",
}
card_text2 = {
    "textAlign": "right",
    "fontSize": "2.5rem",
    "margin": "auto", 
}

def render_template1(group,channel,position,title,template,data,filter):
    g=str(group)
    c=str(channel)
    p=str(position)
    t=str(template)
    ID=g+c+p+t
    df_template1_data = pd.read_csv(data)
    df_template1_data['data'] =  pd.to_datetime(df_template1_data['data'], format='%Y/%m/%d')
    ACUMULADO = df_template1_data._get_value(filter, 'acumulado')
    VALOR_D = df_template1_data._get_value(filter, 'dia')
    UNIDADE = df_template1_data._get_value(filter, 'unidade')
    TITULO = title
  
    
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
                    dbc.Col(html.H1(TITULO, style={"font-size": "4vw"}),
                            width="auto", style={
                            "padding-left": "60px",
                            "padding-right": "10%",
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
                    dbc.Col(html.H2("DU",
                            style={"font-size": "3.5vw"}),
                            width="auto", style={
                            "padding-left": "70px",
                            "padding-right": "70px",
                            "text-align": "center",
                            "margin-left": "auto",
                            "margin-top": "-30px",
                            "margin-right": "140px",
                            "background-color": "#CE0300",
                            'color': 'white',
                            })
                ], className="g-0", style={"min-height": "30px"}),
            dbc.Row(
                [
                    dbc.Col(dbc.Card((dbc.CardHeader(dbc.Row(
                        [
                            dbc.Col(html.Div(className="bi bi-graph-up", style=card_icon),
                                    style={"padding-left": "20px",
                                           "display": "flex", "align-items": "center"},
                                    ),
                            dbc.Col(html.Div("ACUMULADO", style=card_text),
                                    style={"display": "flex",
                                           "align-items": "center"},
                                    ),
                        ], style={"padding-right": "30px", "padding-left": "30px"}),),
                        dbc.CardBody(
                        [
                            html.H5(ACUMULADO,
                                    className="card-title",
                                    style={
                                        "font-size": "10rem",
                                        "text-align": "center",
                                        "color": "#8B8CA8",
                                        "padding-top": "2%",
                                    }),
                            html.H5(UNIDADE,
                                   className="card-text",
                                   style={
                                       "font-size": "5rem",
                                       "text-align": "center",
                                       "color": "#8B8CA8", },
                                   ),
                        ], style={
                            "margin-top": "3%",
                            "margin-bottom": "3%",
                        }),), color="#FFFFFF", style={"background-color": "#FFFFFF", "min-height": "30%", }),
                        style={
                        "align-content": "center",
                    }),
                    dbc.Col(dbc.Card((dbc.CardHeader(dbc.Row(
                        [
                            dbc.Col(html.Div(className="bi bi-calendar-check", style=card_icon2),
                                    style={
                                        "padding-left": "20px", "display": "flex", "align-items": "center"},
                                    ),
                            dbc.Col(html.Div("DIA", style=card_text2),
                                    style={},
                                    ),
                        ], style={"padding-right": "30px", "padding-left": "30px"}),),
                        dbc.CardBody(
                        [
                            html.H5(VALOR_D,
                                    className="card-title",
                                    style={
                                        "font-size": "10rem",
                                        "text-align": "center",
                                        "padding-top": "2%",
                                    }),
                            html.H5(UNIDADE,
                                   className="card-text",
                                   style={
                                       "font-size": "5rem",
                                       "text-align": "center",
                                   },
                                   ),
                        ], style={
                            "margin-top": "3%",
                            "margin-bottom": "3%",
                        }),), color="#CE0300", inverse=True, style={"min-height": "30%"}),
                    ),
                ], style={"margin-left": "5%",
                          "margin-right": "5%",
                          "margin-top": "2%",
                          "margin-botton": "2%",
                          }),
        ],style={"background-color": cor_fundo, "min-height": "100vh"}, id=ID),
