from logging import info
from ChartFactory import BubbleChart
import plotly.graph_objects as go

from dash import dcc, html, Input, Output
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from dash_app import app
from configuration import *


def get_chart(relationship, state):
    return BubbleChart(relationship, state)

def clean_clicked_label(label_raw):
    label_split = label_raw.split("<br>")
    label = ' '.join(label_split)[:-1]

    return label

def get_header_info(selected_info):
    
    if selected_info == "TDIncident":
        header_info = "Info TD Incidents"

    elif selected_info == "Cause":
        header_info = "Causes of TD"

    elif selected_info == "MeasureIdeal":
        header_info = "Measures to solve TD"

    elif selected_info == "MeasureTaken":
        header_info = "Taken measures"

    return header_info


# TODO: define general function for all sources, use it for causes_initiated by party "all"
# parties, causes, info, index_parties, index_causes = causes_initiated_by_party("All")
@app.callback(
    Output('scatter', 'figure'),
    Input('dropdown-affects', 'value'),
    Input('dropdown-currentstate-2', 'value'))
def update_chart(relationship, state):

    chart = get_chart(relationship, state)

    data = go.Scatter(
        x=chart.x, 
        y=chart.y,
        mode='markers',
        # marker_size=chart.amount,
        # marker_color=chart.colors,
        marker=dict(
            size=chart.amount,
            color=chart.amount, #set color equal to a variable
            colorscale='Viridis', # one of plotly colorscales
            reversescale=True,
            showscale=True
            ),
        text=[f"{n} TD items" for n in chart.amount]
        )

    fig = go.Figure(data=data)
    fig.update_layout(height=700, template="plotly_white", margin=dict(l=20, r=20, t=5, b=5))

    # text = [f"Size: {size}" for size in output_amount]
    return fig

@app.callback(
    Output('info_title_bubble', 'children'),
    Output('info_header_bubble', 'children'),
    Output('info_content_bubble', 'children'),
    Input('scatter', 'clickData'),
    Input('dropdown-affects', 'value'),
    Input('dropdown-currentstate-2', 'value'))
def display_info_on_click(clickData, relationship, state_selected): #, child, filter_state, selected_info):
    '''
    When a specific child (TD Subtype) is clicked, in the right bottom panel it displays
    information about it. The content can be selected also with a dropdown menu.

    Args:
        clickData ([type]): [description]
        child ([type]): [description]
        filter ([type]): [description]
        selected_info ([type]): [description]

    Returns:
        [type]: [description]
    '''

    if (clickData == None) or ("x" not in clickData["points"][0].keys()):
        title_info = ""
        header_info = ""
        content = "click a TD element to show info about it"

    else:
        clicked_x = clickData["points"][0]["x"]
        clicked_y = clickData["points"][0]["y"]
        clicked_color = clickData["points"][0]["marker.color"]

        title_info = f"{clicked_y} ({clicked_x})" 
        header_info = "TD Subtypes"
        
        if clicked_color == 'rgb(93, 164, 214)':
            state = "All"
        else:
            state = state_selected
            header_info = f"{state} {header_info}"
        chart = get_chart(relationship, state)

        
        content = chart.extract_info(party=clicked_y, td_type=clicked_x)
        
    
    return title_info, header_info, content

def main():
    popover_children = [
        dbc.PopoverHeader("Page Information"),
        dbc.PopoverBody(["""
            Grid of TD types among disciplines, where the Bubble size is 
            the amount of TD issues (affecting the discipline or created by it).
            
            The items can be filtered by their status.

            When a specific bubble is clicked, the right bottom panel displays
            information about it. 
        """]),
    ]
    
    layout = html.Div([
        dbc.Row(
                [
                    dbc.Col(
                        html.H2("Overview / Status of Technical Debt")
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
                children=html.Div([
                    dcc.Graph(id="scatter")
                    ])
            ),
        html.Div([
            dbc.Card([
                dbc.FormGroup(
                    [
                        html.H4("TD Info"),
                        html.Div([], id="info_title_bubble", style={"font-style": "italic"}),
                        html.Hr(),
                        html.H5([], id="info_header_bubble"),
                        html.Div([], id="info_content_bubble"),

                    ]
                )],
            body=True,
            style={"width": "25rem", "position": "fixed",
                    "top": "24rem",
                    "right": 10,
                    'overflowY': 'scroll', 'height': 450},
            )]
        )
    ])

    radio_dropdown_affects = [
        dbc.Label("Initiates TD or is affected"),
        html.Div(
            [
                dbc.RadioItems(
                    id="dropdown-affects",
                    className="btn-group",
                    labelClassName="btn btn-primary",
                    labelCheckedClassName="active",
                    labelStyle={"width": "120px"},
                    #labelCheckedStyle={"color":"red"},
                    options=[
                        {'label': 'Initiates', 'value': 'INITIATES'},
                        {'label': 'Affects', 'value': 'AFFECTS'},
                    ],
                    value="INITIATES",
                ),
            ], className="radio-group"
        )
    ]

    dropdown_currentstate = [
        dbc.Label("Current State"),
        dcc.Dropdown(
            id='dropdown-currentstate-2',
            options=[
                {'label': "All", 'value': "All"},
                {'label': "Solved", 'value': "Solved"},
                {'label': "Another workaround", 'value': "Another workaround"},
                {'label': "Not solved yet", 'value': "Not solved yet"},
                {'label': "Nothing yet", 'value': "Nothing yet"},
                {'label': "Not yet", 'value': "Not yet"},
                {'label': "Redesign", 'value': "Redesign"},
                {'label': "Solution refused", 'value': "Solution refused"},
            ],
            value='All'
        )
    ]

    controls = radio_dropdown_affects + dropdown_currentstate

    return layout, controls


if __name__ == '__main__':
    main()
