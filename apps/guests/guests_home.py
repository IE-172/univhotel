from dash import dcc
from dash import html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div([html.H2('Guests', style={'color': '#8A1538','margin-top': '15px'})], style={'margin-left':'20px','font-weight':'bold','float': 'left'}),
                        html.Div([dbc.Button("Add New Guest", href='/guests/guests_guestprofile?mode=add', style={'backgroundColor': '#00573F', 'color': 'white', 
                                                                                                            'padding': '10px', 'margin-right':'0px','borderColor':'#00573F',
                                                                                                            'align-items': 'center','margin-top': '10px'})], style={'float': 'right'}),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                    ],
                    width=6  
                ),
                dbc.Col(
                    [
                        html.Div([html.H2('Groups', style={'color': '#8A1538','margin-top': '15px'})], style={'font-weight':'bold','float': 'left'}),
                        html.Div([dbc.Button("Add New Group", href='/guests/guests_groupprofile?mode=add', style={'backgroundColor': '#00573F', 'color': 'white', 
                                                                                                            'padding': '10px', 'margin-right':'20px','borderColor':'#00573F',
                                                                                                            'align-items': 'center','margin-top': '10px'})], style={'float': 'right'}),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                    ],
                    width=6 
                ),
            ],
            style={'background-color':'transparent'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            dbc.Form(
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Search Guests", style={'text-align':'left','color': '#000000','font-weight':'bold'}, width = 3),
                                                        dbc.Col(dbc.Input(id = 'guestshome_guestfilter', placeholder = 'Guest Last Name', type = 'text'), style={'text-align':'left'}, width = 4),
                                                    ],
                                                    className = 'mb-3'
                                                )
                                            )
                                        ),
                                        html.Hr(),
                                        html.Div("Table with Guests", id = 'guestshome_guestslist',style={'background-color':'#ffffff'}),
                                    ],
                                )
                            ],
                            style={'background-color':'#ffffff','margin-left':'20px'}
                        )
                    ],
                    width=6  
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            dbc.Form(
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Search Groups", style={'text-align':'left','color': '#000000','font-weight':'bold'}, width = 3),
                                                        dbc.Col(dbc.Input(id = 'guestshome_groupfilter', placeholder = 'Group Name', type = 'text'), width = 4),
                                                    ],
                                                    className = 'mb-3'
                                                )
                                            )
                                        ),
                                        html.Hr(),
                                        html.Div("Table with Groups", id = 'guestshome_groupslist',style={'background-color':'#ffffff'}),
                                    ],
                                )
                            ],
                            style={'background-color':'#ffffff','margin-right':'20px'}
                        )
                    ],
                    width=6  
                ),
            ]
        ),
    ],
    style={
        'background-image': 'url("assets/backgroundimage.png")',
        'height': '100vh',
        'width': '100%',
        'margin': '0'}
)

@app.callback(
    [
        Output('guestshome_guestslist','children')
    ],
    [
        Input('url','pathname'),
        Input('guestshome_guestfilter', 'value')
    ]
)

def loadbookinglist (pathname, searchterm):
    if pathname == '/guests/guests_home':    
        sql = """SELECT CONCAT(surname, ', ', firstname,' ', middlename ), mobile, guestid
            FROM guest
            WHERE NOT guestdelete
            """
        values = []
        cols = ['Guest Name', 'Contact Number', 'Guest ID']

        if searchterm:
            sql += "AND surname ILIKE %s"
            values += [f"%{searchterm}%"]
        
        sql += "ORDER BY surname ASC"
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for guest_id in df['Guest ID']:
                buttons += [
                    html.Div(dbc.Button('View Profile', href = f'/guests/guests_guestprofile?mode=edit&id={guest_id}', size = 'sm', color = 'warning'), style = {'text-align':'center'})
                ]
            df['Action'] = buttons
            df = df[['Guest Name', 'Contact Number', 'Action']]
            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('guestshome_groupslist','children')
    ],
    [
        Input('url','pathname'),
        Input('guestshome_groupfilter', 'value')
    ]
)

def loadbookinglist (pathname, searchterm):
    if pathname == '/guests/guests_home':    
        sql = """SELECT groupguestname, groupguestid
            FROM groupguest
            WHERE NOT groupguestdelete
            """
        values = []
        cols = ['Group Name', 'Group ID']

        if searchterm:
            sql += "AND groupguestname ILIKE %s"
            values += [f"%{searchterm}%"]
        
        sql += "ORDER BY groupguestname ASC"
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for group_id in df['Group ID']:
                buttons += [
                    html.Div(dbc.Button('View Profile', href = f'/guests/guests_groupprofile?mode=edit&id={group_id}', size = 'sm', color = 'warning'), style = {'text-align':'center'})
                ]
            df['Action'] = buttons
            df = df[['Group Name', 'Action']]
            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate