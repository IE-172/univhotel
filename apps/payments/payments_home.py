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
        html.Div([
                html.Div([html.H2('Payment Records', style={'color': '#8A1538','margin-top': '15px'})], style = {'margin-left':'40px','font-weight':'bold','float':'left'}),
                html.Div([dbc.Button("Add New Payment", href='/payments/payments_profile?mode=add', style={'backgroundColor': '#00573F', 'color': 'white', 
                                                                                                       'padding': '10px', 'margin-right':'20px','borderColor':'#00573F',
                                                                                                       'align-items': 'center','margin-top': '10px'})], style={'float': 'right'})
        ],
        style={
            'background-color': 'transparent'}
                 ),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Card(
            [
            dbc.CardBody(
                [
                    html.Div(
                        dbc.Form(
                            dbc.Row(
                                [
                                    dbc.Label("Search by Guest Name", style={'text-align':'right','color': '#000000','font-weight':'bold','margin-left':'10px','font-size':'18px'}, width = 2),
                                    dbc.Col(dbc.Input(id = 'paymentshome_guestfilter', placeholder = 'Guest Lastname', type = 'text'), style={'text-align':'left'}, width = 2),
                                    dbc.Col(width = 2),
                                    dbc.Label("Search by Check-in Date", style={'text-align':'right','color': '#000000','font-weight':'bold', 'font-size':'18px'}, width = 2),
                                    dbc.Col(dcc.DatePickerSingle(id = 'paymentshome_datepicker', placeholder = 'YYYY/MM/DD', display_format = "YYYY-MM-DD", clearable= True), style={'text-align':'left'}, width = 2) 
                                ],
                                className = 'mb-3'
                            )
                        )
                    ),
                    html.Hr(),
                    html.Div(
                        [
                            html.H4("Initial Deposit and Partial Payments"),
                        ]
                    ),
                    html.Div("Table with Payments", id = 'paymentshome_paymentslist1'),
                    html.Hr(),
                    html.Div(
                        [
                            html.H4("Full Payments"),
                        ]
                    ),
                    html.Div("Table with Payments", id = 'paymentshome_paymentslist2'),
                ],
            )
        ],
        style={'background-color':'#ffffff','margin-left':'10px','margin-right':'10px'}
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
        Output('paymentshome_paymentslist1','children')
    ],
    [
        Input('url','pathname'),
        Input('paymentshome_guestfilter', 'value'),
        Input('paymentshome_datepicker', 'date'),
    ]
)

def loadpaymentlist1 (pathname, searchterm, checkindate):
    if pathname == '/payments/payments_home':    
        sql = """
            Select 
	            roomnumber, 
	            surname, 
	            concat(checkindate,' - ',checkoutdate) as duration, 
	            totalamount, 
	            deposit, 
	            balance, 
	            paymenttype,
                paymentid 
	            from payment p 
		        inner join booking b on b.bookingid = p.bookingid
		        inner join guest g on g.guestid = b.guestid
		        inner join paymenttype pt on pt.paymenttypeid = p.paymenttypeid
		        inner join room r on r.roomid = b.roomid
	            where not bookingdelete and not paymentdelete
                and p.paymenttypeid in (1,2)
            """
        values = []
        cols = ['Room No.', 'Guest', 'Duration', 'Total Amount', 'Deposit', 'Balance', 'Type', 'ID']

        if searchterm:
            sql += "AND surname ILIKE %s"
            values += [f"%{searchterm}%"]
        
        if checkindate:
            sql += """AND checkindate = %s"""
            values += [f"%{checkindate}%"]
        
        sql += "ORDER BY roomnumber ASC"
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for payment_id in df['ID']:
                buttons += [
                    html.Div(dbc.Button('View Payment', href = f'/payments/payments_profile?mode=edit&id={payment_id}', size = 'sm', color = 'warning'), style = {'text-align':'center'})
                ]
            df['Action'] = buttons
            df = df[['Room No.', 'Guest', 'Duration', 'Total Amount', 'Deposit', 'Balance', 'Type', 'Action']]
            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('paymentshome_paymentslist2','children')
    ],
    [
        Input('url','pathname'),
        Input('paymentshome_guestfilter', 'value'),
        Input('paymentshome_datepicker', 'date'),
    ]
)

def loadpaymentlist2 (pathname, searchterm, checkindate):
    if pathname == '/payments/payments_home':    
        sql = """
            Select 
	            roomnumber, 
	            surname, 
	            concat(checkindate,' - ',checkoutdate) as duration, 
	            totalamount, 
	            deposit, 
	            balance, 
	            paymenttype,
                paymentid 
	            from payment p 
		        inner join booking b on b.bookingid = p.bookingid
		        inner join guest g on g.guestid = b.guestid
		        inner join paymenttype pt on pt.paymenttypeid = p.paymenttypeid
		        inner join room r on r.roomid = b.roomid
	            where not bookingdelete and not paymentdelete
                and p.paymenttypeid in (3)
            """
        values = []
        cols = ['Room No.', 'Guest', 'Duration', 'Total Amount', 'Deposit', 'Balance', 'Type', 'ID']

        if searchterm:
            sql += "AND surname ILIKE %s"
            values += [f"%{searchterm}%"]
        
        if checkindate:
            sql += """AND checkindate = %s"""
            values += [f"%{checkindate}%"]
        
        sql += "ORDER BY roomnumber ASC"
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for payment_id in df['ID']:
                buttons += [
                    html.Div(dbc.Button('View Payment', href = f'/payments/payments_profile?mode=edit&id={payment_id}', size = 'sm', color = 'warning'), style = {'text-align':'center'})
                ]
            df['Action'] = buttons
            df = df[['Room No.', 'Guest', 'Duration', 'Total Amount', 'Deposit', 'Balance', 'Type', 'Action']]
            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate