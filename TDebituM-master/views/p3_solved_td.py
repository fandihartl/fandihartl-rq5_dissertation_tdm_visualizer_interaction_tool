from dash import dcc, html, dash_table, Input, Output
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Group

from dash_app import app
from configuration import *
from ChartFactory import Table




def get_chart(relationship):
    return Table(relationship, measure = "MeasureTaken")

@app.callback(
    Output('table-measure', 'children'),
    Input('radio-buttons-affects', 'value'))
def update_chart(relationship):
    chart = get_chart(relationship)

    data_table = dash_table.DataTable(
            # style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            sort_action='native',
            style_cell=chart.style_cell,
            style_data_conditional=chart.style_data_conditional,
            columns=chart.columns,
            data=chart.data,
        )

    return data_table

def main():
    popover_children = [
        dbc.PopoverHeader("Page Information"),
        dbc.PopoverBody(["""
            Table that displays all the TD issues that have been solved and how
            have they been solved (MeasurementsTaken).
            It can be selected the relationship of the Disciplines with the TD issue.
            Every column can be sorted.
        """]),
    ]

    layout = html.Div([
        dbc.Row(
                [
                    dbc.Col(
                        html.H2("Overview / Solved Technical Debt")
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
                placement='left',
                trigger="focus",
        ),
        html.Hr(),
        dcc.Loading(
                id="loading",
                type="dot",
                children=html.Div([], id='table-measure')
            ),
    ])


    # TODO: add checklist to choose columns
    
    radio_affects = [
            dbc.Label("Disciplines relationship"),
            html.Div([
                dbc.RadioItems(
                    id="radio-buttons-affects",
                    className="btn-group",
                    labelClassName="btn btn-primary",
                    labelCheckedClassName="active",
                    labelStyle={"width": "120px"},
                    #labelCheckedStyle={"color":"red"},
                    options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'Initiated', 'value': 'INITIATES'},
                        {'label': 'Affected', 'value': 'AFFECTS'},
                        
                    ],
                    value="All",
                ),
            ], 
            className="radio-group"
            ),
        ]
                
    controls = radio_affects
    
    return layout, controls

if __name__ == '__main__':
    main()