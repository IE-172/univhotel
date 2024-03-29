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
            dcc.Store(id = 'discountprofile_toload', storage_type = 'memory', data = 0)
        ]),
        html.Div([html.H2('Discount Details', style={'color': '#8A1538','margin-left':'25px'})], style = {'float':'left'}),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dbc.Alert(id = 'discountprofile_alert', is_open = False),
                        html.H4("Discount Information", style={'margin-left':'15px'}),
                        html.P("Fields marked with '*' are required.", style={'color': 'red', 'margin-left':'15px'}),
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label(html.Div(["Discount Type", html.Span("*", style={'color': 'red'})]), style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.Input(id ='discountprofile_discounttype', type = 'text', placeholder = 'Enter Discount Type'), style={'text-align':'left'},width = 4)
                                    ],
                                    className = 'mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label(html.Div(["Discount Percentage", html.Span("*", style={'color': 'red'})]),  style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.InputGroup([dbc.Input(id ='discountprofile_percentage', type = 'text', placeholder = 'Enter Percentage'), dbc.InputGroupText("%")]),style={'text-align':'left'},width = 4)
                                    ],
                                    className = 'mb-3'
                                ),
                                html.Hr(),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Label("Delete discount?", style={'margin-left':'15px'},width = 2),
                                                dbc.Col(dbc.Checklist(id = 'discountprofile_delete', inline = True, switch =True, value = 0, options = [{"label":"Mark as deleted","value":1}]), width = 4)
                                            ],
                                            className = 'mb-3'
                                        )
                                    ],
                                    id = 'discountprofile_deletediv'
                                ),
                                html.Div(dbc.Button('Save Discount', id = 'discountprofile_save', n_clicks=0, style={'backgroundColor': '#00573F', 'color': 'white', 'borderColor':'#00573F'}), className="d-grid gap-2 col-6 mx-auto"),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(html.H4("Discount Saved")),
                                        dbc.ModalBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        #update once modal is working
                                                    ],
                                                    id = 'discountprofile_feedbackmessage',
                                                    style={'margin-left': '1px'}
                                                )
                                            ]
                                        ),
                                        dbc.ModalFooter(
                                            [
                                                dbc.Button("Proceed", href = '/discounts/discounts_home', id = 'discountprofile_btnmodal')
                                            ]
                                        )
                                    ],
                                    centered = True,
                                    id = 'discountprofile_successmodal',
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
            Output('discountprofile_alert', 'color'),
            Output('discountprofile_alert', 'children'),
            Output('discountprofile_alert','is_open'),

            Output('discountprofile_successmodal','is_open'),
            Output('discountprofile_feedbackmessage', 'children'),
            Output('discountprofile_btnmodal', 'href')
        ],
        [
            Input('discountprofile_save', 'n_clicks'),
            Input('discountprofile_btnmodal', 'n_clicks')
        ],
        [
            State('discountprofile_discounttype', 'value'),
            State('discountprofile_percentage', 'value'),
            State('url', 'search'),
            State('discountprofile_delete', 'value')
        ]
)

def discountprofile_saveprofile (submitbtn, closebtn, discounttype, percent, search, delete):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'discountprofile_save' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            feedbackmessage = ''
            okay_href = ''

            if not discounttype:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply discount type.'
            elif not percent:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply percentage.'
            else:
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]

                if create_mode == 'add':
                    
                    sql0="""INSERT INTO discount(
                        discounttype, discountpercentage, discountdelete
                    )
                    VALUES(%s, %s, %s)
                    """
                    values = [discounttype, percent, False]
                    db.modifydatabase(sql0, values)

                    feedbackmessage = "Discount has been saved."
                    okay_href = '/discounts/discounts_home'
                    modal_open = True
                
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    discountid = parse_qs(parsed.query)['id'][0]

                    sql0 = """UPDATE discount
                    SET
                        discounttype = %s,
                        discountpercentage = %s,
                        discountdelete = %s
                    WHERE
                        discountid = %s
                    """
                    to_delete = bool(delete)
                    values = [discounttype, percent, to_delete, discountid]
                    db.modifydatabase(sql0, values)                   

                    feedbackmessage = "Discount has been updated."
                    okay_href = '/discounts/discounts_home'
                    modal_open = True

                else:
                    PreventUpdate
            
            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]


@app.callback(
    [
        Output('discountprofile_deletediv', 'style'),
        Output('discountprofile_toload', 'data')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url','search')
    ]
)

def discountprofile_deletediv(pathname, search):
    if pathname =='/discounts/discounts_profile':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        deletediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [deletediv_style, to_load]

@app.callback(
    [
        Output('discountprofile_discounttype', 'value'),
        Output('discountprofile_percentage', 'value'),
    ],
    [
        Input('discountprofile_toload','modified_timestamp')
    ],
    [
        State('discountprofile_toload', 'data'),
        State('url', 'search')
    ]
)

def discountprofile_loadprofile (timestamp, toload, search):
    if toload == 1:
        parsed = urlparse(search)
        discountid = parse_qs(parsed.query)['id'][0]
        sql ="""
            Select discounttype, discountpercentage FROM discount
	            Where discountid = %s """
        values = [discountid]
        col = ['Discount Type', '%']
        df = db.querydatafromdatabase(sql, values, col)
        discounttype = (df['Discount Type'][0]) if pd.notna(df['Discount Type'][0]) else None
        percentage = (df['%'][0]) if pd.notna(df['%'][0]) else None

        return [discounttype, percentage]
    else:
        raise PreventUpdate
