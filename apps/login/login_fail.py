import hashlib

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from urllib.parse import urlparse, parse_qs

import pandas as pd
from datetime import datetime

from app import app

from apps import dbconnect as db

layout = html.Div(
    [
        html.Div([html.H2('Staff Credentials', style={'color': '#8A1538','margin-top': '15px'})], style = {'margin-left':'40px','font-weight':'bold','float':'left'}),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4("You do not have access to this page", style = {'margin-left':'40px'}),
                        html.P("Please contact an admin for assistance.", style = {'margin-left':'40px'})
                        
                    ], 
                style={'background-color':'#ffffff','margin-left':'20px','margin-right':'20px'}
                )
            ],
        style={'background-color': 'transparent'}
        )
    ],
        style={
        'background-image': 'url("assets/backgroundimage.png")',
        'height': '100vh',
        'width': '100%',
        'margin': '0'}
)

