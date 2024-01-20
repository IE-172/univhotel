#new layout

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
                html.Div([html.H2('Guest Bookings', style={'color': '#8A1538','margin-top': '15px'})], style = {'margin-left':'40px','font-weight':'bold','float':'left'}),
                html.Div([dbc.Button("Add New Booking", href='/bookings/bookings_profile?mode=add', style={'backgroundColor': '#00573F', 'color': 'white', 
                                                                                                       'padding': '10px', 'margin-right':'20px','borderColor':'#00573F',
                                                                                                       'align-items': 'center','margin-top': '10px'})], style={'float': 'right'})
        ]),
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
                                    dbc.Label("Search Guest Booking", style={'text-align':'right','color': '#000000','font-weight':'bold','margin-top': '0px'}, width = 2),
                                    dbc.Col(dbc.Input(id = 'bookingshome_guestfilter', placeholder = 'Guest Last Name', type = 'text'), style={'text-align':'left','margin-top': '5px'}, width = 2),
                                    dbc.Col(width = 3),
                                    dbc.Label("Booking Date Range", style={'text-align':'right','color': '#000000','font-weight':'bold','margin-right':'0px'}, width = 2),
                                    dbc.Col(dcc.DatePickerRange(id = 'bookingshome_datepicker', start_date_placeholder_text = 'Check-In', end_date_placeholder_text = 'Check-Out', display_format = "YYYY-MM-DD", clearable = True), style={'text-align':'left'}, width = 3)
                                ],
                                className = 'mb-3'
                            )
                        )
                    ),
                    html.Div("Table with Bookings", id = 'bookingshome_bookingslist'),
                ],
                style={'background-color':'#ffffff','margin-left':'20px','margin-right':'20px'}
            )
        ],
        style={
        'background-color': 'transparent'
        }    
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
        Output('bookingshome_bookingslist','children')
    ],
    [
        Input('url','pathname'),
        Input('bookingshome_guestfilter', 'value'),
        Input('bookingshome_datepicker', 'start_date'),
        Input('bookingshome_datepicker', 'end_date'),
    ]
)

def loadbookinglist (pathname, searchterm, checkindate, checkoutdate):
    if pathname == '/bookings/bookings_home':    
        sql = """SELECT roomnumber, surname, numberofoccupants, checkindate, checkoutdate, statusname, b.bookingid
            FROM booking b
                INNER JOIN room r ON b.roomid = r.roomid
                INNER JOIN guest gst ON b.guestid = gst.guestid
                LEFT JOIN
                    (
                    SELECT sc.*,
                    ROW_NUMBER() OVER (PARTITION BY sc.bookingid ORDER BY sc.statusmodifieddate DESC) AS rn
                    FROM statuschange sc
                    ) AS sc ON b.bookingid = sc.bookingid AND sc.rn = 1
                INNER JOIN statusname sn ON sc.statusnameid = sn.statusnameid
                WHERE NOT bookingdelete 
            """
        values = []
        cols = ['Room No.', 'Guest', 'PAX', 'Check-In Date', 'Check-Out Date', 'Status', 'Booking ID']

        if searchterm:
            sql += "AND surname ILIKE %s"
            values += [f"%{searchterm}%"]
        
        if checkindate:
            sql += """AND checkoutdate >= %s"""
            values += [f"%{checkindate}%"]

        if checkoutdate:
            sql += """AND checkindate <= %s"""
            values += [f"%{checkoutdate}%"]
        
        sql += "ORDER BY r.roomnumber ASC"
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for booking_id in df['Booking ID']:
                buttons += [
                    html.Div(dbc.Button('View Booking', href = f'/bookings/bookings_profile?mode=edit&id={booking_id}', size = 'sm', color = 'warning'), style = {'text-align':'center'})
                ]
            df['Action'] = buttons
            df = df[['Room No.', 'Guest', 'PAX', 'Check-In Date', 'Check-Out Date', 'Status', 'Action']]
            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate



