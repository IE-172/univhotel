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
import phonenumbers

from app import app

from apps import dbconnect as db

layout = html.Div(
    [
        html.Div([
            dcc.Store(id = 'guestprofile_toload', storage_type = 'memory', data = 0)
        ]),
        html.Div([html.H2('Guest Details', style={'color': '#8A1538','margin-left':'25px'})], style = {'float':'left'}),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dbc.Alert(id = 'guestprofile_alert', is_open = False),
                        html.H4("Personal Information", style={'margin-left':'15px'}),
                        html.P("Fields marked with '*' are required.", style={'color': 'red', 'margin-left':'15px'}),
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label(html.Div(["Guest Name", html.Span("*", style={'color': 'red'})]), style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.Input(id ='guestprofile_surname', type = 'text', placeholder = 'Last Name'), width = 2),
                                        dbc.Col(dbc.Input(id ='guestprofile_firstname', type = 'text', placeholder = 'First Name'), width = 2),
                                        dbc.Col(dbc.Input(id ='guestprofile_middlename', type = 'text', placeholder = 'Middle Name'),width = 2),
                                    ],
                                    className = 'mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Guest Address", style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.Textarea(id = 'guestprofile_address', placeholder="Street Address, Municipality/ Barangay, Province/ Charted City, Region, Country"))
                                    ],
                                    className="mb-3"
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label(html.Div(["Mobile No.", html.Span("*", style={'color': 'red'})]), style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.Input(id = 'guestprofile_mobile', type ='text', placeholder = '+639XXXXXXXXX'), width = 3),
                                        dbc.Label(html.Div(["Email", html.Span("*", style={'color': 'red'})]), style={'margin-left':'45px'}, width =2),
                                        dbc.Col(dbc.Input(id = 'guestprofile_email', type ='email', placeholder = 'user@email.com'), width = 3)

                                    ],
                                    className = 'mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Occupation", style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.Input(id = 'guestprofile_occupation', type ='text', placeholder = 'Enter Occupation'))
                                    ],
                                    className = 'mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Nationality", style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.Input(id = 'guestprofile_nationality', type ='text', placeholder = 'Enter Nationality'), width = 3),
                                        dbc.Label("Passport No.", style={'margin-left':'45px'}, width =2),
                                        dbc.Col(dbc.Input(id = 'guestprofile_passport', type ='text', placeholder = 'XXYYYYYYY'), width = 3)

                                    ],
                                    className = 'mb-3'
                                ),
                                html.Hr(),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Label("Delete guest?", style={'margin-left':'15px'}, width = 2),
                                                dbc.Col(dbc.Checklist(id = 'guestprofile_delete', inline = True, switch =True, value = 0, options = [{"label":"Mark as deleted","value":1}]), width = 4)
                                            ],
                                            className = 'mb-3'
                                        )
                                    ],
                                    id = 'guestprofile_deletediv'
                                ),
                                html.Div(dbc.Button('Save Guest Profile', id = 'guestprofile_save', n_clicks=0, style={'backgroundColor': '#00573F', 'color': 'white'}), className="d-grid gap-2 col-6 mx-auto"),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(html.H4("Guest Profile Saved")),
                                        dbc.ModalBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        #update once modal is working
                                                    ],
                                                    id = 'guestprofile_feedbackmessage',
                                                    style={'margin-left': '1px'}
                                                )
                                            ]
                                        ),
                                        dbc.ModalFooter(
                                            [
                                                dbc.Button("Proceed", href = '/guests/guests_home', id = 'guestprofile_btnmodal')
                                            ]
                                        )
                                    ],
                                    centered = True,
                                    id = 'guestprofile_successmodal',
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
            Output('guestprofile_alert', 'color'),
            Output('guestprofile_alert', 'children'),
            Output('guestprofile_alert','is_open'),

            Output('guestprofile_successmodal','is_open'),
            Output('guestprofile_feedbackmessage', 'children'),
            Output('guestprofile_btnmodal', 'href')
        ],
        [
            Input('guestprofile_save', 'n_clicks'),
            Input('guestprofile_btnmodal', 'n_clicks')
        ],
        [
            State('guestprofile_surname', 'value'),
            State('guestprofile_firstname', 'value'),
            State('guestprofile_middlename', 'value'),
            State('guestprofile_address', 'value'),
            State('guestprofile_mobile', 'value'),
            State('guestprofile_email', 'value'),
            State('guestprofile_occupation', 'value'),
            State('guestprofile_nationality', 'value'),
            State('guestprofile_passport', 'value'),
            State('url', 'search'),
            State('guestprofile_delete', 'value')
        ]
)

def guestprofile_saveprofile (submitbtn, closebtn, surname, firstname, middlename, address, mobile, email, occupation, nationality, passport, search, delete):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'guestprofile_save' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            feedbackmessage = ''
            okay_href = ''

            if not surname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply guest last name.'
            elif not firstname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply guest first name.'
            elif not mobile:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply guest mobile number.'
            elif not email:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply guest email.'
            elif mobile and not phonenumbers.is_valid_number(phonenumbers.parse(mobile)):
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply a valid mobile number.'
            else:
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]

                if create_mode == 'add':
                    
                    sql0="""INSERT INTO guest(
                        surname, firstname, middlename, address, mobile, email, occupation, nationality, passport, guestdelete
                    )
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = [surname, firstname, middlename, address, mobile, email, occupation, nationality, passport, False]
                    db.modifydatabase(sql0, values)

                    feedbackmessage = "Guest profile has been saved."
                    okay_href = '/guests/guests_home'
                    modal_open = True
                
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    guestid = parse_qs(parsed.query)['id'][0]

                    sql0 = """UPDATE guest
                    SET
                        surname = %s,
                        firstname = %s,
                        middlename = %s,
                        address = %s,
                        mobile = %s,
                        email = %s,
                        occupation = %s,
                        nationality = %s,
                        passport = %s,
                        guestdelete = %s
                    WHERE
                        guestid = %s
                    """
                    to_delete = bool(delete)
                    values = [surname, firstname, middlename, address, mobile, email, occupation, nationality, passport, to_delete, guestid]
                    db.modifydatabase(sql0, values)                   

                    feedbackmessage = "Guest profile has been updated."
                    okay_href = '/guests/guests_home'
                    modal_open = True

                else:
                    raise PreventUpdate
            
            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]


@app.callback(
    [
        Output('guestprofile_deletediv', 'style'),
        Output('guestprofile_toload', 'data')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url','search')
    ]
)

def guestprofile_deletediv(pathname, search):
    if pathname =='/guests/guests_guestprofile':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        deletediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [deletediv_style, to_load]

@app.callback(
    [
        Output('guestprofile_surname', 'value'),
        Output('guestprofile_firstname', 'value'),
        Output('guestprofile_middlename', 'value'),
        Output('guestprofile_address', 'value'),
        Output('guestprofile_mobile', 'value'),
        Output('guestprofile_email', 'value'),
        Output('guestprofile_occupation', 'value'),
        Output('guestprofile_nationality', 'value'),
        Output('guestprofile_passport', 'value'),
    ],
    [
        Input('guestprofile_toload','modified_timestamp')
    ],
    [
        State('guestprofile_toload', 'data'),
        State('url', 'search')
    ]
)

def guestprofile_loadprofile (timestamp, toload, search):
    if toload == 1:
        parsed = urlparse(search)
        guestid = parse_qs(parsed.query)['id'][0]
        sql ="""
            Select surname, firstname, middlename, address, mobile, email, occupation, nationality, passport FROM guest
	            Where guestid = %s """
        values = [guestid]
        col = ['surname', 'firstname', 'middlename','address', 'mobile', 'email', 'occupation', 'nationality', 'passport']
        df = db.querydatafromdatabase(sql, values, col)
        surname = (df['surname'][0]) if pd.notna(df['surname'][0]) else None
        firstname = (df['firstname'][0]) if pd.notna(df['firstname'][0]) else None
        middlename = (df['middlename'][0]) if pd.notna(df['middlename'][0]) else None
        address = (df['address'][0]) if pd.notna(df['address'][0]) else None
        mobile = (df['mobile'][0]) if pd.notna(df['mobile'][0]) else None
        email = (df['email'][0]) if pd.notna(df['email'][0]) else None
        occupation = (df['occupation'][0]) if pd.notna(df['occupation'][0]) else None
        nationality = (df['nationality'][0]) if pd.notna(df['nationality'][0]) else None
        passport = (df['passport'][0]) if pd.notna(df['passport'][0]) else None

        return [surname, firstname, middlename, address, mobile, email, occupation, nationality, passport ]
    else:
        raise PreventUpdate
