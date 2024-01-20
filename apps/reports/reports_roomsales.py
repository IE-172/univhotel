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
import plotly.graph_objs as go 

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.Div([
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.H2('Room Sales Report', style={'color': '#8A1538'}), width = 'auto'),
                                dbc.Col(html.H6('Generate reports on room sales.'), width = 'auto')
                            ]
                        )
                    ], 
                    style = {'float':'left'})
        ]),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Card(
            [
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.H4("Room and Rate Type Sales Chart"),
                            html.P("Generate charts on room sales.Includes booking status: Booked, Confirmed, Closed, Cancelled"),
                            html.Div(dbc.Form(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Label("Duration", width = 1),
                                                dbc.Col(dcc.DatePickerRange(id = 'roomsalesreport_durationfilter', start_date_placeholder_text = 'Start Date', end_date_placeholder_text = 'End Date', display_format = "YYYY-MM-DD"), width = 3)
                                            ],
                                            className = 'mb-3'
                                        )
                                    ]
                                )
                            )
                        ]
                    ),
                    html.Div(
                        [
                            dcc.Loading(id = 'roomsalesreport_bodyload2', children = [dcc.Graph(id = 'roomsalesreport_bodyreceipts2')], type = "circle")
                        ],
                        style = {'width': '100%', "border": '3px #5c5c5c solid'}
                    ),
                    #second graph
                    html.Br(),
                    html.Br(),
                    html.Div(
                        [
                            dcc.Loading(id = 'roomsalesreport_bodyload3', children = [dcc.Graph(id = 'roomsalesreport_bodyreceipts3')], type = "circle")
                        ],
                        style = {'width': '100%', "border": '3px #5c5c5c solid'}
                    ),
                    html.Br(),
                    html.Br(),
                    html.Div(
                        [
                            dcc.Loading(id = 'roomsalesreport_bodyload', children = [dcc.Graph(id = 'roomsalesreport_bodyreceipts')], type = "circle")
                        ],
                        style = {'width': '100%', "border": '3px #5c5c5c solid'}
                    ),
                    html.Br(),
                    html.Hr(),
                    html.Div(
                        [
                            html.H4("Room Sales List"),
                            html.P("Generate lists on room sales. Includes booking status: Booked, Confirmed, Closed"),
                        ]
                    ),
                    html.Div("Table with report", id = 'roomsalesreport_reporttable'),
                ],
            )
        ]
        )
    ]
)

@app.callback(
    [
        Output('roomsalesreport_bodyreceipts2', 'figure')
    ],
    [
        Input('url', 'pathname'),
        Input('roomsalesreport_durationfilter','start_date'),
        Input('roomsalesreport_durationfilter','end_date'),
    ],
)

def report_loadroomtypesalesgraph (pathname, startdate, enddate):
    if pathname == '/reports/roomsales':
        sql = """
            Select checkoutdate, roomtype, sum(totalamount) as sales from payment p
            inner join booking b on b.bookingid=p.bookingid
            inner join room r on r.roomid=b.roomid
            inner join roomtype rmt on rmt.roomtypeid = r.roomtypeid
            where paymentdelete = false and bookingdelete = false
            AND checkoutdate >= %s AND checkoutdate <= %s
            group by checkoutdate,roomtype
            order by checkoutdate, roomtype
            """
        values = [startdate, enddate]

        cols = ['Check Out Date','Room Type','Sales']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df[['Check Out Date','Room Type','Sales']]

        listofroomtype = df["Room Type"].unique().tolist()
        traces = {}

        colors = ['#3E9651', '#922428' , '#396AB1','#535154', '#DA7C30', '#FCE205']
        i = 0

        for roomtype in listofroomtype:
            traces['tracebar_' + roomtype] = go.Bar(
                y = df[df["Room Type"] == roomtype]["Sales"], 
                x = df[df["Room Type"] == roomtype]["Check Out Date"],
                marker=dict(color=colors[i]),
                name = roomtype)
            i+=1

        data = list(traces.values())

        layout = go.Layout(
            yaxis1 = {'categoryorder':'total ascending','title':"Sales in Pesos"},
            xaxis = {'title':"Date", "mirror":False, "zeroline":True},
            height = 500,
            width = 1300,
            margin = {'b': 50, 't': 20, 'l': 50 },
            hovermode = 'closest',
            autosize = False,
            dragmode = 'zoom',
            barmode = 'stack',
            boxmode = "overlay"
        )

        figure3 = {'data': data, 'layout': layout}
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size ='sm')

        if df.shape[0]:
            return [figure3]
        else:
            return ['No figure to display']
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('roomsalesreport_bodyreceipts', 'figure')
    ],
    [
        Input('url', 'pathname'),
        Input('roomsalesreport_durationfilter','start_date'),
        Input('roomsalesreport_durationfilter','end_date'),
    ],
)

def report_loadroomsalesgraph (pathname, startdate, enddate):
    if pathname == '/reports/roomsales':
        sql = """
            Select roomnumber, ratetype, sum(totalamount) as sales from payment p
	            inner join booking b on b.bookingid=p.bookingid
	            inner join room r on r.roomid=b.roomid
	            inner join ratetype rt on rt.ratetypeid=b.ratetypeid
	            where paymentdelete = false and bookingdelete = false
                AND checkoutdate >= %s AND checkindate <= %s
	            group by roomnumber, ratetype
	            order by roomnumber, ratetype
            """
        values = [startdate, enddate]

        cols = ['Room No.','Rate Type','Sales']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df[['Room No.','Rate Type','Sales']]

        listofratetype = df["Rate Type"].unique().tolist()
        traces = {}

        colors = ['#3E9651', '#922428' , '#396AB1','#535154', '#DA7C30', '#FCE205']
        i = 0

        for ratetype in listofratetype:
            traces['tracebar_' + ratetype] = go.Bar(
                y = df[df["Rate Type"] == ratetype]["Sales"], 
                x = df[df["Rate Type"] == ratetype]["Room No."],
                marker=dict(color=colors[i]),
                name = ratetype)
            i+=1

        data = list(traces.values())

        layout = go.Layout(
            yaxis1 = {'categoryorder':'total ascending','title':"Sales in Pesos"},
            xaxis = {'title':"Rooms", "mirror":False, "zeroline":True},
            height = 500,
            width = 1300,
            margin = {'b': 50, 't': 20, 'l': 50 },
            hovermode = 'closest',
            autosize = False,
            dragmode = 'zoom',
            barmode = 'stack',
            boxmode = "overlay"
        )

        figure3 = {'data': data, 'layout': layout}
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size ='sm')

        if df.shape[0]:
            return [figure3]
        else:
            return ['No figure to display']
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('roomsalesreport_reporttable','children')
    ],
    [
        Input('url','pathname'),
        Input('roomsalesreport_durationfilter', 'start_date'),
        Input('roomsalesreport_durationfilter', 'end_date')
    ]
)

def loadroomsales (pathname, startdate, enddate):
    if pathname == '/reports/roomsales':    
        sql = """
            select 
	            roomnumber,
	            groupguestname,
                numberofoccupants, 
                monthsduration, 
                daysduration,
                case
                    when b.ratetypeid = 1 then residentrate
                    when b.ratetypeid = 2 then transientrate
                end as roomrate,
                discountamount,
                earnedroomfee,
                p.bookingid
                from payment p
                inner join booking b on b.bookingid = p.bookingid
                inner join room r on r.roomid = b.roomid
                inner join ratetype rt on rt.ratetypeid = b.ratetypeid
                inner join roomtype rmt on rmt.roomtypeid = r.roomtypeid
                left join groupguest gg on gg.groupguestid = b.groupguestid
                where bookingdelete = false and paymentdelete = false
            """
        values = []
        cols = ['Room No.','Group','PAX','Months','Days','Room Rate','Discount','Room Fee','bookingid']

        if startdate and enddate:
            sql += "AND checkoutdate >= %s AND checkindate <= %s"
            values += [startdate, enddate]
        
        sql += "ORDER BY roomnumber ASC"
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for booking_id in df['bookingid']:
                buttons += [
                    html.Div(dbc.Button('View Booking', href = f'/bookings/bookings_profile?mode=edit&id={booking_id}', size = 'sm', color = 'warning'), style = {'text-align':'center'})
                ]
            df['Action'] = buttons
            df = df[['Room No.','Group','PAX','Months','Days','Room Rate','Discount','Room Fee', 'Action']]
            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center', 'font-size': '12px'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('roomsalesreport_bodyreceipts3', 'figure')
    ],
    [
        Input('url', 'pathname'),
        Input('roomsalesreport_durationfilter','start_date'),
        Input('roomsalesreport_durationfilter','end_date'),
    ],
)

def report_loadroomtypesaleslinegraph (pathname, startdate, enddate):
    if pathname == '/reports/roomsales':
        sql = """
            Select checkoutdate, roomtype, sum(totalamount) as sales from payment p
            inner join booking b on b.bookingid=p.bookingid
            inner join room r on r.roomid=b.roomid
            inner join roomtype rmt on rmt.roomtypeid = r.roomtypeid
            where paymentdelete = false and bookingdelete = false
            AND checkoutdate >= %s AND checkoutdate <= %s
            group by checkoutdate,roomtype
            order by checkoutdate, roomtype
            """
        values = [startdate, enddate]

        cols = ['Check Out Date','Room Type','Sales']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df[['Check Out Date','Room Type','Sales']]

        listofroomtype = df["Room Type"].unique().tolist()
        traces = {}
        colors = ['#3E9651', '#922428' , '#396AB1','#535154', '#DA7C30', '#FCE205']
        i = 0

        for roomtype in listofroomtype:
            traces['tracebar_' + roomtype] = go.Scatter(
                y = df[df["Room Type"] == roomtype]["Sales"], 
                x = df[df["Room Type"] == roomtype]["Check Out Date"],
                name = roomtype,
                marker=dict(color=colors[i]),
                mode = 'lines+markers')
            i+=1

        data = list(traces.values())

        layout = go.Layout(
            yaxis1 = {'categoryorder':'total ascending',
                      'title':"Sales in Pesos"},
            xaxis = {'title':"Date", 
                     "mirror":False, 
                     "zeroline":True},
            height = 500,
            width = 1300,
            margin = {'b': 50, 't': 20, 'l': 50 },
            hovermode = 'closest',
            autosize = False,
            dragmode = 'zoom',
        )

        figure3 = {'data': data, 'layout': layout}
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size ='sm')

        if df.shape[0]:
            return [figure3]
        else:
            return ['No figure to display']
    else:
        raise PreventUpdate
