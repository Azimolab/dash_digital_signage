from dash import Dash, html, dcc, callback
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_extensions.enrich import html, dcc, Output, Input
import pandas as pd
from templates import template1, template2
import os
import datetime
from flask_caching import Cache
import pandas as pd

#df_db = pd.read_csv('db.csv')
#df_cartoes = pd.read_csv('cartoes.csv')
#df_humanos_prod = pd.read_csv('humanos_prod.csv')
