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
        html.Div([
            dcc.Store(id = 'staffprofile_toload', storage_type = 'memory', data = 0)
        ]),
        html.Div([html.H2('Staff Details', style={'color': '#8A1538','margin-top': '15px'})], style = {'margin-left':'40px','font-weight':'bold','float':'left'}),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dbc.Alert(id = 'staffprofile_alert', color="danger", is_open=False),
                        html.H4(("Personal Information"), style={'margin-left':'15px'}),
                        html.P("Fields marked with '*' are required.", style={'margin-left':'15px', 'color': 'red'}),
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label(html.Div(["Staff Name", html.Span("*", style={'color': 'red'})],style={'margin-left':'15px'}), width=2),
                                        dbc.Col(dbc.Input(id ='staffprofile_lastname', type = 'text', placeholder = 'Last Name', invalid=False), width = 2),
                                        dbc.Col(dbc.Input(id ='staffprofile_firstname', type = 'text', placeholder = 'First Name', invalid=False), width = 2),
                                    ],
                                    className = 'mb-3'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.H4("Log-In Credentials", style={'margin-left':'15px'}),
                        html.P("Fields marked with '*' are required.", style={'margin-left':'15px', 'color': 'red'}),
                        dbc.Row(
                            [
                                dbc.Label(html.Div(["Username", html.Span("*", style={'color': 'red'})],style={'margin-left':'15px'}), width=2),
                                dbc.Col(dbc.Input(type="text", id="staffprofile_username", placeholder="Enter a username", invalid=False), width=4),
                            ],
                            className="mb-3"
                        ),
                        dbc.Row(
                            [
                                dbc.Label(html.Div(["New Password", html.Span("*", style={'color': 'red'})],style={'margin-left':'15px'}), width=2),
                                dbc.Col(dbc.Input(type="password", id="staffprofile_password", placeholder="Enter a password", valid=False, invalid=False), width=4),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Label(html.Div(["Confirm Password", html.Span("*",  style={'color': 'red'})],style={'margin-left':'15px'}),width=2),
                                dbc.Col( dbc.Input(type="password", id="staffprofile_passwordconf", placeholder="Re-type the password", valid=False, invalid=False), width=4),
                            ],
                            className="mb-3",
                        ),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label("Assign Access", style={'color': '#000000', 'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.RadioItems(id = 'staffprofile_admin', inline = True, value = 1, options = [{"label":"Regular","value":1},{"label":"Admin","value":2}]), style={'text-align':'center'}, width = 4)
                                    ],
                                    className = 'mb-3'
                                )
                            ],
                        ),
html.Hr(),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label("Remove staff?", style={'margin-left':'15px'},width = 2),
                                        dbc.Col(dbc.Checklist(id = 'staffprofile_delete', inline = True, switch =True, value = 0, options = [{"label":"Mark as removed","value":1}]), width = 4)
                                    ],
                                    className = 'mb-3'
                                )
                            ],
                            id = 'staffprofile_deletediv'
                        ),
                        html.Div(dbc.Button('Save Staff Details', id = 'staffprofile_save', n_clicks=0, style={'backgroundColor': '#00573F', 'color': 'white', 'borderColor':'#00573F'}), className="d-grid gap-2 col-6 mx-auto"),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H4("Staff Profile Saved")),
                                dbc.ModalBody(
                                    [
                                        dbc.Row(
                                            [
                                                #update once modal is working
                                            ],
                                            id = 'staffprofile_feedbackmessage',
                                            style={'margin-left': '1px'}
                                        )
                                    ]
                                ),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Proceed", href = '/staff/login_home', id = 'staffprofile_btnmodal')
                                    ]
                                )
                            ],
                            centered = True,
                            id = 'staffprofile_successmodal',
                            backdrop = 'static'
                        )    
                    ]
                )
            ],
            style={'background-color':'#ffffff','margin-left':'20px','margin-right':'20px'}
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
        Output('staffprofile_lastname', 'invalid'),
        Output('staffprofile_firstname', 'invalid'),
        Output('staffprofile_username', 'invalid'),

        Output('staffprofile_password', 'valid'),
        Output('staffprofile_password', 'invalid'),
        Output('staffprofile_passwordconf', 'valid'),
        Output('staffprofile_passwordconf', 'invalid'),
        Output('staffprofile_save', 'disabled'),
    ],
    [
        Input('staffprofile_lastname', 'value'),
        Input('staffprofile_firstname', 'value'),
        Input('staffprofile_username', 'value'),
        Input('staffprofile_password', 'value'),
        Input('staffprofile_passwordconf', 'value'),
    ],
    [
        State('url', 'search')
    ]
)

def validateinput(lastname, firstname, username, password, passwordconf, search):
    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query)['mode'][0]

    if create_mode == 'add':
        if not lastname and not firstname and not username and not password and not passwordconf:
            invalid_lastname = False
            invalid_firstname = False
            invalid_username = False
            valid_password = False
            invalid_password = False
            enablebtn = False

        else:
            invalid_lastname = not lastname
            invalid_firstname = not firstname
            invalid_username = not username
            valid_password = password and passwordconf and password == passwordconf
            invalid_password = not valid_password
            enablebtn = password and passwordconf and valid_password
            
    elif create_mode == 'edit':
        if password or passwordconf:
            invalid_lastname = not lastname
            invalid_firstname = not firstname
            invalid_username = not username
            valid_password = password and passwordconf and password == passwordconf
            invalid_password = not valid_password
            enablebtn = password and passwordconf and valid_password
        else:
            invalid_lastname = not lastname
            invalid_firstname = not firstname
            invalid_username = not username
            valid_password = False
            invalid_password = False
            enablebtn = True

    else:
        raise PreventUpdate

    return [invalid_lastname, invalid_firstname, invalid_username, valid_password, invalid_password, valid_password, invalid_password, not enablebtn]




@app.callback(
    [
        Output('staffprofile_alert', 'color'),
        Output('staffprofile_alert', 'children'),
        Output('staffprofile_alert','is_open'),

        Output('staffprofile_successmodal','is_open'),
        Output('staffprofile_feedbackmessage', 'children'),
        Output('staffprofile_btnmodal', 'href')  
    ],
    [
        Input('staffprofile_save', 'n_clicks'),
        Input('staffprofile_btnmodal', 'n_clicks')
    ],
    [
        State('staffprofile_lastname', 'value'),
        State('staffprofile_firstname', 'value'),
        State('staffprofile_username', 'value'),
        State('staffprofile_password', 'value'),
        State('url', 'search'),
        State('staffprofile_admin','value'),
        State('staffprofile_delete', 'value')
    ]
)
def saveuser(submitbtn, closebtn,lastname, firstname, username, password, search, admin, delete):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'staffprofile_save' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            feedbackmessage = ''
            okay_href = ''
        
        if not lastname:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Please supply staff last name.'
        elif not firstname:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Please supply staff first name.'
        elif not username:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Please supply staff username.'
        else:
            parsed = urlparse(search)
            create_mode = parse_qs(parsed.query)['mode'][0]
            
            if create_mode == 'add':

                sql0="""INSERT INTO staff(
                        stafflastname, stafffirstname, staffusername, staffpassword, staffaccess
                    )
                    VALUES(%s, %s, %s, %s, %s)
                    """
                
                encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()  
                if admin == 2:
                    to_assign = True
                else:
                    to_assign = False

                values = [lastname, firstname, username, encrypt_string(password), to_assign]
                try:
                    db.modifydatabase(sql0, values)
                except Exception:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Username already exists.'
                    return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

                feedbackmessage = "Staff credentials have been added."
                okay_href = '/staff/login_home'
                modal_open = True

            elif create_mode == 'edit':

                parsed = urlparse(search)
                staffid = parse_qs(parsed.query)['id'][0]

                sql0 = """UPDATE staff
                    SET
                        stafflastname = %s,
                        stafffirstname = %s,
                        staffusername = %s,
                        staffaccess = %s,
                        staffdelete = %s
                    WHERE
                        staffid = %s
                    """
                to_delete = bool(delete)
                if admin == 2:
                    to_assign = True
                else:
                    to_assign = False

                values = [lastname, firstname, username, to_assign, to_delete, staffid]
                try:
                    db.modifydatabase(sql0, values)
                except Exception:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Username already exists.'
                    return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

                if password:
                    sql1="""UPDATE staff
                        SET
                            staffpassword = %s
                        WHERE
                            staffid = %s
                        """
                
                    encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()  
                    values = [encrypt_string(password), staffid]
                    db.modifydatabase(sql1, values)

                feedbackmessage = "Staff credentials have been updated"
                okay_href = '/staff/login_home'
                modal_open = True

            else:
                PreventUpdate
            
        return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

@app.callback(
    [
        Output('staffprofile_deletediv', 'style'),
        Output('staffprofile_toload', 'data')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url','search')
    ]
)

def staffprofile_deletediv(pathname, search):
    if pathname =='/staff/login_credentials':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        deletediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [deletediv_style, to_load]

@app.callback(
    [
        Output('staffprofile_lastname', 'value'),
        Output('staffprofile_firstname', 'value'),
        Output('staffprofile_username', 'value'),
        Output('staffprofile_admin', 'value')
    ],
    [
        Input('staffprofile_toload','modified_timestamp')
    ],
    [
        State('staffprofile_toload', 'data'),
        State('url', 'search')
    ]
)

def staffprofile_loadprofile (timestamp, toload, search):
    if toload == 1:
        parsed = urlparse(search)
        staffid = parse_qs(parsed.query)['id'][0]
        sql ="""
            Select stafflastname, stafffirstname, staffusername, staffaccess FROM staff
	            Where staffid = %s """
        values = [staffid]
        col = ['lastname', 'firstname', 'username', 'access']
        df = db.querydatafromdatabase(sql, values, col)
        lastname = (df['lastname'][0]) if pd.notna(df['lastname'][0]) else None
        firstname = (df['firstname'][0]) if pd.notna(df['firstname'][0]) else None
        username = (df['username'][0]) if pd.notna(df['username'][0]) else None
        access = (df['access'][0]) if pd.notna(df['access'][0]) else None

        to_access = 2 if access == True else 1

        return [lastname, firstname, username, to_access]
    else:
        raise PreventUpdate
