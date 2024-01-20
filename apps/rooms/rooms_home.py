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
                html.Div([html.H2('Room Types and Rooms', style={'color': '#8A1538','margin-top': '15px'})], style = {'margin-left':'40px','font-weight':'bold','float':'left'}),
                html.Div([dbc.Button("Add New Room", href='/rooms/rooms_profile?mode=add', style={'backgroundColor': '#00573F', 'color': 'white', 
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
                                    dbc.Label("Search Availability", style={'text-align':'right','color': '#000000','font-weight':'bold','margin-left':'10px','font-size':'18px'}, width = 2),
                                    dbc.Col(dcc.DatePickerRange(id = 'roomshome_datepicker', start_date_placeholder_text = 'Check-In', end_date_placeholder_text = 'Check-Out', display_format = "YYYY-MM-DD", clearable = True), style={'text-align':'left'}, width = 3),
                                    dbc.Col(html.Div([dbc.Button("Add New Room Type", href='/rooms/roomtypes_profile?mode=add', style={'backgroundColor': '#00573F', 'color': 'white', 
                                                                                                                                'padding': '10px', 'margin-right':'5px','borderColor':'#00573F',
                                                                                                                                'align-items': 'center'})], style={'float': 'right'}))
                                ],
                                className = 'mb-3',
                            )
                        )
                    ),
                    html.H4("Room Types"),
                    html.Div("Table with room types", id = 'roomshome_list1',style={'background-color':'#ffffff'}),
                ],
            )
        ],
        style={'background-color':'#ffffff','margin-left':'10px','margin-right':'10px'}
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Regular-Twin Rooms"),
                                        html.Div("Table with Regular-Twin Rooms", id = 'roomshome_list2',style={'background-color':'#ffffff'})
                                    ],                                   
                                )
                            ],
                            style={'background-color':'#ffffff','margin-left':'5px'}
                        )
                    ],
                    width=3  
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Regular-Triple Rooms"),
                                        html.Div("Table with Regular-Triple Rooms", id = 'roomshome_list3',style={'background-color':'#ffffff'})
                                    ],                                    
                                )
                            ],
                            style={'background-color':'#ffffff'}
                        )
                    ],
                    width=3 
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Deluxe-Twin Rooms"),
                                        html.Div("Table with Deluxe-Twin Rooms", id = 'roomshome_list4',style={'background-color':'#ffffff'})
                                    ],
                                )
                            ],
                            style={'background-color':'#ffffff'}
                        )
                    ],
                    width=3 
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Presidential Rooms"),
                                        html.Div("Table with Presidential Rooms", id = 'roomshome_list5',style={'background-color':'#ffffff'})
                                    ],
                                )
                            ],
                            style={'background-color':'#ffffff','margin-right':'5px'}
                        )
                    ],
                    width=3  
                )
            ],
            className = "g-1",
            style={
            'background-color': 'transparent'}
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
        Output('roomshome_list1','children')
    ],
    [
        Input('url','pathname')
    ]
)

def loadlist1 (pathname):
    if pathname == '/rooms/rooms_home':    
        sql = """
            select roomtype, maximumoccupants, residentrate, transientrate, roomextensionrate, roomtypeid from roomtype rt
	        where not roomtypedelete
            """
        values = []
        cols = ['Room Type', 'Max PAX', 'Resident Rate', 'Transient Rate', 'Extension Rate', 'ID']
        
        sql += "ORDER BY roomtypeid ASC"
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for roomtype_id in df['ID']:
                buttons += [
                    html.Div(dbc.Button('View Type', href = f'/rooms/roomtypes_profile?mode=edit&id={roomtype_id}', size = 'sm', color = 'warning'), style = {'text-align':'center'})
                ]
            df['Action'] = buttons
            df = df[['Room Type', 'Max PAX', 'Resident Rate', 'Transient Rate', 'Extension Rate', 'Action']]
            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('roomshome_list2','children')
    ],
    [
        Input('url','pathname'),
        Input('roomshome_datepicker', 'start_date'),
        Input('roomshome_datepicker', 'end_date'),
    ]
)

def loadlist2 (pathname, startdate, enddate):
    if pathname == '/rooms/rooms_home':    
        sql = """
            SELECT DISTINCT roomnumber, roomid
            FROM room r
            where not roomdelete
            and roomtypeid=1
            order by roomnumber
            """
        values = []
        cols = ['Room No.', 'ID']

        if startdate and enddate:
            sql = """
            SELECT DISTINCT roomnumber,b.roomid
            FROM room r
            inner join roomtype rt on r.roomtypeid=rt.roomtypeid
            left join booking b on b.roomid = r.roomid
            WHERE roomnumber NOT IN (
                SELECT roomnumber
                FROM roomtype rt
                inner join room r on r.roomtypeid=rt.roomtypeid
                left join booking b on b.roomid = r.roomid
				LEFT JOIN
				(
				SELECT sc.*,
				ROW_NUMBER() OVER (PARTITION BY sc.bookingid ORDER BY sc.statusmodifieddate DESC) AS rn
				FROM statuschange sc
				) AS sc ON b.bookingid = sc.bookingid AND sc.rn = 1
				left join statusname sn on sn.statusnameid=sc.statusnameid
                WHERE not sc.statusnameid=4
				and ((checkindate BETWEEN %s AND %s)
                OR (checkoutdate BETWEEN %s AND %s)
                OR (%s BETWEEN checkindate AND checkoutdate)
                OR (%s BETWEEN checkindate AND checkoutdate))
				and not roomtypedelete and not bookingdelete
            )
            and roomdelete = false
			and r.roomtypeid=1
            """
            values = [startdate, enddate, startdate, enddate, startdate, enddate]
            cols = ['Room No.', 'ID']
            
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for room_id in df['ID']:
                buttons += [
                    html.Div(dbc.Button('View Room', href = f'/rooms/rooms_profile?mode=edit&id={room_id}', size = 'sm', color = 'warning'), style = {'text-align':'center'})
                ]
            df['Action'] = buttons
            df = df[['Room No.', 'Action']]
            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('roomshome_list3','children')
    ],
    [
        Input('url','pathname'),
        Input('roomshome_datepicker', 'start_date'),
        Input('roomshome_datepicker', 'end_date'),
    ]
)

def loadlist3 (pathname, startdate, enddate):
    if pathname == '/rooms/rooms_home':    
        sql = """
            SELECT DISTINCT roomnumber, roomid
            FROM room r
            where not roomdelete
            and roomtypeid=2
            order by roomnumber
            """
        values = []
        cols = ['Room No.', 'ID']

        if startdate and enddate:
            sql = """
            SELECT DISTINCT roomnumber, b.roomid
            FROM room r
            inner join roomtype rt on r.roomtypeid=rt.roomtypeid
            left join booking b on b.roomid = r.roomid
            WHERE roomnumber NOT IN (
                SELECT roomnumber
                FROM roomtype rt
                inner join room r on r.roomtypeid=rt.roomtypeid
                left join booking b on b.roomid = r.roomid
				LEFT JOIN
				(
				SELECT sc.*,
				ROW_NUMBER() OVER (PARTITION BY sc.bookingid ORDER BY sc.statusmodifieddate DESC) AS rn
				FROM statuschange sc
				) AS sc ON b.bookingid = sc.bookingid AND sc.rn = 1
				left join statusname sn on sn.statusnameid=sc.statusnameid
                WHERE not sc.statusnameid=4
				and ((checkindate BETWEEN %s AND %s)
                OR (checkoutdate BETWEEN %s AND %s)
                OR (%s BETWEEN checkindate AND checkoutdate)
                OR (%s BETWEEN checkindate AND checkoutdate))
				and not roomtypedelete and not bookingdelete
            )
            and roomdelete = false
			and r.roomtypeid=2
            """
            values = [startdate, enddate, startdate, enddate, startdate, enddate]
            cols = ['Room No.', 'ID']
            
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for room_id in df['ID']:
                buttons += [
                    html.Div(dbc.Button('View Room', href = f'/rooms/rooms_profile?mode=edit&id={room_id}', size = 'sm', color = 'warning'), style = {'text-align':'center'})
                ]
            df['Action'] = buttons
            df = df[['Room No.', 'Action']]
            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('roomshome_list4','children')
    ],
    [
        Input('url','pathname'),
        Input('roomshome_datepicker', 'start_date'),
        Input('roomshome_datepicker', 'end_date'),
    ]
)

def loadlist4 (pathname, startdate, enddate):
    if pathname == '/rooms/rooms_home':    
        sql = """
            SELECT DISTINCT roomnumber, roomid
            FROM room r
            where not roomdelete
            and roomtypeid=3
            order by roomnumber
            """
        values = []
        cols = ['Room No.', 'ID']

        if startdate and enddate:
            sql = """
            SELECT DISTINCT roomnumber,b.roomid
            FROM room r
            inner join roomtype rt on r.roomtypeid=rt.roomtypeid
            left join booking b on b.roomid = r.roomid
            WHERE roomnumber NOT IN (
                SELECT roomnumber
                FROM roomtype rt
                inner join room r on r.roomtypeid=rt.roomtypeid
                left join booking b on b.roomid = r.roomid
				LEFT JOIN
				(
				SELECT sc.*,
				ROW_NUMBER() OVER (PARTITION BY sc.bookingid ORDER BY sc.statusmodifieddate DESC) AS rn
				FROM statuschange sc
				) AS sc ON b.bookingid = sc.bookingid AND sc.rn = 1
				left join statusname sn on sn.statusnameid=sc.statusnameid
                WHERE not sc.statusnameid=4
				and ((checkindate BETWEEN %s AND %s)
                OR (checkoutdate BETWEEN %s AND %s)
                OR (%s BETWEEN checkindate AND checkoutdate)
                OR (%s BETWEEN checkindate AND checkoutdate))
				and not roomtypedelete and not bookingdelete
            )
            and roomdelete = false
			and r.roomtypeid=3
            """
            values = [startdate, enddate, startdate, enddate, startdate, enddate]
            cols = ['Room No.', 'ID']
            
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for room_id in df['ID']:
                buttons += [
                    html.Div(dbc.Button('View Room', href = f'/rooms/rooms_profile?mode=edit&id={room_id}', size = 'sm', color = 'warning'), style = {'text-align':'center'})
                ]
            df['Action'] = buttons
            df = df[['Room No.', 'Action']]
            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('roomshome_list5','children')
    ],
    [
        Input('url','pathname'),
        Input('roomshome_datepicker', 'start_date'),
        Input('roomshome_datepicker', 'end_date'),
    ]
)

def loadlist5 (pathname, startdate, enddate):
    if pathname == '/rooms/rooms_home':    
        sql = """
            SELECT DISTINCT roomnumber, roomid
            FROM room r
            where not roomdelete
            and roomtypeid=4
            order by roomnumber
            """
        values = []
        cols = ['Room No.', 'ID']

        if startdate and enddate:
            sql = """
            SELECT DISTINCT roomnumber,b.roomid
            FROM room r
            inner join roomtype rt on r.roomtypeid=rt.roomtypeid
            left join booking b on b.roomid = r.roomid
            WHERE roomnumber NOT IN (
                SELECT roomnumber
                FROM roomtype rt
                inner join room r on r.roomtypeid=rt.roomtypeid
                left join booking b on b.roomid = r.roomid
				LEFT JOIN
				(
				SELECT sc.*,
				ROW_NUMBER() OVER (PARTITION BY sc.bookingid ORDER BY sc.statusmodifieddate DESC) AS rn
				FROM statuschange sc
				) AS sc ON b.bookingid = sc.bookingid AND sc.rn = 1
				left join statusname sn on sn.statusnameid=sc.statusnameid
                WHERE not sc.statusnameid=4
				and ((checkindate BETWEEN %s AND %s)
                OR (checkoutdate BETWEEN %s AND %s)
                OR (%s BETWEEN checkindate AND checkoutdate)
                OR (%s BETWEEN checkindate AND checkoutdate))
				and not roomtypedelete and not bookingdelete
            )
            and roomdelete = false
			and r.roomtypeid=4
            """
            values = [startdate, enddate, startdate, enddate, startdate, enddate]
            cols = ['Room No.', 'ID']
            
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for room_id in df['ID']:
                buttons += [
                    html.Div(dbc.Button('View Room', href = f'/rooms/rooms_profile?mode=edit&id={room_id}', size = 'sm', color = 'warning'), style = {'text-align':'center'})
                ]
            df['Action'] = buttons
            df = df[['Room No.', 'Action']]
            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate