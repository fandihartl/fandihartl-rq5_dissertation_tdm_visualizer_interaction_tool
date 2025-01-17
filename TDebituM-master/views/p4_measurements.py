
import plotly.graph_objects as go

from dash import dcc, html, dash_table, Input, Output
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from dash_app import app
from configuration import *

from ChartFactory import Table


def get_chart(relationship, discipline):
    return Table(relationship, discipline, measure="MeasureIdeal")

@app.callback(
    Output('table-overview', 'children'),
    Input('radio-buttons-affects-2', 'value'),
    Input('dropdown-discipline-involved', 'value'))
def update_chart(relationship, discipline):
    chart = get_chart(relationship, discipline)

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
            Table that displays all the open TD issues with the measures that
            need to be taken to solve them (MeasureIdeal).
            It can be filtered by discipline and by its relationship with the TD issue.
            Every column can be sorted.
        """]),
    ]

    layout = html.Div([
        dbc.Row(
                [
                    dbc.Col(
                        html.H2("Overview / Measurements")
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
            children=html.Div([], id='table-overview')
        ),
    ])

    radio_affects = [
        dbc.Label("Initiates TD or is affected"),
        html.Div([
            dbc.RadioItems(
                id="radio-buttons-affects-2",
                className="btn-group",
                labelClassName="btn btn-primary",
                labelCheckedClassName="active",
                labelStyle={"width": "120px"},
                #labelCheckedStyle={"color":"red"},
                options=[
                    {'label': 'All', 'value': 'All'},
                    {'label': 'Initiates', 'value': 'INITIATES'},
                    {'label': 'Affects', 'value': 'AFFECTS'},
                    
                ],
                value="All",
            ),
        ], 
        className="radio-group"
        )
    ]

    dropdown_discipline = [
        dbc.Label("Involved discipline"),
        dcc.Dropdown(
            id='dropdown-discipline-involved',
            options=[
                {'label': 'All disciplines', 'value': 'All'},
                {'label': 'Mechanical Engineering', 'value': 'ME'},
                {'label': 'Electronical Engineering', 'value': 'EE'},
                {'label': 'Software Engineering', 'value': 'SE'},

                {'label': 'Management', 'value': 'MA'},

                {'label': 'Sales', 'value': 'SAL'},
                {'label': 'Verkauf', 'value': 'VER'},
                {'label': 'Purchase', 'value': 'PUR'},
            ],
            value='All'
        )
    ]

    controls = radio_affects + dropdown_discipline

    return layout, controls


if __name__ == '__main__':
    main()

