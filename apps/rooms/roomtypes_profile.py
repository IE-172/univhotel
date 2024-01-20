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
from decimal import Decimal

from app import app

from apps import dbconnect as db

layout = html.Div(
    [
        html.Div([
            dcc.Store(id = 'roomtypesprofile_toload', storage_type = 'memory', data = 0)
        ]),
        html.Div([html.H2('Room Type Details', style={'color': '#8A1538','margin-left':'25px'})], style = {'float':'left'}),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dbc.Alert(id = 'roomtypesprofile_alert', is_open = False),
                        html.H4("Room Type Information", style={'margin-left':'15px'}),
                        html.P("Fields marked with '*' are required.", style={'color': 'red', 'margin-left':'15px'}),
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label(["Room Type", html.Span("*", style={'color': 'red'})], style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.Input(id ='roomtypesprofile_roomtype', type = 'text', placeholder = 'Enter Room Type'), style={'text-align':'left'}, width = 4)
                                    ],
                                    className = 'mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label(["Max Occupants", html.Span("*", style={'color': 'red'})],  style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.InputGroup([dbc.Input(id = 'roomtypesprofile_occupants', placeholder="0", type="number", min = 1, step = 1),dbc.InputGroupText("Adult/s")]), style={'text-align':'left'}, width = 4),

                                    ],
                                    className = 'mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Resident Rate", style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.InputGroup([dbc.InputGroupText("₱"), dbc.Input(id = 'roomtypesprofile_resident', placeholder="Enter resident rate", type="number", min=0, step=0.01, pattern=r"^\d+(\.\d{1,2})?$",), dbc.InputGroupText("per month")]), width = 4),

                                    ],
                                    className = 'mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Transient Rate", style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.InputGroup([dbc.InputGroupText("₱"), dbc.Input(id = 'roomtypesprofile_transient', placeholder="Enter transient rate", type="number",min=0, step=0.01, pattern=r"^\d+(\.\d{1,2})?$",), dbc.InputGroupText("per day")]), width = 4),

                                    ],
                                    className = 'mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Extension Rate", style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.InputGroup([dbc.InputGroupText("₱"), dbc.Input(id = 'roomtypesprofile_extension', placeholder="Enter extension rate", type="number",min=0, step=0.01, pattern=r"^\d+(\.\d{1,2})?$",), dbc.InputGroupText("per hour")]), width = 4),
                                    ],
                                    className = 'mb-3'
                                ),
                                html.Hr(),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Label("Delete room type?", style={'margin-left':'15px'}, width = 2),
                                                dbc.Col(dbc.Checklist(id = 'roomtypesprofile_delete', inline = True, switch =True, value = 0, options = [{"label":"Mark as deleted","value":1}]), width = 4)
                                            ],
                                            className = 'mb-3'
                                        )
                                    ],
                                    id = 'roomtypesprofile_deletediv'
                                ),
                                html.Div(dbc.Button('Save Room Type', id = 'roomtypesprofile_save', n_clicks=0, style={'backgroundColor': '#00573F', 'color': 'white'}), className="d-grid gap-2 col-6 mx-auto"),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(html.H4("Room Type Saved")),
                                        dbc.ModalBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        #update once modal is working
                                                    ],
                                                    id = 'roomtypesprofile_feedbackmessage',
                                                    style={'margin-left': '1px'}
                                                )
                                            ]
                                        ),
                                        dbc.ModalFooter(
                                            [
                                                dbc.Button("Proceed", href = '/rooms/rooms_home', id = 'roomtypesprofile_btnmodal')
                                            ]
                                        )
                                    ],
                                    centered = True,
                                    id = 'roomtypesprofile_successmodal',
                                    backdrop = 'static'
                                )
                            ]
                            
                        )
                    ]
                )
            ],
            style={'background-color':'#ffffff','margin-left':'20px','margin-right':'20px'}
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
            Output('roomtypesprofile_alert', 'color'),
            Output('roomtypesprofile_alert', 'children'),
            Output('roomtypesprofile_alert','is_open'),

            Output('roomtypesprofile_successmodal','is_open'),
            Output('roomtypesprofile_feedbackmessage', 'children'),
            Output('roomtypesprofile_btnmodal', 'href')
        ],
        [
            Input('roomtypesprofile_save', 'n_clicks'),
            Input('roomtypesprofile_btnmodal', 'n_clicks')
        ],
        [
            State('roomtypesprofile_roomtype', 'value'),
            State('roomtypesprofile_occupants', 'value'),
            State('roomtypesprofile_resident', 'value'),
            State('roomtypesprofile_transient', 'value'),
            State('roomtypesprofile_extension', 'value'),
            State('url', 'search'),
            State('roomtypesprofile_delete', 'value')
        ]
)

def roomtypesprofile_saveprofile (submitbtn, closebtn, roomtype, occupants, resident, transient, extension, search, delete):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'roomtypesprofile_save' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            feedbackmessage = ''
            okay_href = ''

            if not roomtype:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply room type.'
            elif not occupants:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply maximum occupants.'
            elif occupants < 0:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply valid number of occupants.'
            elif not resident and not transient:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply at least 1 room rate.'

            elif resident is not None and resident < 0:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply valid rate.'
            elif transient is not None and transient < 0:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply valid rate.'
            elif extension is not None and extension < 0:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply valid rate.'
            else:
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]

                if create_mode == 'add':
                    
                    sql0="""INSERT INTO roomtype(
                        roomtype, maximumoccupants, residentrate, transientrate, roomextensionrate, roomtypedelete
                    )
                    VALUES(%s, %s, %s, %s, %s, %s)
                    """
                    values = [roomtype, occupants, resident, transient, extension, False]
                    db.modifydatabase(sql0, values)

                    feedbackmessage = "Room type has been saved."
                    okay_href = '/rooms/rooms_home'
                    modal_open = True
                
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    roomtypeid = parse_qs(parsed.query)['id'][0]

                    sql0 = """UPDATE roomtype
                    SET
                        roomtype = %s,
                        maximumoccupants = %s,
                        residentrate = %s,
                        transientrate = %s,
                        roomextensionrate = %s,
                        roomtypedelete = %s
                    WHERE
                        roomtypeid = %s
                    """
                    to_delete = bool(delete)
                    values = [roomtype, occupants, resident, transient, extension, to_delete, roomtypeid]
                    db.modifydatabase(sql0, values)               

                    feedbackmessage = "Room type has been updated."
                    okay_href = '/rooms/rooms_home'
                    modal_open = True

                else:
                    PreventUpdate
            
            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]


@app.callback(
    [
        Output('roomtypesprofile_deletediv', 'style'),
        Output('roomtypesprofile_toload', 'data')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url','search')
    ]
)

def roomtypesprofile_deletediv(pathname, search):
    if pathname =='/rooms/roomtypes_profile':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        deletediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [deletediv_style, to_load]

@app.callback(
    [
        Output('roomtypesprofile_roomtype', 'value'),
        Output('roomtypesprofile_occupants', 'value'),
        Output('roomtypesprofile_resident', 'value'),
        Output('roomtypesprofile_transient', 'value'),
        Output('roomtypesprofile_extension', 'value')
    ],
    [
        Input('roomtypesprofile_toload','modified_timestamp')
    ],
    [
        State('roomtypesprofile_toload', 'data'),
        State('url', 'search')
    ]
)

def roomtypesprofile_loadprofile (timestamp, toload, search):
    if toload == 1:
        parsed = urlparse(search)
        roomtypeid = parse_qs(parsed.query)['id'][0]
        sql ="""
            Select roomtype, maximumoccupants, residentrate, transientrate, roomextensionrate FROM roomtype
	            Where roomtypeid = %s """
        values = [roomtypeid]
        col = ['Room Type', 'Maximum Occupants', 'Resident Rate', 'Transient Rate', 'Extension Rate']
        df = db.querydatafromdatabase(sql, values, col)
        roomtype = (df['Room Type'][0]) if pd.notna(df['Room Type'][0]) else None
        maxpax = int(df['Maximum Occupants'][0]) if pd.notna(df['Maximum Occupants'][0]) else None
        resident = (df['Resident Rate'][0]) if pd.notna(df['Resident Rate'][0]) else None
        transient = (df['Transient Rate'][0]) if pd.notna(df['Transient Rate'][0]) else None
        extension = (df['Extension Rate'][0]) if pd.notna(df['Extension Rate'][0]) else None

        return [roomtype, maxpax, resident, transient, extension]
    else:
        raise PreventUpdate
