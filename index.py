from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import webbrowser
import pandas as pd
from apps import dbconnect as db


from app import app
from apps import commonmodules as cm
from apps import home
from apps.login import login_credentials, login_page, login_home, login_fail
from apps.bookings import bookings_home, bookings_profile
from apps.guests import guests_home, guests_guestprofile, guests_groupprofile
from apps.reports import reports_guestarrival, reports_guestdeparture, reports_occupancy, reports_roomsales, reports_bookingactivities
from apps.discounts import discounts_home, discounts_profile
from apps.rooms import rooms_home, rooms_profile, roomtypes_profile
from apps.payments import payments_home, payments_profile


app.layout = html.Div(
    [
        dcc.Location(id='url', refresh = True),
        dcc.Store(id = 'sessionlogout', data=True, storage_type = 'session'),
        dcc.Store(id = 'currentuserid', data=-1, storage_type = 'session'),
        html.Div(cm.navbar, id = 'navbar_div'),
        html.Div(id = 'page-content', style = {'background-image': 'url("assets/backgroundimage.png")'}),
    ]
)

@app.callback(
    [
        Output('page-content', 'children'),
        Output('sessionlogout', 'data'),
        Output('navbar_div', 'className')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data')
    ]
)

def displaypage (pathname, sessionlogout, userid):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'url':
            if userid < 0:
                if pathname == '/':
                    returnlayout = login_page.layout
                else:
                    returnlayout = '404:request not found'
            else:

                sql = """ SELECT staffactive from staff where staffactive"""
                values = []
                col = ['staffactive']
                df = db.querydatafromdatabase(sql, values, col)
                if df.empty:
                    admin = True
                else:
                    sql = """SELECT staffaccess from staff
                        WHERE staffactive = true"""
                    values = []
                    col = ['access']
                    df = db.querydatafromdatabase(sql, values, col)
                    admin = bool(df['access'][0]) if pd.notna(df['access'][0]) else None

                if pathname == '/logout':
                    returnlayout = login_page.layout
                    sessionlogout = True
                elif pathname == '/' or pathname == '/home':
                    returnlayout = home.layout
                elif pathname == '/staff/login_home':
                    if admin == True:
                        returnlayout = login_home.layout
                    else:
                        returnlayout = login_fail.layout
                elif pathname == '/staff/login_credentials':
                    returnlayout = login_credentials.layout
                elif pathname == '/rooms/rooms_home':
                    returnlayout = rooms_home.layout
                elif pathname == '/rooms/rooms_profile':
                    returnlayout = rooms_profile.layout
                elif pathname == '/rooms/roomtypes_profile':
                    returnlayout = roomtypes_profile.layout          
                elif pathname == '/discounts/discounts_home':
                    returnlayout = discounts_home.layout
                elif pathname == '/discounts/discounts_profile':
                    returnlayout = discounts_profile.layout
                elif pathname == '/guests/guests_home':
                    returnlayout = guests_home.layout
                elif pathname == '/guests/guests_guestprofile':
                    returnlayout = guests_guestprofile.layout
                elif pathname == '/guests/guests_groupprofile':
                    returnlayout = guests_groupprofile.layout
                elif pathname == '/bookings/bookings_home':
                    returnlayout = bookings_home.layout
                elif pathname == '/bookings/bookings_profile':
                    returnlayout = bookings_profile.layout
                elif pathname == '/payments/payments_home':
                    returnlayout = payments_home.layout
                elif pathname == '/payments/payments_profile':
                    returnlayout = payments_profile.layout
                elif pathname == '/reports/bookingactivities':
                    returnlayout = reports_bookingactivities.layout
                elif pathname == '/reports/guestarrival':
                    returnlayout = reports_guestarrival.layout
                elif pathname == '/reports/guestdeparture':
                    returnlayout = reports_guestdeparture.layout
                elif pathname == '/reports/occupancy':
                    returnlayout = reports_occupancy.layout
                elif pathname == '/reports/roomsales':
                    returnlayout = reports_roomsales.layout
                else:
                    returnlayout = "error404"

            logout_conditions = [
                pathname in ['/', '/logout'],
                userid == -1,
                not userid
            ]
            
            sessionlogout = any(logout_conditions)
            
            navbar_classname = 'd-none' if sessionlogout else ''

            
        else:
            raise PreventUpdate
        
        return [returnlayout, sessionlogout, navbar_classname]

    else:
        raise PreventUpdate

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new = 0, autoraise = True)
    app.run_server(debug=False)
