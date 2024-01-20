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
            dcc.Store(id = 'groupprofile_toload', storage_type = 'memory', data = 0)
        ]),
        html.Div([html.H2('Group Details', style={'color': '#8A1538','margin-left':'25px'})], style = {'float':'left'}),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dbc.Alert(id = 'groupprofile_alert', is_open = False),
                        html.H4("Group Information", style={'margin-left':'15px'}),
                        html.P("Fields marked with '*' are required.", style={'color': 'red', 'margin-left':'15px'}),
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label(["Group Name", html.Span("*", style={'color': 'red'})], style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.Input(id ='groupprofile_groupname', type = 'text', placeholder = 'Enter Group Name'), style={'text-align':'left'})
                                    ],
                                    className = 'mb-3'
                                ),
                                html.Hr(),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Label("Delete group?", style={'margin-left':'15px'}, width = 2),
                                                dbc.Col(dbc.Checklist(id = 'groupprofile_delete', inline = True, switch =True, value = 0, options = [{"label":"Mark as deleted","value":1}]), width = 4)
                                            ],
                                            className = 'mb-3'
                                        )
                                    ],
                                    id = 'groupprofile_deletediv'
                                ),
                                html.Div(dbc.Button('Save Group Profile', id = 'groupprofile_save', n_clicks=0, style={'backgroundColor': '#00573F', 'color': 'white'}), className="d-grid gap-2 col-6 mx-auto"),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(html.H4("Group Profile Saved")),
                                        dbc.ModalBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        #update once modal is working
                                                    ],
                                                    id = 'groupprofile_feedbackmessage',
                                                    style={'margin-left': '1px'}
                                                )
                                            ]
                                        ),
                                        dbc.ModalFooter(
                                            [
                                                dbc.Button("Proceed", href = '/guests/guests_home', id = 'groupprofile_btnmodal')
                                            ]
                                        )
                                    ],
                                    centered = True,
                                    id = 'groupprofile_successmodal',
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
            Output('groupprofile_alert', 'color'),
            Output('groupprofile_alert', 'children'),
            Output('groupprofile_alert','is_open'),

            Output('groupprofile_successmodal','is_open'),
            Output('groupprofile_feedbackmessage', 'children'),
            Output('groupprofile_btnmodal', 'href')
        ],
        [
            Input('groupprofile_save', 'n_clicks'),
            Input('groupprofile_btnmodal', 'n_clicks')
        ],
        [
            State('groupprofile_groupname', 'value'),
            State('url', 'search'),
            State('groupprofile_delete', 'value')
        ]
)

def groupprofile_saveprofile (submitbtn, closebtn, groupname, search, delete):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'groupprofile_save' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            feedbackmessage = ''
            okay_href = ''

            if not groupname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply group name.'
            else:
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]

                if create_mode == 'add':
                    
                    sql0="""INSERT INTO groupguest(
                        groupguestname, groupguestdelete
                    )
                    VALUES(%s, %s)
                    """
                    values = [groupname, False]
                    db.modifydatabase(sql0, values)

                    feedbackmessage = "Group profile has been saved."
                    okay_href = '/guests/guests_home'
                    modal_open = True
                
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    groupguestid = parse_qs(parsed.query)['id'][0]

                    sql0 = """UPDATE groupguest
                    SET
                        groupguestname = %s,
                        groupguestdelete = %s
                    WHERE
                        groupguestid = %s
                    """
                    to_delete = bool(delete)
                    values = [groupname, to_delete, groupguestid]
                    db.modifydatabase(sql0, values)                   

                    feedbackmessage = "Group profile has been updated."
                    okay_href = '/guests/guests_home'
                    modal_open = True

                else:
                    PreventUpdate
            
            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]


@app.callback(
    [
        Output('groupprofile_deletediv', 'style'),
        Output('groupprofile_toload', 'data')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url','search')
    ]
)

def groupprofile_deletediv(pathname, search):
    if pathname =='/guests/guests_groupprofile':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        deletediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [deletediv_style, to_load]

@app.callback(
    [
        Output('groupprofile_groupname', 'value'),
    ],
    [
        Input('groupprofile_toload','modified_timestamp')
    ],
    [
        State('groupprofile_toload', 'data'),
        State('url', 'search')
    ]
)

def groupprofile_loadprofile (timestamp, toload, search):
    if toload == 1:
        parsed = urlparse(search)
        groupguestid = parse_qs(parsed.query)['id'][0]
        sql ="""
            Select groupguestname FROM groupguest
	            Where groupguestid = %s """
        values = [groupguestid]
        col = ['groupname']
        df = db.querydatafromdatabase(sql, values, col)
        groupname = (df['groupname'][0]) if pd.notna(df['groupname'][0]) else None

        return [groupname]
    else:
        raise PreventUpdate


