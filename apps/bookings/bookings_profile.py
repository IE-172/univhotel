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
            dcc.Store(id = 'bookingprofile_toload', storage_type = 'memory', data = 0)
        ]),
        html.Div([html.H2('Booking Details', style={'margin-left':'25px', 'color': '#8A1538'})], style = {'float':'left'}),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dbc.Alert(id = 'bookingprofile_alert', is_open = False),
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label(html.Div(["Booking Status", html.Span("*", style={'color': 'red'})]),  style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dcc.Dropdown(id = 'bookingprofile_statusname', placeholder = "Select Status"),  style={'text-align':'left'}, width = 5)
                                    ],
                                    className = 'mb-3'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.H4("Guest Information",style={'margin-left':'15px'}),
                        html.P("Fill-in basic information about the guest. If record doesn't exist, proceed to 'Add New Record'.",style={'margin-left':'15px'}),
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label(html.Div(["Guest Name", html.Span("*", style={'color': 'red'})]), style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dcc.Dropdown(id = 'bookingprofile_guestname', placeholder = "Select Guest"),  style={'text-align':'left'}, width = 3),
                                        dbc.Col([dbc.Button("Add New Guest Record", color = "secondary", href = '/guests/guests_guestprofile?mode=add')]),
                                    ],
                                    className = 'mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Group Name",  style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dcc.Dropdown(id = 'bookingprofile_groupname', placeholder = "Select Group"), style={'text-align':'left'}, width = 3),
                                        dbc.Col([dbc.Button("Add New Group Record", color = "secondary", href = '/guests/guests_groupprofile?mode=add')]),
                                    ],
                                    className = 'mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label(html.Div(["No. of Occupants", html.Span("*", style={'color': 'red'})]), style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.InputGroup([dbc.Input(id = 'bookingprofile_occupants', placeholder="0", type="number", min = 1, step = 1),dbc.InputGroupText("Adult/s")]), style={'text-align':'left'}, width = 3),
                                        dbc.Label("Discount Type", style={'margin-left':'15px'}, width =2),
                                        dbc.Col(dcc.Dropdown(id = 'bookingprofile_discount', placeholder = "Select Discount Type"), style={'text-align':'left'},  width = 3)

                                    ],
                                    className = 'mb-3'
                                ),
                            ]
                        ),
                        html.Hr(),
                        html.H4("Booking Information", style={'margin-left':'15px'}),
                        html.P("Fill-in information about the booking.", style={'margin-left':'15px'}),
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label(html.Div(["Rate Type", html.Span("*", style={'color': 'red'})]), style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.RadioItems(id = 'bookingprofile_ratetype', inline = True, value = 1, options = [{"label":"Resident","value":1},{"label":"Transient","value":2}]), style={'text-align':'left'}, width=3),
                                        dbc.Label(html.Div(["Booking Duration", html.Span("*", style={'color': 'red'})]),  style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dcc.DatePickerRange(id = 'bookingprofile_datepicker', start_date_placeholder_text = 'Check-In', end_date_placeholder_text = 'Check-Out', display_format = "YYYY-MM-DD"),  style={'text-align':'left'}, width = 3)
                                    ],
                                    className = 'mb-3', align = 'center'
                                ),
                               dbc.Row(
                                    [
                                        dbc.Label(html.Div(["Room Type", html.Span("*", style={'color': 'red'})]), style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dcc.Dropdown(id = 'bookingprofile_roomtype', placeholder = "Select Room Type"),{'text-align':'left'}, width = 3),
                                        dbc.Label(html.Div(["Room No.", html.Span("*", style={'color': 'red'})]),  style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dcc.Dropdown(id = 'bookingprofile_roomnumber', placeholder = "Select Room Number"), {'text-align':'left'},width = 3)
                                    ],
                                    className = 'mb-3'
                                ),
                                html.P("Fill-up right after guest check-in and check-out.", style={'margin-left':'15px'}),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Label("Arrival Time",style={'margin-left':'15px'}, width = 2),
                                                dbc.Col(
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(dbc.Input(id='bookingprofile_arrivalhours', type="text", placeholder ="HH"), {'text-align':'left'}), 
                                                            dbc.Col(dbc.Label(":"), width=1, style={'line-height': '38px', 'text-align': 'center'}),
                                                            dbc.Col(dbc.Input(id='bookingprofile_arrivalmins', type="text", placeholder ="MM"), {'text-align':'left'}), 
                                                            dbc.Col(dbc.Label(":"), width=1, style={'line-height': '38px', 'text-align': 'center'}),
                                                            dbc.Col(dbc.Input(id='bookingprofile_arrivalsecs', type="text", placeholder ="SS"), {'text-align':'left'})
                                                        ], 
                                                        className = 'g-0'
                                                    ), 
                                                    width = 3
                                                ),
                                            ],
                                            className = 'mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Departure Time", style={'margin-left':'15px'}, width = 2),
                                                dbc.Col(
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(dbc.Input(id='bookingprofile_departurehours', type="text", placeholder ="HH"), style={'text-align':'left'}), 
                                                            dbc.Col(dbc.Label(":"), width=1, style={'line-height': '38px', 'text-align': 'center'}),
                                                            dbc.Col(dbc.Input(id='bookingprofile_departuremins', type="text", placeholder ="MM"), style={'text-align':'left'}), 
                                                            dbc.Col(dbc.Label(":"), width=1, style={'line-height': '38px', 'text-align': 'center'}),
                                                            dbc.Col(dbc.Input(id='bookingprofile_departuresecs', type="text", placeholder ="SS"), style={'text-align':'left'})
                                                        ], 
                                                        className = 'g-0'
                                                    ), 
                                                    width = 3
                                                ),
                                            ],
                                            className = 'mb-3'
                                        )
                                    ],
                                    id = 'bookingprofile_timediv'    
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label("Delete booking?", style={'margin-left':'15px'}, width = 2),
                                        dbc.Col(dbc.Checklist(id = 'bookingprofile_delete', inline = True, switch =True, value = 0, options = [{"label":"Mark as deleted","value":1}]), {'text-align':'left'}, width = 4)
                                    ],
                                    className = 'mb-3'
                                )
                            ],
                            id = 'bookingprofile_deletediv'
                        ),
                        html.Div(dbc.Button('Save Booking', id = 'bookingprofile_save', n_clicks=0, style={'backgroundColor': '#00573F', 'color': 'white', 'borderColor':'#00573F'}), className="d-grid gap-2 col-6 mx-auto"),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H4("Booking Saved")),
                                dbc.ModalBody(
                                    [
                                        html.H6("Here is a summary of the booking:"),
                                        dbc.Row(
                                            [
                                                #update once modal is working
                                            ],
                                            id = 'bookingprofile_feedbackmessage',
                                            style={'margin-left': '1px'}
                                        )
                                    ]
                                ),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Proceed", href = '/bookings/bookings_home', id = 'bookingprofile_btnmodal')
                                    ]
                                )
                            ],
                            centered = True,
                            id = 'bookingprofile_successmodal',
                            backdrop = 'static'
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
        Output('bookingprofile_statusname','options'),
        Output('bookingprofile_guestname', 'options'),
        Output('bookingprofile_groupname', 'options'),
        Output('bookingprofile_discount','options'),
        Output('bookingprofile_roomtype', 'options')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)

def bookingprofile_loaddropdowns (pathname, search):
    if pathname == '/bookings/bookings_profile':
        sql1 = """
        SELECT statusname as label, statusnameid as value FROM statusname
        WHERE NOT statusnamedelete """
        values1 = []
        cols1 = ['label', 'value']
        df1 = db.querydatafromdatabase(sql1, values1, cols1)
        statusname_options = df1.to_dict('records')

        sql = """
        SELECT CONCAT(surname,', ', firstname, ' ', middlename) as label, guestid as value FROM guest
        WHERE NOT guestdelete
        ORDER BY surname ASC"""
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        guestname_options = df.to_dict('records')

        sql = """
        SELECT groupguestname as label, groupguestid as value FROM groupguest
        WHERE NOT groupguestdelete
        ORDER BY groupguestname ASC"""
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        groupname_options = df.to_dict('records')

        sql = """
        SELECT CONCAT(discounttype, ' ', discountpercentage) as label, discountid as value FROM discount
        WHERE NOT discountdelete
        ORDER BY discounttype ASC"""
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        discount_options = df.to_dict('records')

        sql = """
        SELECT roomtype as label, roomtypeid as value FROM roomtype
        WHERE NOT roomtypedelete
        ORDER BY roomtypeid ASC"""
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        roomtype_options = df.to_dict('records')

        return [statusname_options, guestname_options, groupname_options, discount_options, roomtype_options]
    
    else:
        raise PreventUpdate
    
    
    
@app.callback(
    [
        Output('bookingprofile_roomnumber', 'options')
    ],
    [
        Input('url','pathname'),
        Input('bookingprofile_roomtype', 'value')
    ]
)

def bookingprofile_loaddropdown2 (pathname, roomtype):
    if pathname == '/bookings/bookings_profile': 
        sql2 = """
        SELECT r.roomnumber as label, roomid as value FROM room r
        INNER JOIN roomtype rt ON rt.roomtypeid = r.roomtypeid
        WHERE NOT roomdelete
        AND r.roomtypeid = %s"""
        
        values2 = [f"{roomtype}"]
        cols2 = ['label', 'value']
        df2 = db.querydatafromdatabase(sql2, values2, cols2)
        roomnumber_options = df2.to_dict('records') 

        return [roomnumber_options]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('bookingprofile_deletediv', 'style'),
        Output('bookingprofile_toload', 'data')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url','search')
    ]
)

def bookingprofile_deletediv(pathname, search):
    if pathname =='/bookings/bookings_profile':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        deletediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [deletediv_style, to_load]

@app.callback(
        [
            Output('bookingprofile_alert', 'color'),
            Output('bookingprofile_alert', 'children'),
            Output('bookingprofile_alert','is_open'),

            Output('bookingprofile_successmodal','is_open'),
            Output('bookingprofile_feedbackmessage', 'children'),
            Output('bookingprofile_btnmodal', 'href')
        ],
        [
            Input('bookingprofile_save', 'n_clicks'),
            Input('bookingprofile_btnmodal', 'n_clicks')
        ],
        [
            State('bookingprofile_statusname', 'value'),
            State('bookingprofile_guestname','value'),
            State('bookingprofile_groupname', 'value'),
            State('bookingprofile_occupants', 'value'),
            State('bookingprofile_discount', 'value'),
            State('bookingprofile_ratetype', 'value'),
            State('bookingprofile_roomtype', 'value'),
            State('bookingprofile_roomnumber','value'),
            State('bookingprofile_datepicker', 'start_date'),
            State('bookingprofile_datepicker', 'end_date'),
            State('bookingprofile_arrivalhours', 'value'),
            State('bookingprofile_arrivalmins', 'value'),
            State('bookingprofile_arrivalsecs', 'value'),
            State('bookingprofile_departurehours', 'value'),
            State('bookingprofile_departuremins', 'value'),
            State('bookingprofile_departuresecs', 'value'),
            State('url', 'search'),
            State('bookingprofile_delete', 'value')
        ]
)

def bookingprofile_saveprofile (submitbtn, closebtn, statusname, guestname, groupname, occupants, discount, ratetype, roomtype, roomnumber, checkindate, checkoutdate, arrivalhours, arrivalmins, arrivalsecs, departurehours, departuremins, departuresecs, search, delete):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'bookingprofile_save' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            feedbackmessage = ''
            okay_href = ''

            if not statusname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply booking status.'
            elif not guestname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply guest name.'
            elif not occupants:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply number of occupants.'
            elif not ratetype:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply rate type.'
            elif not roomtype:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply room type.'
            elif not roomnumber:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply room number.'
            elif not checkindate:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply check-in date.'
            elif not checkoutdate:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply check-out date.'
            elif occupants < 0:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply valid number of occupants.'
            else:
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]

                sqlstaff = """
                    select staffid from staff
	                where staffactive
                    """
                valuesstaff = []
                colstaff = ['staffid']
                df0 = db.querydatafromdatabase(sqlstaff, valuesstaff, colstaff)

                staffid = int(df0['staffid'][0]) if pd.notna(df0['staffid'][0]) else 0

                
                if create_mode == 'add':
                    
                    sql0="""INSERT INTO booking(
                        roomid,
                        discountid,
                        guestid,
                        staffid,
                        groupguestid,
                        ratetypeid,
                        numberofoccupants,
                        checkindate,
                        checkoutdate,
                        bookingdelete
                    )
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = [roomnumber, discount, guestname, staffid, groupname, ratetype, occupants, checkindate, checkoutdate, False]
                    db.modifydatabase(sql0, values)
                    
                    if not arrivalhours:
                        None
                    else:
                        datetime_str = f"{checkindate} {arrivalhours}:{arrivalmins}:{arrivalsecs}"
                        arrivaltime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

                        sql1 = """
                        UPDATE booking
                        SET
                            arrivaltime = %s
                        WHERE bookingid = (SELECT MAX(bookingid) FROM booking);
                        """
                        values = [arrivaltime]
                        db.modifydatabase(sql1, values)

                    if not departurehours:
                        None
                    else:
                        datetime_str2 = f"{checkoutdate} {departurehours}:{departuremins}:{departuresecs}"
                        departuretime = datetime.strptime(datetime_str2, "%Y-%m-%d %H:%M:%S")

                        sql1 = """
                        UPDATE booking
                        SET
                            departuretime = %s
                        WHERE bookingid = (SELECT MAX(bookingid) FROM booking);
                        """
                        values = [departuretime]
                        db.modifydatabase(sql1, values)

                    sql2 = """
                    Select daysduration, monthsduration, hourextension, bookingid from booking
                    Order by bookingid desc limit 1;
                    """
                    values2 = []
                    col2 = ['daysduration', 'monthsduration', 'hourextension', 'bookingid']
                    df2 = db.querydatafromdatabase(sql2, values2, col2)
                    
                    daysduration = int(df2['daysduration'][0]) if pd.notna(df2['daysduration'][0]) else 0
                    monthsduration = int(df2['monthsduration'][0]) if pd.notna(df2['monthsduration'][0]) else 0
                    hourextension = int(df2['hourextension'][0]) if pd.notna(df2['hourextension'][0]) else 0

                    feedbackmessage = f"Total length of stay is {monthsduration} months, {daysduration} days, and {hourextension} hours."
                    okay_href = '/bookings/bookings_home'
                    modal_open = True

                    bookingid = int(df2['bookingid'][0]) if pd.notna(df2['bookingid'][0]) else 0

                    sql3 = """
                    INSERT INTO statuschange(
                        bookingid,
                        statusnameid,
                        statuschangedelete
                    )
                    VALUES(%s,%s,%s)"""
                    values3 = [bookingid, statusname, False]
                    db.modifydatabase(sql3, values3)

                
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    bookingid = parse_qs(parsed.query)['id'][0]

                    sql0 = """UPDATE booking
                    SET
                        roomid = %s,
                        discountid = %s,
                        guestid = %s,
                        staffid = %s,
                        groupguestid = %s,
                        ratetypeid = %s,
                        numberofoccupants = %s,
                        checkindate = %s,
                        checkoutdate = %s,
                        bookingdelete = %s
                    WHERE
                        bookingid= %s
                    """
                    to_delete = bool(delete)
                    values = [roomnumber, discount, guestname, staffid, groupname, ratetype, occupants, checkindate, checkoutdate, to_delete, bookingid]
                    db.modifydatabase(sql0, values)                   
                    
                    if not arrivalhours:
                        None
                    else:
                        datetime_str = f"{checkindate} {arrivalhours}:{arrivalmins}:{arrivalsecs}"
                        arrivaltime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

                        sql1 = """
                        UPDATE booking
                        SET
                            arrivaltime = %s
                        WHERE bookingid = %s;
                        """
                        values = [arrivaltime, bookingid]
                        db.modifydatabase(sql1, values)

                    if not departurehours:
                        None
                    else:
                        datetime_str2 = f"{checkoutdate} {departurehours}:{departuremins}:{departuresecs}"
                        departuretime = datetime.strptime(datetime_str2, "%Y-%m-%d %H:%M:%S")

                        sql1 = """
                        UPDATE booking
                        SET
                            departuretime = %s
                        WHERE bookingid = %s;
                        """
                        values = [departuretime, bookingid]
                        db.modifydatabase(sql1, values)
                    
                    sql2 = """
                    Select daysduration, monthsduration, hourextension from booking
                    where bookingid = %s;
                    """
                    values2 = [bookingid]
                    col2 = ['daysduration', 'monthsduration', 'hourextension']
                    df2 = db.querydatafromdatabase(sql2, values2, col2)

                    daysduration = int(df2['daysduration'][0]) if pd.notna(df2['daysduration'][0]) else 0
                    monthsduration = int(df2['monthsduration'][0]) if pd.notna(df2['monthsduration'][0]) else 0
                    hourextension = int(df2['hourextension'][0]) if pd.notna(df2['hourextension'][0]) else 0

                    feedbackmessage = f"Total length of stay is {monthsduration} months, {daysduration} days, and {hourextension} hours."
                    okay_href = '/bookings/bookings_home'
                    modal_open = True

                    sql3 = """
                    INSERT INTO statuschange(
                        bookingid,
                        statusnameid,
                        statuschangedelete
                    )
                    VALUES(%s,%s,%s)"""
                    values3 = [bookingid, statusname, False]
                    db.modifydatabase(sql3, values3)

                else:
                    PreventUpdate
            
            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

@app.callback(
    [
        Output('bookingprofile_statusname', 'value'),
        Output('bookingprofile_guestname','value'),
        Output('bookingprofile_groupname', 'value'),
        Output('bookingprofile_occupants', 'value'),
        Output('bookingprofile_discount', 'value'),
        Output('bookingprofile_ratetype', 'value'),
        Output('bookingprofile_roomtype', 'value'),
        Output('bookingprofile_roomnumber','value'),
        Output('bookingprofile_datepicker','start_date'),
        Output('bookingprofile_datepicker','end_date'),
        Output('bookingprofile_arrivalhours','value'),
        Output('bookingprofile_arrivalmins','value'),
        Output('bookingprofile_arrivalsecs','value'),
        Output('bookingprofile_departurehours','value'),
        Output('bookingprofile_departuremins','value'),
        Output('bookingprofile_departuresecs','value'),
    ],
    [
        Input('bookingprofile_toload','modified_timestamp')
    ],
    [
        State('bookingprofile_toload', 'data'),
        State('url', 'search') 
    ]
)

def bookingprofile_loadprofile (timestamp, toload, search):
    if toload == 1:
        parsed = urlparse(search)
        bookingid = parse_qs(parsed.query)['id'][0]
        sql ="""
            Select statusnameid, guestid, groupguestid, numberofoccupants, discountid, ratetypeid, roomtypeid, b.roomid, checkindate, checkoutdate, arrivaltime, departuretime FROM booking b
                LEFT JOIN
                    (
                    SELECT sc.*,
                    ROW_NUMBER() OVER (PARTITION BY sc.bookingid ORDER BY sc.statusmodifieddate DESC) AS rn
                    FROM statuschange sc
                    ) AS sc ON b.bookingid = sc.bookingid AND sc.rn = 1
                Inner Join room r ON r.roomid = b.roomid
	            Where b.bookingid = %s """
        values = [bookingid]
        col = ['statusnameid', 'guestid', 'groupguestid','occupants', 'discountid', 'ratetypeid', 'roomtypeid', 'roomid', 'checkindate', 'checkoutdate', 'arrivaltime', 'departuretime']
        df = db.querydatafromdatabase(sql, values, col)
        statusnameid = int(df['statusnameid'][0]) if pd.notna(df['statusnameid'][0]) else None
        guestid = int(df['guestid'][0]) if pd.notna(df['guestid'][0]) else None
        groupguestid = int(df['groupguestid'][0]) if pd.notna(df['groupguestid'][0]) else None
        occupants = int(df['occupants'][0]) if pd.notna(df['occupants'][0]) else None
        discountid = int(df['discountid'][0]) if pd.notna(df['discountid'][0]) else None
        ratetypeid = int(df['ratetypeid'][0]) if pd.notna(df['ratetypeid'][0]) else None
        roomtypeid = int(df['roomtypeid'][0]) if pd.notna(df['roomtypeid'][0]) else None
        roomid = int(df['roomid'][0]) if pd.notna(df['roomid'][0]) else None
        checkindate = (df['checkindate'][0]) if pd.notna(df['checkindate'][0]) else None
        checkoutdate = (df['checkoutdate'][0]) if pd.notna(df['checkoutdate'][0]) else None
        arrivalhours, arrivalmins, arrivalsecs = None, None, None
        departurehours, departuremins, departuresecs = None, None, None
        
        if pd.notna(df['arrivaltime'][0]):
            arrivaltime = (df['arrivaltime'][0])
            formatted_string = arrivaltime.strftime('%Y-%m-%d %H:%M:%S')
            timestamp_dt = datetime.strptime(formatted_string, '%Y-%m-%d %H:%M:%S')
            arrivalhours = timestamp_dt.hour
            arrivalmins = timestamp_dt.minute
            arrivalsecs = timestamp_dt.second
        else:
            None
        
        if pd.notna(df['departuretime'][0]):
            departuretime = (df['departuretime'][0])
            formatted_string = departuretime.strftime('%Y-%m-%d %H:%M:%S')
            timestamp_dt = datetime.strptime(formatted_string, '%Y-%m-%d %H:%M:%S')
            departurehours = timestamp_dt.hour
            departuremins = timestamp_dt.minute
            departuresecs = timestamp_dt.second
        else:
            None

        return [statusnameid, guestid, groupguestid, occupants, discountid, ratetypeid, roomtypeid, roomid, checkindate, checkoutdate, arrivalhours, arrivalmins, arrivalsecs, departurehours, departuremins, departuresecs]
    else:
        raise PreventUpdate
