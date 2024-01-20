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
                                dbc.Col(html.H2('Occupancy Report', style={'color': '#8A1538'}), width = 'auto'),
                                dbc.Col(html.H6('Generate reports on occupancy.'), width = 'auto')
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
                            html.H4("Occupancy by Booking Status"),
                            html.P("Generate charts on occupancy by booking status.Includes booking status: Booked, Confirmed, Closed"),
                            html.Div(dbc.Form(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Label("Duration", width = 1),
                                                dbc.Col(dcc.DatePickerRange(id = 'occupancyreport_durationfilter', start_date_placeholder_text = 'Start Date', end_date_placeholder_text = 'End Date', display_format = "YYYY-MM-DD"), width = 3)
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
                            dcc.Loading(id = 'occupancyreport_bodyload', children = [dcc.Graph(id = 'occupancyreport_bodyreceipts')], type = "circle")
                        ],
                        style = {'width': '100%', "border": '3px #5c5c5c solid'}
                    ),
                    html.Br(),
                    html.Hr(),
                    html.Div(
                        [
                            html.H4("Occupancy List"),
                            html.P("Generate lists on occupancy. Includes booking status: Booked, Confirmed, Closed"),
                        ]
                    ),
                    html.Div("Table with report", id = 'occupancyreport_reporttable'),
                ],
            )
        ]
        )
    ]
)


@app.callback(
    [
        Output('occupancyreport_bodyreceipts', 'figure')
    ],
    [
        Input('url', 'pathname'),
        Input('occupancyreport_durationfilter','start_date'),
        Input('occupancyreport_durationfilter','end_date'),
    ],
)

def report_loadoccupancygraph (pathname, startdate, enddate):
    if pathname == '/reports/occupancy':
        sql = """
            SELECT 
                date_series::date AS date,
                statusname,
                COUNT(b.checkindate) AS occupancy_count
            FROM 
                generate_series(%s::date, %s::date, interval '1 day') date_series
            LEFT JOIN 
                booking b ON date_series BETWEEN b.checkindate AND b.checkoutdate
            LEFT JOIN
                (
                SELECT sc.*,
                ROW_NUMBER() OVER (PARTITION BY sc.bookingid ORDER BY sc.statusmodifieddate DESC) AS rn
                FROM statuschange sc
                ) AS sc ON b.bookingid = sc.bookingid AND sc.rn = 1
            INNER JOIN statusname sn ON sc.statusnameid = sn.statusnameid
            WHERE 
                bookingdelete = false
                and not sc.statusnameid = 1
                and not sc.statusnameid = 4
                and not sc.statusnameid = 6
            """
        values = [startdate, enddate]

        sql += """
                GROUP BY 
                    statusname,
	                date_series::date
                ORDER BY 
                    date_series::date,
	                statusname
                """
        cols = ['Date','Status','Occupancy']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df[['Date','Status','Occupancy']]

        listofstatusname = df["Status"].unique().tolist()
        colors = ['#3E9651', '#922428' , '#396AB1','#535154', '#DA7C30', '#FCE205']
        i = 0


        traces = {}
        for statusname in listofstatusname:
            traces['tracebar_' + statusname] = go.Bar(
                y = df[df["Status"] == statusname]["Occupancy"], 
                x = df[df["Status"] == statusname]["Date"],
                marker=dict(color=colors[i]),
                name = statusname)
            i+=1

        data = list(traces.values())

        layout = go.Layout(
            yaxis1 = {'categoryorder':'total ascending','title':"Occupancy", 'range':[0,10]},
            xaxis = {'title':"Dates", "mirror":False, "zeroline":True},
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
        Output('occupancyreport_reporttable','children')
    ],
    [
        Input('url','pathname'),
        Input('occupancyreport_durationfilter', 'start_date'),
        Input('occupancyreport_durationfilter', 'end_date')
    ]
)

def loadoccupancy (pathname, startdate, enddate):
    if pathname == '/reports/occupancy':    
        sql = """
            SELECT 
                roomnumber,
                groupguestname,
                numberofoccupants,
                monthsduration,
                daysduration,
                case
                    when b.ratetypeid = 1 then residentrate
                    when b.ratetypeid = 2 then transientrate
                end as roomrate,
                earnedroomfee,
                discountamount,
                p.bookingid
                from payment p
                    Inner Join booking b on b.bookingid = p.bookingid
                    Inner Join room r on r.roomid = b.roomid
                    Left Join groupguest gg on gg.groupguestid = b.groupguestid
                    Inner Join ratetype rt on rt.ratetypeid = b.ratetypeid
                    Inner Join roomtype rmt on rmt.roomtypeid = r.roomtypeid
                WHERE not paymentdelete and not bookingdelete
            """
        values = []
        cols = ['Room No.', 'Group ', 'PAX', 'Months', 'Days', 'Room Rate', 'Room Fee', 'Discount', 'bookingid']

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
            df = df[['Room No.', 'Group ', 'PAX', 'Months', 'Days', 'Room Rate', 'Room Fee', 'Discount', 'Action']]
            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center', 'font-size': '12px'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate

