import hashlib

import dash_bootstrap_components as dbc
from dash import callback_context, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardImg(src=r'assets/univhotellogo.jpeg', top=True),
                dbc.CardBody(
                    [
                        dbc.Alert('Username or password is incorrect.', color="danger", id='login_alert', is_open=False),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Input(type="text", id="login_username", placeholder="username")),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Input(type="password", id="login_password", placeholder="password")),
                            ],
                            className="mb-3",
                        ),
                        html.H6("Forgotten your username or password?", style={'textAlign': 'center'}),
                        html.H6("Contact an admin for assistance.", style={'textAlign': 'center'}),
                        html.Br(),
                        dbc.Button('Log in', id='login_loginbtn', style={'backgroundColor': '#00573F', 'color': 'white'}, className="d-grid gap-2 col-6 mx-auto"),
                        
                    ]
                ),
            ],
            style = {'position':'static', 'transform':'translate(115%, 5%)', 'width':'30%'}
        ),  
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br()
    ]
)


@app.callback(
    [
        Output('login_alert', 'is_open'),
        Output('currentuserid', 'data'),
    ],
    [
        Input('login_loginbtn', 'n_clicks'), 
        Input('sessionlogout', 'modified_timestamp'),
    ],
    [
        State('login_username', 'value'),
        State('login_password', 'value'),   
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'), 
        State('url', 'pathname'), 
    ]
)
def loginprocess(loginbtn, sessionlogout_time, username, password, sessionlogout, currentuserid, pathname):
    
    ctx = callback_context
    
    if ctx.triggered:
        openalert = False
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
    
    
    if eventid == 'login_loginbtn': 
    
        if loginbtn and username and password:
                
            if username == 'admin' and password == 'password':
                currentuserid = 999  
            
            else:
                sql = """SELECT staffid
                FROM staff
                WHERE 
                    staffusername = %s 
                    AND staffpassword = %s
                    AND NOT staffdelete
                """
                
                encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest() 
                
                values = [username, encrypt_string(password)]
                cols = ['staffid']
                df = db.querydatafromdatabase(sql, values, cols)
                
                if df.shape[0]: # if query returns rows
                    currentuserid = df['staffid'][0]
                    sql = """
                        UPDATE staff
                        SET
                            staffactive = true
                        WHERE
                            staffid = %s"""
                    values = [f"{currentuserid}"]
                    db.modifydatabase(sql,values)

                else:
                    currentuserid = -1
                    openalert = True
                
    elif eventid == 'sessionlogout' and pathname == '/logout': # reset the userid if logged out
        currentuserid = -1
        sql = "UPDATE staff SET staffactive = False"
        values = []
        db.modifydatabase(sql,values)
        
    else:
        raise PreventUpdate
    
    return [openalert, currentuserid]


@app.callback(
    [
        Output('url', 'pathname'),
    ],
    [
        Input('currentuserid', 'modified_timestamp'),
    ],
    [
        State('currentuserid', 'data'), 
    ]
)
def routelogin(logintime, userid):
    ctx = callback_context
    if ctx.triggered:
        if userid > 0:
            url = '/home'
        else:
            url = '/'
    else:
        raise PreventUpdate
    return [url]




