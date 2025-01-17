from logging import info
from random import seed
from sre_parse import State
from ChartFactory import BubbleChart
import plotly.graph_objects as go
import plotly.express as px
import dash_table
#from fig import fig


from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from dash_app import app
from configuration import *
import scipy.stats as stats
import numpy as np
import pandas as pd
from scipy.stats.stats import fisher_exact


# read the excel sheet (TD_datasource)
xl_file_Tabelle1 = pd.read_excel("C:\\Users\\sarya\\Downloads\\TD_datasource_71.xlsx", sheet_name= "Tabelle1")
xl_file_p_value = pd.read_excel("C:\\Users\\sarya\\Downloads\\pValue.xlsx")

def main():
    popover_children = [
        dbc.PopoverHeader("Page Information"),
        dbc.PopoverBody(["""
            This Table shows the p-values of Chi-square test for any two selected
            columns in TD excel file. You can select the columns in the righthand side of the page 
            using the two dropdowns, then please press submit to udate the table.

            If the P-value is less than the predefined significance level (0.05), 
            then the column and row headers are dependent, this cell will be highlighted in green

            The table in the bottom righthand side shows the dependacies 

            P.S it may take some minutes to update the table

        """]),
    ]
    
    layout = html.Div([
        dbc.Row(
                [
                    dbc.Col(
                        html.H2("Correlations/Chi-Square Test")
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Info",
                            id="info-target",
                            color="success",
                            className="mr-1",
                            n_clicks=0,
                        ), 
                        width=1, style={"padding-top": "8px"}),
                ], 
                justify="between"   
        ),
        
        dbc.Popover(
                popover_children,
                id="info-popover",
                target="info-target",
                placement='right',
                trigger="focus",
        ),
    
        dbc.Row(
            dbc.Col(
                html.Div(id="update_table")
        )
        )       
        #dcc.Dropdown(["TD Type","TD Subtype (Li+own)","Cause","Domain","TD incident description","PLC","Company Size","Position"],"TD Type", id="first_dropdown")

    ])
    controls=html.Div([
        dbc.Row([
            dbc.Col([
                html.H3("First Column",className="text-left, width=1"),
                dcc.Dropdown(id="first_dropdown",value="TD Type",options= [
                                                                    {'label':'TD Type','value':'TD Type'},
                                                                    {'label':'TD Subtype (Li+own)','value':'TD Subtype (Li+own)'},
                                                                    {'label':'Cause','value':'Cause'},
                                                                    {'label':'Domain','value':'Domain'},
                                                                    {'label':'TD incident description','value':'TD incident description'},
                                                                    {'label':'PLC','value':'PLC'},
                                                                    {'label':'Company Size','value':'Company Size'},
                                                                    {'label':'Position','value':'Position'}
                                                                            ]
                            )

                    ]
                    )
        ]),
        dbc.Row([
            dbc.Col([
                html.H3("Second Column",className="text-left, width=1"),
                dcc.Dropdown(id="second_dropdown",value='TD Type',options= [
                                                                    {'label':'TD Type','value':'TD Type'},
                                                                    {'label':'TD Subtype (Li+own)','value':'TD Subtype (Li+own)'},
                                                                    {'label':'Cause','value':'Cause'},
                                                                    {'label':'Domain','value':'Domain'},
                                                                    {'label':'TD incident description','value':'TD incident description'},
                                                                    {'label':'PLC','value':'PLC'},
                                                                    {'label':'Company Size','value':'Company Size'},
                                                                    {'label':'Position','value':'Position'}
                                                                            ]
                            )
                    ])
                ]),
        dbc.Row([
            dbc.Col([
                html.Button(id='trigger_button', n_clicks = 0, children="submit")
            ])
        ]

        ),
        dbc.Row([
            dbc.Card([
                dbc.FormGroup(
                    [
                        html.H4("Dependencies Table"),
                        html.Div(id="update_correlation")

                    ]
                )],
            body=True,
            style={"width": "25rem", "position": "fixed",
                    "top": "32rem",
                    "right": 10,
                    'overflowY': 'scroll', 'height': 450},
            )]
        )
        ])
                        

    return layout, controls




if __name__ == '__main__':
    main()