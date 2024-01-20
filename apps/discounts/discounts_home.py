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
                html.Div([html.H2('Offered Discounts', style={'color': '#8A1538','margin-top': '15px'})], style = {'margin-left':'40px','font-weight':'bold','float':'left'}),
                html.Div([dbc.Button("Add New Discount", href='/discounts/discounts_profile?mode=add', style={'backgroundColor': '#00573F', 'color': 'white', 
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
                                    dbc.Label("Search Discount", style={'text-align':'right','color': '#000000','font-weight':'bold'}, width = 2),
                                    dbc.Col(dbc.Input(id = 'discountshome_discountfilter', placeholder = 'Discount Type', type = 'text'), style={'text-align':'left'}, width = 2),
                                ],
                                className = 'mb-3'
                            )
                        )
                    ),
                    html.Div("Table with Discounts", id = 'discountshome_discountlist',style={'background-color':'#ffffff','width': '75%','margin-right': '175px', 'margin-left': '175px'}),
                ],
                style={'background-color':'#ffffff','margin-left':'20px','margin-right':'20px'}
            )
        ],
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
        Output('discountshome_discountlist','children')
    ],
    [
        Input('url','pathname'),
        Input('discountshome_discountfilter', 'value')
    ]
)

def loaddiscountslist (pathname, searchterm):
    if pathname == '/discounts/discounts_home':    
        sql = """
            select discounttype, discountpercentage, discountid from discount
	        where not discountdelete
            """
        values = []
        cols = ['Discount Type', '%', 'ID']

        if searchterm:
            sql += "AND discounttype ILIKE %s"
            values += [f"%{searchterm}%"]
        
        sql += "ORDER BY discounttype ASC"
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for discount_id in df['ID']:
                buttons += [
                    html.Div(dbc.Button('View Details', href = f'/discounts/discounts_profile?mode=edit&id={discount_id}', size = 'sm', color = 'warning'), style = {'text-align':'center'})
                ]
            df['Action'] = buttons
            df = df[['Discount Type', '%', 'Action']]
            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align':'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate


