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
                                dbc.Col(html.H2('Guest Arrival Report', style={'color': '#8A1538'}), width = 'auto'),
                                dbc.Col(html.H6('Generate reports on guest arrivals.'), width = 'auto')
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
                            html.H4("Arrivals Chart"),
                            html.P("Generate charts on guest arrivals. Includes booking status: Booked, Confirmed, Closed"),
                            html.Div(dbc.Form(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Label("Duration", width = 1),
                                                dbc.Col(dcc.DatePickerRange(id = 'arrivalreport_durationfilter', start_date_placeholder_text = 'Start Date', end_date_placeholder_text = 'End Date', display_format = "YYYY-MM-DD"), width = 3)
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
                            dcc.Loading(id = 'arrivalreport_bodyload', children = [dcc.Graph(id = 'arrivalreport_bodyreceipts')], type = "circle")
                        ],
                        style = {'width': '100%', "border": '3px #5c5c5c solid'}
                    ),
                    html.Br(),
                    html.Hr(),
                    html.Div(
                        [
                            html.H4("Daily Arrivals"),
                            html.P("Generate lists on guest arrivals per day. Includes booking status: Booked, Confirmed, Closed"),
                            dbc.Form(
                                dbc.Row(
                                    [
                                        dbc.Label("Check-In Date", width = 2),
                                        dbc.Col(dcc.DatePickerSingle(id = 'arrivalreport_datefilter', placeholder = "YYYY/MM/DD", display_format = "YYYY-MM-DD"), width = 3),
                                    ],
                                    className = 'mb-3'
                                )
                            )
                        ]
                    ),
                    html.Div("Table with report", id = 'arrivalreport_reporttable'),
                ],
            )
        ]
        )
    ]
)


@app.callback(
    [
        Output('arrivalreport_bodyreceipts', 'figure')
    ],
    [
        Input('url', 'pathname'),
        Input('arrivalreport_durationfilter','start_date'),
        Input('arrivalreport_durationfilter','end_date'),
    ],
)
  
def report_loadarrivalgraph (pathname, startdate, enddate):
    if pathname == '/reports/guestarrival':
        sql = """
            SELECT checkindate, roomtype, count(b.bookingid) FROM booking b
                INNER JOIN room r ON r.roomid = b.roomid
                INNER JOIN roomtype rt ON rt.roomtypeid = r.roomtypeid
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
        values = []

        if startdate and enddate:
            sql += "AND checkindate >= %s and checkindate <= %s"
            values += [startdate, enddate]

            sql += """
                Group By roomtype, checkindate
                Order By checkindate, roomtype
                """
            cols = ['Checkin Date','Room Type','Number of Arrivals']
            df = db.querydatafromdatabase(sql, values, cols)
            df = df[['Checkin Date','Room Type','Number of Arrivals']]

            listofroomtype = df["Room Type"].unique().tolist()
            traces = {}

            colors = ['#3E9651', '#922428' , '#396AB1','#535154', '#DA7C30', '#FCE205']
            i = 0

            for roomtype in listofroomtype:
                traces['tracebar_' + roomtype] = go.Bar(
                    y = df[df["Room Type"] == roomtype]["Number of Arrivals"], 
                    x = df[df["Room Type"] == roomtype]["Checkin Date"],
                    marker=dict(color=colors[i]),
                    name = roomtype)
                i+=1
            
            data = list(traces.values())

            layout = go.Layout(
                yaxis1 = {'categoryorder':'total ascending','title':"Number of Arrivals", 'range':[0,10]},
                xaxis = {'title':"Arrival Dates", "mirror":False, "zeroline":True},
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
        Output('arrivalreport_reporttable','children')
    ],
    [
        Input('url','pathname'),
        Input('arrivalreport_datefilter', 'date')
    ]
)

def loadguestarrival (pathname, searchterm):
    if pathname == '/reports/guestarrival':    
        sql = """Select 
            roomnumber, 
            statusname, 
            concat(surname,', ',firstname,' ',middlename) as guestname,
            concat(checkindate,' - ',checkoutdate) as duration, 
            monthsduration, 
            daysduration, 
            hourextension, 
            discountpercentage,
            ratetype,
            case
                when b.ratetypeid = 1 then residentrate
                when b.ratetypeid = 2 then transientrate
            end as roomrate,
            earnedroomfee,
            discountamount,
            extensioncharges,
            additionalcharges,
            totalamount,
            deposit,
            balance,
            p.bookingid
            from payment p
                inner join booking b on p.bookingid = b.bookingid
                inner join room r on r.roomid = b.roomid
                inner join (
                    SELECT sc.*, ROW_NUMBER() OVER (PARTITION BY sc.bookingid ORDER BY sc.statusmodifieddate DESC) AS rn FROM statuschange sc) 
                    AS sc ON b.bookingid = sc.bookingid AND sc.rn = 1
                inner join statusname sn on sn.statusnameid = sc. statusnameid
                inner join guest g on g.guestid = b.guestid
                left join discount d on d.discountid = b.discountid
                left join ratetype rt on rt.ratetypeid = b.ratetypeid
                left join roomtype rmt on rmt.roomtypeid = r.roomtypeid
                where not paymentdelete 
                and not bookingdelete
            """
        values = []
        cols = ['Room No.', 'Status', 'Guest', 'Duration', 'Months', 'Days', 'Hours', '%', 'Type', 'Room Rate', 'Room Fee', 'Discount', 'Extension Fee', 'Addtl Charges', 'Total', 'Deposit', 'Balance', 'bookingid']

        if searchterm:
            sql += "AND checkindate = %s"
            values += [f"%{searchterm}%"]
        
        sql += "ORDER BY roomnumber ASC"
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for booking_id in df['bookingid']:
                buttons += [
                    html.Div(dbc.Button('View Booking', href = f'/bookings/bookings_profile?mode=edit&id={booking_id}', size = 'sm', color = 'warning'), style = {'text-align':'center'})
                ]
            df['Action'] = buttons
            df = df[['Room No.', 'Status', 'Guest', 'Duration', 'Months', 'Days', 'Hours', '%', 'Type','Room Rate', 'Room Fee', 'Discount', 'Extension Fee', 'Addtl Charges', 'Total', 'Deposit', 'Balance', 'Action']]
            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate