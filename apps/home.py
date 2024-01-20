from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app

layout = html.Div(
    [
        html.H2(
            style={
                'background-color': '#8A1538',
                'opacity': '0.95',
                'width': '100%',
                'left': '0',
                'margin': '-30px 0 0 0',
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center',
            },
            children=[
                html.H2(
                    'Welcome to the University Hotel Front Desk Database!',
                    className='slide-in',
                    style={
                        'font-weight': 'bold',
                        'color': '#faf5f5',
                        'text-align': 'center',
                        'padding': '5px',
                        'width': '100%',
                    }
                )
            ]
        ),
        html.Br(),
        html.H2(
            'This application simplifies the operations of the University Hotel Front Desk by providing fundamental features for bookings, room management, and the generation of necessary reports.',
            style={
                'font-weight': 'normal',
                'font-size': '20px',
                'font-style': 'italic',
                'color': '#000000',
                'text-align': 'center',
                'margin-left': '250px',
                'margin-right': '250px',
            }
        ),
        html.Br(),
        html.Div([
            html.P("If any assistance is needed, contact the admin for help."),
        ],
        style={
             'font-weight': 'bold',
                'font-size': '20px',
                'font-style': 'italic',
                'color': '#000000',
                'text-align': 'center',
                'margin-left': '250px',
                'margin-right': '250px',
        }),
        dbc.Carousel(
            items=[
                {"key": "1", "src": "assets/slide1.png"},
                {"key": "2", "src": "assets/slide2.png"},
                {"key": "3", "src": "assets/slide3.png"},
            ],
            controls=True,
            indicators=True,
            style={
                'width': '45%',
                'height': '20px',
                'margin': 'auto',
                'border': 'none',
                'text-align': 'center',
            }
        ),
    ],
    style={
        'background-image': 'url("assets/backgroundimage.png")',
        'height': '100vh',
        'width': '100%',
        'margin': '0'}
)

