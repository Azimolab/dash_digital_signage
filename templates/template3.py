import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash_extensions.enrich import html, dcc, Output, Input, DashProxy
import dash
import pandas as pd
from pandas.tseries.offsets import DateOffset
import plotly.express as px
from base64 import b64encode
from datetime import datetime, timedelta

config_graph={"displayModeBar": False, "showTips": False}

cor_fundo = "#E6E6EE"

row_table = {
    "width": "100%",
    "margin": "5px",
    "display": "flex",
    "flex-flow": "row wrap",
    "align-content": "stretch",
    "background-color" : "white",
    "border": "1px solid",
    "border-color": "grey",
}

txt_table_col1={
    "width": "40%",
    "height": "auto",

}
txt_table_col2={
    "width": "60%",
    "height": "auto",

}
txt_table_col3={
    "width": "60%",
    "height": "auto",
    "className": "g-0",
}


txt_table_valor = {
    "margin": "auto",
    "fontSize": "2vw",
    "color": "#8B8CA8",
  "font-weight": "bold",
  "text-align": "center"
}
txt_table_mes = {
      "margin": "auto",
    "fontSize": "2vw",
    "color": "#8B8CA8",
  "font-weight": "bold",
  "text-align": "left"
}
today = datetime.today()


def render_template3(group, channel, position, title, template, data, filter):
    TITLE = title
    g = str(group)
    c = str(channel)
    p = str(position)
    t = str(template)
    ID = g+c+p+t

    #filter = 180
    today = datetime.today()
    day1=(datetime.now().day)
    target = today - timedelta(days=int(filter))
    #data = 'humanos_prod.csv'
    df = pd.read_csv(data)

    df['data'] = df['data'].astype('datetime64[ns]')

    df = df[lambda x: x['data'].between(
        datetime(target.year, target.month, 1), today)]

    df["DIA"] = df["data"].apply(lambda x: str(x.day))
    df["MES"] = df["data"].apply(lambda x: str(x.month))
    df["ANO"] = df["data"].apply(lambda x: str(x.year))

    df = pd.DataFrame(df).sort_values(by='data', ascending=True)
    df_receitas_mes = df.groupby("MES")["valor"].median()
    df=df_receitas_mes.reset_index()

    #df.groupby('MES').sum() # soma meses

    fig = px.bar(df, x="MES", y="valor")

    fig2 = fig.update_layout(
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
            l=50,
            r=50,
            t=50,
        ),
        showlegend=True,
        plot_bgcolor='white'
    )

    img_bytes = fig2.to_image(
        format="png", width="100%", height="100%", scale=1)
    encoding = b64encode(img_bytes).decode()
    img2_b64 = "data:image/png;base64," + encoding

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
                    dbc.Col(html.H1(TITLE, style={"font-size": "3vw"}),
                            width="auto", style={
                            "padding-left": "3%",
                            "padding-right": "10%",
                            "margin-top": "-25px",
                            "background-color": "#CE0300",
                            'color': 'white',
                            "clip-path": "polygon(0 0, 100% 0, 84% 100%, 0% 100%)"
                            }),
                ],
                className="g-0",
            ),

            dbc.Row(
                [
                    dbc.Col(
                        html.Img(src=img2_b64, style={'width': '100%', "padding": "0%"}
                        ), className="g-0", width={"size": 10, "offset": 1})

                ], style={"margin-left": "5%",
                          "margin-right": "5%",
                          "margin-top": "2%",
                          "margin-botton": "2%",
                          "padding": "0%"}),
        ], style={"background-color": cor_fundo, "min-height": "100vh"}, id=ID),



