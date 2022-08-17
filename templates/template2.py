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


def render_template2(group, channel, position, title, template, data, filter):
    TITLE = title
    g = str(group)
    c = str(channel)
    p = str(position)
    t = str(template)
    ID = g+c+p+t

    filter = 180
    data = 'humanos_prod.csv'
    today = datetime.today()

    day1=(datetime.now().day)
    
    target = today - timedelta(days=int(filter))
    df = pd.read_csv(data)

    df['data'] = df['data'].astype('datetime64[ns]')

    df = df[lambda x: x['data'].between(
        datetime(target.year, target.month, 1), today)]

    df["DIA"] = df["data"].apply(lambda x: str(x.day))
    df["MES"] = df["data"].apply(lambda x: str(x.month))
    df["ANO"] = df["data"].apply(lambda x: str(x.year))

    #df.groupby('MES').sum() # soma meses
    df_ds = pd.DataFrame(df).sort_values(by='data', ascending=True)
    fig = px.line(df_ds, x='DIA', y='valor', color='MES')

    df2=df

    array2 = ['2']
    mes2= df2.loc[df2['MES'].isin(array2)]
    v2=mes2['valor'].values[day1]

    array3 = ['3']
    mes3= df2.loc[df2['MES'].isin(array3)]
    v3=mes3['valor'].values[day1]

    array4 = ['4']
    mes4= df2.loc[df2['MES'].isin(array4)]
    v4=mes4['valor'].values[day1]

    array5 = ['5']
    mes5= df2.loc[df2['MES'].isin(array5)]
    v5=mes5['valor'].values[day1]

    array6 = ['6']
    mes6= df2.loc[df2['MES'].isin(array6)]
    v6=mes6['valor'].values[day1]

    array7 = ['7']
    mes7= df2.loc[df2['MES'].isin(array7)]
    v7=mes7['valor'].values[day1]

    

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
        showlegend=False,
        plot_bgcolor='white'
    )

    img_bytes = fig2.to_image(
        format="png", width="100%", height="100%", scale=1)
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
                        html.Img(src=img_b64, style={'width': '100%', "padding": "0%"}
                        ), className="g-0", width="9"),
                    dbc.Col([
                        dbc.Row(
                            [
                                dbc.Col(html.Div("JUL", style=txt_table_mes), width=4, style=txt_table_col1),
                                dbc.Col(html.Div(v7, style=txt_table_valor), width=8, style=txt_table_col2),
                            ], style=row_table
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div("JUN", style=txt_table_mes), width=4, style=txt_table_col1),
                                dbc.Col(html.Div(v6, style=txt_table_valor), width=8, style=txt_table_col2)
                            ], style=row_table
                        ),
                        dbc.Row(
                            [
                                 dbc.Col(html.Div("MAI", style=txt_table_mes), width=4, style=txt_table_col1),
                                dbc.Col(html.Div(v5, style=txt_table_valor), width=8, style=txt_table_col2),
                            ], style=row_table
                        ),
                        dbc.Row(
                            [
                                 dbc.Col(html.Div("ABR", style=txt_table_mes), width=4, style=txt_table_col1),
                                dbc.Col(html.Div(v4, style=txt_table_valor), width=8, style=txt_table_col2),
                            ], style=row_table
                        ),
                        dbc.Row(
                            [
                                 dbc.Col(html.Div("MAR", style=txt_table_mes), width=4, style=txt_table_col1),
                                dbc.Col(html.Div(v3, style=txt_table_valor), width=8, style=txt_table_col2),
                            ], style=row_table
                        ),
                        dbc.Row(
                            [
                                 dbc.Col(html.Div("FEV", style=txt_table_mes), width=4, style=txt_table_col1),
                                dbc.Col(html.Div(v2, style=txt_table_valor), width=8, style=txt_table_col2),
                            ], style=row_table
                        )
                    ], className="g-0", width="3", 
                    style={"padding": "0%", "min-height": "100%",
                    "display": "flex", 
                    "flex-flow": "row wrap", 
                    "align-content": "stretch",
                     "background-color" : "white",})

                ], style={"margin-left": "5%",
                          "margin-right": "5%",
                          "margin-top": "2%",
                          "margin-botton": "2%",
                          "padding": "0%"}),
        ], style={"background-color": cor_fundo, "min-height": "100vh"}, id=ID),



