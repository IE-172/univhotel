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
import plotly.express as px

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.Div([
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.H2('Booking Activities Report', style={'color': '#8A1538'}), width = 'auto'),
                                dbc.Col(html.H6('Generate reports on booking activities.'), width = 'auto')
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
                            html.H4("Booking Activities Chart and List"),
                            html.P("Generate charts and lists on booking activities."),
                            html.Div(dbc.Form(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Label("Duration", width = 1),
                                                dbc.Col(dcc.DatePickerRange(id = 'activitiesreport_durationfilter', start_date_placeholder_text = 'Start Date', end_date_placeholder_text = 'End Date', display_format = "YYYY-MM-DD"), width = 3)
                                            ],
                                            className = 'mb-3'
                                        )
                                    ]
                                )
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.Div(
                                [
                                    dcc.Loading(id = 'activitiesreport_bodyload', children = [dcc.Graph(id = 'activitiesreport_bodyreceipts')], type = "circle")
                                ],
                                style = {'width': '100%', "border": '3px #5c5c5c solid'}
                            ),
                            width = 8
                            ),
                            dbc.Col(html.Div("Table with report", id = 'activitiesreport_reporttable'), width = 4),
                        ]
                    ),
                    html.Br(),
                    html.Hr(), 
            
                    html.Div("Table with report", id = 'activitiesreport_bookingslist'),
                ],
            )
        ]
        )
    ]
)

@app.callback(
    [
        Output('activitiesreport_bodyreceipts', 'figure')
    ],
    [
        Input('url','pathname'),
        Input('activitiesreport_durationfilter', 'start_date'),
        Input('activitiesreport_durationfilter', 'end_date')
    ]
)

def activitiesreportloadgraph (pathname, startdate, enddate):
    if pathname == '/reports/bookingactivities':
        sql = """
            select sn.statusnameid, statusname, checkindate, count(b.bookingid) as count from booking b
            LEFT JOIN
            (
            SELECT sc.*,
            ROW_NUMBER() OVER (PARTITION BY sc.bookingid ORDER BY sc.statusmodifieddate DESC) AS rn
            FROM statuschange sc
            ) AS sc ON b.bookingid = sc.bookingid AND sc.rn = 1
            inner join statusname sn on sn.statusnameid=sc.statusnameid
            where not bookingdelete
            """
        values = []

        if startdate and enddate:
            sql += "AND checkindate >= %s and checkindate <= %s"
            values += [startdate, enddate]
        
            sql += """
                group by sn.statusnameid, checkindate, statusname
                order by checkindate, statusname
                """
            cols = ['ID','Status Name', 'Checkin Date', 'Count']
            df = db.querydatafromdatabase(sql, values, cols)

            df = df[['Status Name', 'Checkin Date', 'Count']]
            

            listofstatus = df["Status Name"].unique().tolist()
            traces = {}
            
            colors = ['#3E9651', '#922428' , '#396AB1','#535154', '#DA7C30', '#FCE205']
            i = 0

            for status in listofstatus:
                traces['tracebar_' + status] = go.Bar(
                    y = df[df["Status Name"] == status]["Count"], 
                    x = df[df["Status Name"] == status]["Checkin Date"],
                    marker=dict(color=colors[i]),
                    name = status)
                i+=1

            data = list(traces.values())
            layout = go.Layout(
                yaxis1 = {'categoryorder':'total ascending','title':"Number of Bookings", 'range':[0,20]},
                xaxis = {'title':"Date",
                          "mirror":False,
                          "zeroline":True,
                          'tickangle': 45
                          },
                height = 500,
                width = 850,
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
        Output('activitiesreport_reporttable','children')
    ],
    [
        Input('url','pathname'),
        Input('activitiesreport_durationfilter', 'start_date'),
        Input('activitiesreport_durationfilter', 'end_date')
    ]
)

def loadbookingactivities (pathname, startdate, enddate):
    if pathname == '/reports/bookingactivities':    
        sql = """ 
            select sn.statusnameid, statusname, count(b.bookingid) as count from booking b
            LEFT JOIN
            (
            SELECT sc.*,
            ROW_NUMBER() OVER (PARTITION BY sc.bookingid ORDER BY sc.statusmodifieddate DESC) AS rn
            FROM statuschange sc
            ) AS sc ON b.bookingid = sc.bookingid AND sc.rn = 1
            inner join statusname sn on sn.statusnameid=sc.statusnameid
            where not bookingdelete
            """
        values = []
        cols = ['ID','Status Name', 'Count']

        if startdate and enddate:
            sql += "AND checkindate >= %s and checkindate <= %s"
            values += [startdate, enddate]
        
        sql += """
            group by sn.statusnameid, statusname
            order by statusname
            """
        df = db.querydatafromdatabase(sql, values, cols)

        df = df[['Status Name', 'Count']]
        table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center', 'font-size': '12px'})
        return [table]
    
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('activitiesreport_bookingslist','children')
    ],
    [
        Input('url','pathname'),
        Input('activitiesreport_durationfilter', 'start_date'),
        Input('activitiesreport_durationfilter', 'end_date')
    ]
)

def loadbookinglist (pathname, checkindate, checkoutdate):
    if pathname == '/reports/bookingactivities':  
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
                #AND NOT sc.statusnameid = 4
                #AND NOT sc.statusnameid = 5
            
        values = []
        cols = ['Room No.', 'Guest', 'PAX', 'Check-In Date', 'Check-Out Date', 'Status', 'Booking ID']
        
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
                    html.Div(dbc.Button('View Booking', href = f'/bookings/bookings_profile?mode=edit&id={booking_id}', size = 'sm', color = 'warning'), style = {'text-align':'center', 'font-size': '12 px'})
                ]
            df['Action'] = buttons
            df = df[['Room No.', 'Guest', 'PAX', 'Check-In Date', 'Check-Out Date', 'Status', 'Action']]
            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center', 'font-size': '12 px'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate

