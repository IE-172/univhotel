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

from urllib.parse import urlparse, parse_qs
from decimal import Decimal as d
from decimal import Context, getcontext

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.Div([
            dcc.Store(id = 'paymentsprofile_toload', storage_type = 'memory', data = 0)
        ]),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div([html.H2('Payment Details', style={'color': '#8A1538','margin-left':'25px'})], style={'float': 'left'}),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                    ],
                    width=6  
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.H4("Booking Summary"),
                                                html.P("Breakdown of booking details."),
                                                dbc.Form(
                                                    dbc.Row(
                                                        [
                                                            dbc.Label("Booking", width = 4),
                                                            dbc.Col(dcc.Dropdown(id = 'paymentsprofile_booking', placeholder = "Select Booking"), width = 8),
                                                        ],
                                                        className = 'mb-2'
                                                    )
                                                ),
                                                dbc.Row(
                                                        [
                                                            dbc.Label("Booking Status", width = 4),
                                                            dbc.Col([],id='paymentsprofile_statusname'),
                                                        ],
                                                        className = 'mb-3'
                                                ),
                                                html.Hr(),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Guest Name", width = 4),
                                                        dbc.Col([],id='paymentsprofile_guestname'),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Group Name", width = 4),
                                                        dbc.Col([],id='paymentsprofile_groupname'),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("PAX", width = 4),
                                                        dbc.Col([],id='paymentsprofile_occupants'),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Discount Type", width = 4),
                                                        dbc.Col([],id='paymentsprofile_discount'),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                html.Hr(),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Rate Type", width = 4),
                                                        dbc.Col([],id='paymentsprofile_ratetype'),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Room Type", width = 4),
                                                        dbc.Col([],id='paymentsprofile_roomtype'),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Room No.", width = 4),
                                                        dbc.Col([],id='paymentsprofile_roomnumber'),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Duration", width = 4),
                                                        dbc.Col([],id='paymentsprofile_duration'),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                dbc.Label("Months:", style={'margin-left':'15px'}),
                                                                dbc.Col([],id='paymentsprofile_months',style={'margin-left':'25px'}),
                                                            ],
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                dbc.Label("Days:"),
                                                                dbc.Col([],id='paymentsprofile_days',style={'margin-left':'25px'}),
                                                            ],
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                dbc.Label("Hours:"),
                                                                dbc.Col([],id='paymentsprofile_hours',style={'margin-left':'25px'}),
                                                            ],
                                                        ),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                            ]
                                        )
                                    ],
                                )
                            ],
                            style={'background-color':'#ffffff','margin-left':'10px'}
                        )
                    ],
                    width=6  
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.H4("Payment Information"),
                                                html.P("Breakdown of payment details."),
                                                dbc.Alert(id = 'paymentsprofile_alert', is_open = False),
                                                dbc.Form(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Label("Payment Type", width = 4),
                                                                dbc.Col(dcc.Dropdown(id = 'paymentsprofile_paymenttype', placeholder = "Select Payment"), width = 8),
                                                            ],
                                                            className = 'mb-3'
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                dbc.Label("Mode of Payment", width = 4),
                                                                dbc.Col(dcc.Dropdown(id = 'paymentsprofile_paymentmode', placeholder = "Select Mode of Payment"), width = 8),
                                                            ],
                                                            className = 'mb-3'
                                                        ),
                                                    ]
                                                ),
                                                html.Hr(),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Room Rate", width = 4),
                                                        dbc.Col([],id='paymentsprofile_roomrate'),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Room Fee", width = 4),
                                                        dbc.Col([],id='paymentsprofile_roomfee'),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Discount Amount", width = 4),
                                                        dbc.Col([],id='paymentsprofile_discountamount'),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Extension Charges", width = 4),
                                                        dbc.Col([],id='paymentsprofile_extension'),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Adjusted Charges", width = 4),
                                                        dbc.Col([dbc.InputGroup([dbc.InputGroupText("₱"), dbc.Input(id = 'paymentsprofile_additional', placeholder="0.00", type="number")])]),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                html.Hr(),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Total Amount", width = 4),
                                                        dbc.Col([],id='paymentsprofile_total'),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Deposit Amount", width = 4),
                                                        dbc.Col([dbc.InputGroup([dbc.InputGroupText("₱"), dbc.Input(id = 'paymentsprofile_deposit', placeholder="0.00", type="number")])]),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                html.Hr(),
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Balance", width = 4),
                                                        dbc.Col([],id='paymentsprofile_balance'),
                                                    ],
                                                    className = 'mb-1'
                                                ),
                                                html.Hr(),
                                                html.Div(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Label("Delete payment transaction?", width = 7),
                                                                dbc.Col(dbc.Checklist(id = 'paymentsprofile_delete', inline = True, switch =True, value = 0, options = [{"label":"Mark as deleted","value":1}]))
                                                            ],
                                                            className = 'mb-3'
                                                        )
                                                    ],
                                                    id = 'paymentsprofile_deletediv'
                                                ),
                                                html.Div(dbc.Button('Save Payment', id = 'paymentsprofile_save', n_clicks=0, style={'backgroundColor': '#00573F', 'color': 'white'}), className="d-grid gap-2 col-6 mx-auto"),
                                                dbc.Modal(
                                                    [
                                                        dbc.ModalHeader(html.H4("Payment Saved")),
                                                        dbc.ModalBody(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        #update once modal is working
                                                                    ],
                                                                    id = 'paymentsprofile_feedbackmessage',
                                                                    style={'margin-left': '1px'}
                                                                )
                                                            ]
                                                        ),
                                                        dbc.ModalFooter(
                                                            [
                                                                dbc.Button("Proceed", href = '/payments/payments_home', id = 'paymentsprofile_btnmodal')
                                                            ]
                                                        )
                                                    ],
                                                    centered = True,
                                                    id = 'paymentsprofile_successmodal',
                                                    backdrop = 'static'
                                                )
                                            ]
                                        )
                                    ],
                                )
                            ],
                            style={'background-color':'#ffffff','margin-right':'10px'}
                        )
                    ],
                    width=6  
                ),
            ]
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
        Output('paymentsprofile_booking','options'),
        Output('paymentsprofile_paymenttype', 'options'),
        Output('paymentsprofile_paymentmode','options')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)

def paymentsprofile_loaddropdown1 (pathname, search):
    if pathname == '/payments/payments_profile':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]

        if create_mode == 'add':
            sql1 = """
            SELECT concat (roomnumber,' ',surname,' ',checkindate,' - ',checkoutdate) as label, b.bookingid as value 
            FROM booking b
            inner join room r on r.roomid = b.roomid
            inner join guest g on g.guestid = b.guestid
            LEFT JOIN
                (
                SELECT sc.*,
                ROW_NUMBER() OVER (PARTITION BY sc.bookingid ORDER BY sc.statusmodifieddate DESC) AS rn
                FROM statuschange sc
                ) AS sc ON b.bookingid = sc.bookingid AND sc.rn = 1
            INNER JOIN statusname sn ON sc.statusnameid = sn.statusnameid
            WHERE b.bookingid NOT IN (
                Select 
                p.bookingid
                from payment p 
                inner join booking b on b.bookingid = p.bookingid
                inner join guest g on g.guestid = b.guestid
                inner join paymenttype pt on pt.paymenttypeid = p.paymenttypeid
                inner join room r on r.roomid = b.roomid
                where not bookingdelete and not paymentdelete
            )			
            and roomdelete = false 
            and bookingdelete = false
            and not sc.statusnameid = 6
            """
            values1 = []
            cols1 = ['label', 'value']
            df1 = db.querydatafromdatabase(sql1, values1, cols1)
            booking_options = df1.to_dict('records')

        elif create_mode == 'edit':
            
            parsed = urlparse(search)
            paymentid = parse_qs(parsed.query)['id'][0]

            print(create_mode)
            print(paymentid)

            sql1 = """
            SELECT concat (roomnumber,' ',surname,' ',checkindate,' - ',checkoutdate) as label, p.bookingid as value 
            FROM payment p
            inner join booking b on b.bookingid=p.bookingid
            inner join room r on r.roomid = b.roomid
            inner join guest g on g.guestid = b.guestid
            where paymentid = %s
            """
            values1 = [paymentid]
            cols1 = ['label', 'value']
            df1 = db.querydatafromdatabase(sql1, values1, cols1)
            booking_options = df1.to_dict('records')

        sql2 = """
        Select paymenttype as label, paymenttypeid as value from paymenttype
        where not paymenttypedelete
        """
        values2 = []
        cols2 = ['label', 'value']
        df2 = db.querydatafromdatabase(sql2, values2, cols2)
        paymenttype_options = df2.to_dict('records')
    
        sql3 = """
        Select modeofpayment as label, modeofpaymentid as value from modeofpayment
        where not modeofpaymentdelete
        """
        values3 = []
        cols3 = ['label', 'value']
        df3 = db.querydatafromdatabase(sql3, values3, cols3)
        paymentmode_options = df3.to_dict('records')

        return [booking_options, paymenttype_options, paymentmode_options]
    
    else:
        raise PreventUpdate

    
@app.callback(
    [
        Output('paymentsprofile_statusname', 'children'),
        Output('paymentsprofile_guestname','children'),
        Output('paymentsprofile_groupname', 'children'),
        Output('paymentsprofile_occupants', 'children'),
        Output('paymentsprofile_discount', 'children'),
        Output('paymentsprofile_ratetype', 'children'),
        Output('paymentsprofile_roomtype', 'children'),
        Output('paymentsprofile_roomnumber','children'),
        Output('paymentsprofile_duration','children'),
        Output('paymentsprofile_months','children'),
        Output('paymentsprofile_days','children'),
        Output('paymentsprofile_hours','children'),
    ],
    [
        Input('url','pathname'),
        Input('paymentsprofile_booking', 'value')
    ]
)

def paymentsprofile_loadsummary (pathname, bookingid):
    if pathname == '/payments/payments_profile': 
        
        sql ="""
            select 
                statusname, 
                concat(surname,', ',firstname,' ',middlename) as guestname, 
                groupguestname, 
                numberofoccupants, 
                discounttype, 
                ratetype, 
                roomtype,
                roomnumber,
                concat(checkindate,' - ',checkoutdate) as duration,
                monthsduration,
                daysduration,
                hourextension
            from booking b
                inner join room r on r.roomid = b.roomid
                inner join roomtype rt on rt.roomtypeid = r.roomtypeid
                inner join guest g on g.guestid = b.guestid
                left join groupguest gg on gg.groupguestid = b.groupguestid
                left join discount d on d.discountid = b.discountid
                inner join ratetype rtt on rtt.ratetypeid = b.ratetypeid
                LEFT JOIN
                    (
                    SELECT sc.*,
                    ROW_NUMBER() OVER (PARTITION BY sc.bookingid ORDER BY sc.statusmodifieddate DESC) AS rn
                    FROM statuschange sc
                    ) AS sc ON b.bookingid = sc.bookingid AND sc.rn = 1
                INNER JOIN statusname sn ON sc.statusnameid = sn.statusnameid
            where b.bookingid = %s
            """
        values = [bookingid]
        col = ['statusname', 'guestname', 'groupguestname','numberofoccupants', 'discounttype', 'ratetype', 'roomtype', 'roomnumber', 'duration', 'monthsduration', 'daysduration', 'hourextension']
        df = db.querydatafromdatabase(sql, values, col)
            
        statusname = (df['statusname'][0]) if pd.notna(df['statusname'][0]) else None
        guestname = (df['guestname'][0]) if pd.notna(df['guestname'][0]) else None
        groupname = (df['groupguestname'][0]) if pd.notna(df['groupguestname'][0]) else None
        occupants = (df['numberofoccupants'][0]) if pd.notna(df['numberofoccupants'][0]) else None
        discount = (df['discounttype'][0]) if pd.notna(df['discounttype'][0]) else None
        ratetype = (df['ratetype'][0]) if pd.notna(df['ratetype'][0]) else None
        roomtype = (df['roomtype'][0]) if pd.notna(df['roomtype'][0]) else None
        roomnumber = (df['roomnumber'][0]) if pd.notna(df['roomnumber'][0]) else None
        duration = (df['duration'][0]) if pd.notna(df['duration'][0]) else None
        months = (df['monthsduration'][0]) if pd.notna(df['monthsduration'][0]) else 0
        days = (df['daysduration'][0]) if pd.notna(df['daysduration'][0]) else 0
        hours = (df['hourextension'][0]) if pd.notna(df['hourextension'][0]) else 0


        return [statusname, guestname, groupname, occupants, discount, ratetype, roomtype, roomnumber, duration, months, days, hours]
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('paymentsprofile_deletediv', 'style'),
        Output('paymentsprofile_toload', 'data')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url','search')
    ]
)

def paymentsprofile_deletediv(pathname, search):
    if pathname =='/payments/payments_profile':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        deletediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [deletediv_style, to_load]

@app.callback(
    [
        Output('paymentsprofile_roomrate','children'),
        Output('paymentsprofile_roomfee','children'),
        Output('paymentsprofile_discountamount','children'),
        Output('paymentsprofile_extension','children'),
        Output('paymentsprofile_total','children'),
        Output('paymentsprofile_balance', 'children'),
        Output('paymentsprofile_roomrate','value'),
        Output('paymentsprofile_roomfee','value'),
        Output('paymentsprofile_discountamount','value'),
        Output('paymentsprofile_extension','value'),
        Output('paymentsprofile_total','value'),
        Output('paymentsprofile_total','deposit'),
        Output('paymentsprofile_balance', 'value'),
    ],
    [
        Input('url','pathname'),
        Input('paymentsprofile_booking', 'value'),
        Input('paymentsprofile_additional', 'value'),
        Input('paymentsprofile_deposit', 'value')
    ]
)

def loadpaymentdetails(pathname, bookingid, additional, deposit):
    if pathname =='/payments/payments_profile':
        
        sql = """
        select 
            bookingid,
            case
                when b.ratetypeid = 1 then residentrate
                when b.ratetypeid = 2 then transientrate
            end as roomrate,
            case
                when b.ratetypeid = 1 then monthsduration
                when b.ratetypeid = 2 then daysduration
            end as roomfeemultiplier,
            discountpercentage as discountmultiplier,
            hourextension,
            roomextensionrate
        from booking b
            inner join ratetype rt on rt.ratetypeid = b.ratetypeid
            inner join room r on r.roomid = b.roomid
            inner join roomtype rmt on rmt.roomtypeid = r.roomtypeid
            left join discount d on d.discountid = b.discountid
        where bookingid = %s
        """
        values = [bookingid]
        cols = ['bookingid', 'roomrate', 'roomfeex','discountx','hourextension','extensionrate']
        df = db.querydatafromdatabase(sql, values, cols)

        roomrate = (df['roomrate'][0]) if pd.notna(df['roomrate'][0]) else 0
        roomfeex = (df['roomfeex'][0]) if pd.notna(df['roomfeex'][0]) else 0
        discountx = (df['discountx'][0]) if pd.notna(df['discountx'][0]) else 0
        hourextension = (df['hourextension'][0]) if pd.notna(df['hourextension'][0]) else 0
        extensionrate = (df['extensionrate'][0]) if pd.notna(df['extensionrate'][0]) else 0

        roomfee = (d(str(roomrate)) * d(str(roomfeex)))
        discountamount = (d(str(roomfee)) * (d(str(discountx)) / 100))
        extension = (d(str(hourextension)) * d(str((extensionrate))))

        if additional:
            total = (d(str(roomfee)) - d(str(discountamount)) + d(str(extension)) + d(str(additional)))
        else:
            total = (d(str(roomfee)) - d(str(discountamount)) + d(str(extension)))

        if deposit:
            balance = d(str(total)) - d(str(deposit))
        else:
            balance = d(str(total))

        return [roomrate,roomfee, discountamount, extension, total, balance, roomrate,roomfee, discountamount, extension, total, deposit, balance]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('paymentsprofile_alert', 'color'),
        Output('paymentsprofile_alert', 'children'),
        Output('paymentsprofile_alert','is_open'),

        Output('paymentsprofile_successmodal','is_open'),
        Output('paymentsprofile_feedbackmessage', 'children'),
        Output('paymentsprofile_btnmodal', 'href')
    ],
    [
        Input('paymentsprofile_save', 'n_clicks'),
        Input('paymentsprofile_btnmodal', 'n_clicks')
    ],
    [
        State('paymentsprofile_booking', 'value'),
        State('paymentsprofile_paymenttype','value'),
        State('paymentsprofile_paymentmode', 'value'),
        State('paymentsprofile_roomfee', 'value'),
        State('paymentsprofile_discountamount', 'value'),
        State('paymentsprofile_extension', 'value'),
        State('paymentsprofile_additional', 'value'),
        State('paymentsprofile_total','value'),
        State('paymentsprofile_deposit', 'value'),
        State('paymentsprofile_balance', 'value'),
        State('url', 'search'),
        State('paymentsprofile_delete', 'value')
    ]
)

def paymentsprofile_save (submitbtn, closebtn, bookingid, paymenttype, paymentmode, roomfee, discountamount, extension, additional, total, deposit, balance, search, delete):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'paymentsprofile_save' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            feedbackmessage = ''
            okay_href = ''

            if not bookingid:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply booking details.'
            elif not paymenttype:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply payment type.'
            elif not paymentmode:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply mode of payment.'
            else:
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]

                sql0 = """
                    select staffid from staff
	                where staffactive
                    """
                values0 = []
                col0 = ['staffid']
                df0 = db.querydatafromdatabase(sql0, values0, col0)

                staffid = int(df0['staffid'][0]) if pd.notna(df0['staffid'][0]) else 0

                sql1 = """
                    select guestid from booking
	                where bookingid = %s
                    """
                values1 = [bookingid]
                col1 = ['guestid']
                df1 = db.querydatafromdatabase(sql1, values1, col1)

                guestid = int(df1['guestid'][0]) if pd.notna(df1['guestid'][0]) else 0

                if create_mode == 'add':
                    
                    sql2="""INSERT INTO payment(
                        guestid,
                        staffid,
                        bookingid,
                        paymenttypeid,
                        modeofpaymentid,
                        earnedroomfee,
                        discountamount,
                        extensioncharges,
                        additionalcharges,
                        totalamount,
                        deposit,
                        balance,
                        paymentdelete
                    )
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                    values2 = [guestid, staffid, bookingid, paymenttype, paymentmode, roomfee, discountamount, extension, additional, total, deposit, balance, False]
                    db.modifydatabase(sql2, values2)

                    feedbackmessage = "Payment record has been saved."
                    okay_href = '/payments/payments_home'
                    modal_open = True
                    
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    paymentid = parse_qs(parsed.query)['id'][0]

                    sql3 = """UPDATE payment
                    SET
                        guestid = %s,
                        staffid = %s,
                        bookingid = %s,
                        paymenttypeid = %s,
                        modeofpaymentid = %s,
                        earnedroomfee = %s,
                        discountamount = %s,
                        extensioncharges = %s,
                        additionalcharges = %s,
                        totalamount = %s,
                        deposit = %s,
                        balance = %s,
                        paymentdelete = %s
                    WHERE
                        paymentid = %s
                    """
                    to_delete = bool(delete)
                    values3 = [guestid, staffid, bookingid, paymenttype, paymentmode, roomfee, discountamount, extension, additional, total, deposit, balance, to_delete, paymentid]
                    db.modifydatabase(sql3, values3)                   
                    
                    feedbackmessage = "Payment record has been updated"
                    okay_href = '/payments/payments_home'
                    modal_open = True

                else:
                    PreventUpdate
            
            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

@app.callback(
    [
        Output('paymentsprofile_booking', 'value'),
        Output('paymentsprofile_paymenttype','value'),
        Output('paymentsprofile_paymentmode', 'value'),
        Output('paymentsprofile_additional', 'value'),
        Output('paymentsprofile_deposit', 'value'),
    ],
    [
        Input('paymentsprofile_toload','modified_timestamp')
    ],
    [
        State('paymentsprofile_toload', 'data'),
        State('url', 'search')
    ]
)

def payments_loadload (timestamp, toload, search):
    if toload == 1:
        parsed = urlparse(search)
        paymentid = parse_qs(parsed.query)['id'][0]
        sql ="""
            Select
                bookingid,
                paymenttypeid,
                modeofpaymentid,
                additionalcharges,
                deposit
            from payment
            where paymentid = %s
            """
        values = [paymentid]
        col = ['bookingid', 'paymenttype', 'paymentmode', 'additional', 'deposit']
        df = db.querydatafromdatabase(sql, values, col)

        bookingid = int(df['bookingid'][0]) if pd.notna(df['bookingid'][0]) else None
        paymenttype = int(df['paymenttype'][0]) if pd.notna(df['paymenttype'][0]) else None
        paymentmode = int(df['paymentmode'][0]) if pd.notna(df['paymentmode'][0]) else None
        additional = (df['additional'][0]) if pd.notna(df['additional'][0]) else None
        deposit = (df['deposit'][0]) if pd.notna(df['deposit'][0]) else None
        
        return [bookingid, paymenttype, paymentmode, additional, deposit]
    else:
        raise PreventUpdate







