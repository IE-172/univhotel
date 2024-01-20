from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd


from app import app
from apps import dbconnect as db


navlink_style = {
   'color': '#8A1538'
}

navbar = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.H6(f'Logged in as: ', style={'color': '#8A1538', 'text-align': 'right', 'padding-right': '7px','font-size': '17px'}), width=1),
                dbc.Col(html.H6(id='staffname', style={**navlink_style, 'font-weight': 'bold','font-size': '17px'}), width=2),
                dbc.Col(width=1),
                dbc.Col(html.Div(html.Img(src=r'assets/univhotellogo.png', style={'width': '20%','margin-right': '125px'}), className='d-flex justify-content-center mx-auto')),
                dbc.Col(width=1),
                dbc.Col(html.Div(dbc.Button("Log Out", href='/logout', style={'backgroundColor': '#8A1538', 'color': 'white', 'padding': '7px', 'font-weight': 'bold', 'margin-left': 'auto', 'margin-right': '20px', 'font-size': '14px'}), style={'float': 'right'}), width=2),
            ],
            className="g-0 mx-2",
            align="end"
        ),
        html.Br(),
        dbc.Nav([
            dbc.Col(dbc.NavItem(dbc.NavLink("HOME", href="/home", style={**navlink_style,'font-weight': 'bold','text-align': 'center','font-size': '17px'}))),
            dbc.Col(dbc.NavItem(dbc.NavLink("STAFF", href="/staff/login_home", style={**navlink_style,'font-weight': 'bold','text-align': 'center','font-size': '17px'}))),
            dbc.Col(dbc.NavItem(dbc.NavLink("DISCOUNTS", href="/discounts/discounts_home", style={**navlink_style,'font-weight': 'bold','text-align': 'center','font-size': '17px'}))),
            dbc.Col(dbc.NavItem(dbc.NavLink("ROOMS", href="/rooms/rooms_home", style={**navlink_style,'font-weight': 'bold','text-align': 'center','font-size': '17px'}))),
            dbc.Col(dbc.NavItem(dbc.NavLink("GUESTS", href="/guests/guests_home", style={**navlink_style,'font-weight': 'bold','text-align': 'center','font-size': '17px'}))),
            dbc.Col(dbc.NavItem(dbc.NavLink("BOOKINGS", href="/bookings/bookings_home", style={**navlink_style,'font-weight': 'bold','text-align': 'center','font-size': '17px'}))),
            dbc.Col(dbc.NavItem(dbc.NavLink("PAYMENTS", href="/payments/payments_home", style={**navlink_style,'font-weight': 'bold','text-align': 'center','font-size': '17px'}))),
            dbc.Col(dbc.NavItem(
                dbc.DropdownMenu(
                [
                dbc.DropdownMenuItem(dbc.NavLink("Booking Activities", href="/reports/bookingactivities", style={'color': '#8A1538','font-size': '17px'})),
                dbc.DropdownMenuItem(dbc.NavLink("Guest Arrival Report", href="/reports/guestarrival", style={'color': '#8A1538','font-size': '17px'})), 
                dbc.DropdownMenuItem(dbc.NavLink("Guest Departure Report", href="/reports/guestdeparture", style={'color': '#8A1538','font-size': '17px'})),
                dbc.DropdownMenuItem(dbc.NavLink("Occupancy Report", href="/reports/occupancy", style={'color': '#8A1538','font-size': '17px'})),
                dbc.DropdownMenuItem(dbc.NavLink("Room Sales Report", href="/reports/roomsales", style={'color': '#8A1538','font-size': '17px'})),
                ],
                label="REPORTS",
                style={'font-weight': 'bold','font-size': '17px'},
                nav=True
                ),
            ))
        ], fill = True, style = {'margin': 'auto','background-color': '#f5f5f5'}),
    ],
    style = {'background-image': 'url("assets/header.png")','background-repeat': 'repeat','align-items': 'center', 'height':'212.70px'}
)

@app.callback(
    [
        Output('staffname','children')
    ],
    [
        Input('url','pathname')
    ]
)

def getstaffname(pathname):
    sql = """SELECT stafffirstname from staff
        WHERE staffactive = true"""
    values = []
    col = ['stafffirstname']
    df = db.querydatafromdatabase(sql, values, col)
    staffname = (df['stafffirstname'][0]) if pd.notna(df['stafffirstname'][0]) else None
    return[staffname]
