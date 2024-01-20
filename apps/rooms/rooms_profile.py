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
        html.Div([
            dcc.Store(id = 'roomsprofile_toload', storage_type = 'memory', data = 0)
        ]),
        html.Div([html.H2('Room Details', style={'color': '#8A1538', 'margin-left': '25px'})], style = {'float':'left'}),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dbc.Alert(id = 'roomsprofile_alert', is_open = False),
                        html.H4("Room Information", style = {'margin-left': '15px'}),
                        html.P("Fields marked with '*' are required.", style={'color': 'red', 'margin-left': '15px'}),
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label(["Room Number", html.Span("*", style={'color': 'red'})], style = {'margin-left': '15px'}, width = 2),
                                        dbc.Col(dbc.Input(id ='roomsprofile_roomnumber', type = 'text', placeholder = 'Enter Room Number'), style = {'text-align': 'left'}, width = 4)
                                    ],
                                    className = 'mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label(["Room Type", html.Span("*", style={'color': 'red'})], style = {'margin-left': '15px'}, width = 2),
                                        dbc.Col(dcc.Dropdown(id = 'roomsprofile_roomtype', placeholder = "Select Room Type"), style = {'text-align': 'left'}, width = 4)
                                    ],
                                    className = 'mb-3'
                                ),
                                html.Hr(),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Label("Delete Room?", style = {'margin-left': '15px'}, width = 2),
                                                dbc.Col(dbc.Checklist(id = 'roomsprofile_delete', inline = True, switch =True, value = 0, options = [{"label":"Mark as deleted","value":1}]), width = 4)
                                            ],
                                            className = 'mb-3'
                                        )
                                    ],
                                    id = 'roomsprofile_deletediv'
                                ),
                                html.Div(dbc.Button('Save Room', id = 'roomsprofile_save', n_clicks=0, style={'backgroundColor': '#00573F', 'color': 'white', 'borderColor': '#00573F'}), className="d-grid gap-2 col-6 mx-auto"),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(html.H4("Room Saved")),
                                        dbc.ModalBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        #update once modal is working
                                                    ],
                                                    id = 'roomsprofile_feedbackmessage',
                                                    style={'margin-left': '1px'}
                                                )
                                            ]
                                        ),
                                        dbc.ModalFooter(
                                            [
                                                dbc.Button("Proceed", href = '/rooms/rooms_home', id = 'roomsprofile_btnmodal')
                                            ]
                                        )
                                    ],
                                    centered = True,
                                    id = 'roomsprofile_successmodal',
                                    backdrop = 'static'
                                )
                            ]
                            
                        )
                    ]
                )
            ],
            style = {'background-color': '#ffffff', 'margin-left': '20px', 'margin-right': '20px'}
        )
    ],
    style={
        'background-image': 'url("assets/backgroundimage.png")',
        'height': '100vh',
        'width': '100%',
        'margin': '0'}
)

@app.callback(
    [
        Output('roomsprofile_roomtype','options')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)

def roomsprofile_loaddropdowns (pathname, search):
    if pathname == '/rooms/rooms_profile':
        sql1 = """
        SELECT roomtype as label, roomtypeid as value FROM roomtype
        WHERE NOT roomtypedelete """
        values1 = []
        cols1 = ['label', 'value']
        df1 = db.querydatafromdatabase(sql1, values1, cols1)
        roomtype_options = df1.to_dict('records')

        return [roomtype_options]
    
    else:
        raise PreventUpdate

@app.callback(
        [
            Output('roomsprofile_alert', 'color'),
            Output('roomsprofile_alert', 'children'),
            Output('roomsprofile_alert','is_open'),

            Output('roomsprofile_successmodal','is_open'),
            Output('roomsprofile_feedbackmessage', 'children'),
            Output('roomsprofile_btnmodal', 'href')
        ],
        [
            Input('roomsprofile_save', 'n_clicks'),
            Input('roomsprofile_btnmodal', 'n_clicks')
        ],
        [
            State('roomsprofile_roomnumber', 'value'),
            State('roomsprofile_roomtype', 'value'),
            State('url', 'search'),
            State('roomsprofile_delete', 'value')
        ]
)

def roomsprofile_saveprofile (submitbtn, closebtn, roomnumber, roomtype, search, delete):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'roomsprofile_save' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            feedbackmessage = ''
            okay_href = ''

            if not roomnumber:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply room number.'
            elif not roomtype:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply room type.'
            else:
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]

                if create_mode == 'add':
                    
                    sql0="""INSERT INTO room(
                        roomnumber, roomtypeid, roomdelete
                    )
                    VALUES(%s, %s, %s)
                    """
                    values = [roomnumber, roomtype, False]
                    try:
                        db.modifydatabase(sql0, values)
                    except Exception:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = 'Room number already exists.'
                        return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

                    feedbackmessage = "Room has been saved."
                    okay_href = '/rooms/rooms_home'
                    modal_open = True
                
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    roomid = parse_qs(parsed.query)['id'][0]

                    sql0 = """UPDATE room
                    SET
                        roomnumber = %s,
                        roomtypeid = %s,
                        roomdelete = %s
                    WHERE
                        roomid = %s
                    """
                    to_delete = bool(delete)
                    values = [roomnumber, roomtype, to_delete, roomid]
                    try:
                        db.modifydatabase(sql0, values)
                    except Exception:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = 'Room number already exists.'
                        return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]                  

                    feedbackmessage = "Room has been updated."
                    okay_href = '/rooms/rooms_home'
                    modal_open = True

                else:
                    PreventUpdate
            
            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]


@app.callback(
    [
        Output('roomsprofile_deletediv', 'style'),
        Output('roomsprofile_toload', 'data')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url','search')
    ]
)

def roomsprofile_deletediv(pathname, search):
    if pathname =='/rooms/rooms_profile':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        deletediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [deletediv_style, to_load]

@app.callback(
    [
        Output('roomsprofile_roomnumber', 'value'),
        Output('roomsprofile_roomtype', 'value'),
    ],
    [
        Input('roomsprofile_toload','modified_timestamp')
    ],
    [
        State('roomsprofile_toload', 'data'),
        State('url', 'search')
    ]
)

def roomsprofile_loadprofile (timestamp, toload, search):
    if toload == 1:
        parsed = urlparse(search)
        roomid = parse_qs(parsed.query)['id'][0]
        sql ="""
            Select roomnumber, roomtypeid FROM room
	            Where roomid = %s """
        values = [roomid]
        col = ['Room No.', 'Room Type']
        df = db.querydatafromdatabase(sql, values, col)
        roomnumber = (df['Room No.'][0]) if pd.notna(df['Room No.'][0]) else None
        roomtypeid = int(df['Room Type'][0]) if pd.notna(df['Room Type'][0]) else None

        return [roomnumber, roomtypeid]
    else:
        raise PreventUpdate


