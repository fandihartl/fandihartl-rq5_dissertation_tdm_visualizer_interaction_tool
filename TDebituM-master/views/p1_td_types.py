''' 
Overview/TD Types view

Creates a dynamic Sunburst chart that offers a general view of the distribution
of td types and td subtypes, or the distribution of td among disciplines and
the type of it. The displayed information can be changed using a button in the UI.
The data displayed can be filtered regarding the status of the td issues using a
dropdown menu.

contains the following functions:
    * get_chart: returns a ChartFactory.Sunburst object
    * main: the main function of the script
callbacks:
    * update_chart
    * display_info_on_click

Returns:
    layout (list): child of the component with id="page-content"
    controls (list): child of the component with id="page-content"
'''
import plotly.graph_objects as go

from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

from dash_app import app
from configuration import *
from ChartFactory import Sunburst


def get_chart(parent, child, filter_state, info=""):
    '''[summary]

    Args:
        parent ([type]): [description]
        child ([type]): [description]
        filter_state ([type]): [description]
        info (str, optional): [description]. Defaults to "".

    Returns:
        [type]: [description]
    '''
    return Sunburst(parent, child, filter_state, info)

def clean_clicked_label(label_raw) -> list:
    '''[summary]

    Args:
        label_raw ([type]): [description]

    Returns:
        [type]: [description]
    '''
    label_split = label_raw.split("<br>")
    label = ' '.join(label_split)[:-1]

    return label

def get_header_info(selected_info) -> str:
    '''[summary]

    Args:
        selected_info ([type]): [description]

    Returns:
        [type]: [description]
    '''
    
    if selected_info == "TDIncident":
        header_info = "Info TD Incidents"

    elif selected_info == "Cause":
        header_info = "Causes of TD"

    elif selected_info == "MeasureIdeal":
        header_info = "Measures to solve TD"

    elif selected_info == "MeasureTaken":
        header_info = "Taken measures"

    return header_info


@app.callback(
    Output('sunburst', 'figure'),
    Input('type-of-graph', 'value'),
    Input('radio-td-type-party', 'value'),
    Input('dropdown-currentstate', 'value'))
def update_chart(type_graph, parent, filter_state):
    '''
    Updates the Sunburst Chart with the UI input

    Args:
        child (str: Value of radio-td-type-party): Selected radio button. Is the first layer of the graph
        filter (str: Value of dropdown-currentstate): Selected value of the current sate, to filter the data displayed

    Returns:
        go.Figure(): Updated Sunburst figure with the corresponding Inputs from the UI
    '''
    if parent == 'TDType':
        child = 'TDSubtype'
    elif parent == 'Party':
        child = 'TDType'

    chart = get_chart(parent, child, filter_state)
    

    # TODO: icicle with continuous colorscale (criticallity)
    if type_graph == 'Sunburst':
        data = go.Sunburst(
            ids=chart.ids,
            parents=chart.parents,
            labels=chart.get_labels(30),
            values=chart.values,
            hoverinfo='label+value+percent parent+percent entry+percent root',
            # pathbar=dict(visible=True)
            insidetextorientation='radial',
            # outsidetextfont=dict(family="Arial")
        )

    elif type_graph == 'Treemap':
        data = go.Treemap(
            ids=chart.ids,
            parents=chart.parents,
            labels=chart.get_labels(15),
            values=chart.values,
            hoverinfo='label+value+percent parent+percent entry+percent root',
        )

    fig = go.Figure(data=data)
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=750, 
        uniformtext=dict(minsize=10, mode='hide'))

    return fig

@app.callback(
    Output('title_info', 'children'),
    Output('header_info', 'children'),
    Output('content', 'children'),
    Input('sunburst', 'clickData'),
    Input('radio-td-type-party', 'value'),
    Input('dropdown-currentstate', 'value'),
    Input('dropdown-info', 'value'))
def display_info_on_click(clickData, parent, filter_state, selected_info):
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

    if parent == 'TDType':
        child = 'TDSubtype'
    elif parent == 'Party':
        child = 'TDType'


    if (clickData == None) or ("parent" not in clickData["points"][0].keys()):
        title_info = ""
        header_info = ""
        content = "click a TD element to show info about it"

    else:
        clicked_parent = clickData["points"][0]["parent"]
        clicked_label = clean_clicked_label(clickData["points"][0]["label"])
        chart = get_chart(parent, child, filter_state, selected_info)

        title_info = f"{clicked_label} ({clicked_parent})"
        header_info = get_header_info(selected_info)
        content = chart.get_info(clicked_parent, clicked_label)
        
    return title_info, header_info, content

def main():
    '''[summary]

    Returns:
        layout.child
        controls.child
    '''
    popover_children = [
        dbc.PopoverHeader("Page Information"),
        dbc.PopoverBody(["""
            Distribution of td types and td subtypes, 
            (or TD types among disciplines).\n
            
            The TD issues can be filtered by their status.

            When a specific child is clicked, the right bottom panel displays
            information about it. 
        """]),
    ]

    # todo: do the same with controls. combination of title and info, popover, loading, info panel
    layout = html.Div([
        dbc.Row(
                [
                    dbc.Col(
                        html.H2("Overview / Types of Technical Debt")
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
                placement='left-start',
                trigger="focus",
        ),

        html.Hr(),
        dcc.Loading(
                id="loading",
                type="dot",
                children=html.Div([
                    dcc.Graph(id="sunburst") # Definition of the graph. It gets updated with the callback
                    ])
            ),
        html.Div([
            dbc.Card([
                dbc.FormGroup(
                    [
                        html.H4("TD Info"),
                        html.Div([], id="title_info", style={"font-style": "italic"}),
                        html.Hr(),
                        html.H5([], id="header_info"),
                        html.Div([], id="content"),

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

    # TODO: add input to choose type of diagram
    # TODO: compare same control elements and see which attributes are repeated. do class defining the necessary inputs
    # NOTE: label title, id, options(label and value: can be the same or different)
    radio_type_graph = [
        dbc.Label("Type of Graph"),
        html.Div(
            [
                dbc.RadioItems(
                    id="type-of-graph",
                    className="btn-group",
                    labelClassName="btn btn-primary",
                    labelCheckedClassName="active",
                    labelStyle={"width": "120px"},
                    #labelCheckedStyle={"color":"red"},
                    options=[
                        {"label": "Sunburst", "value": "Sunburst"},
                        {"label": "Treemap", "value": "Treemap"},
                    ],
                    value="Sunburst",
                )
            ], 
            className="radio-group",
        )
    ]

    radio_display = [
        dbc.Label("Display"),
        html.Div(
            [
                dbc.RadioItems(
                    id="radio-td-type-party",
                    className="btn-group",
                    labelClassName="btn btn-primary",
                    labelCheckedClassName="active",
                    labelStyle={"width": "120px"},
                    #labelCheckedStyle={"color":"red"},
                    options=[
                        {"label": "TD Subtype", "value": "TDType"},
                        {"label": "Party", "value": "Party"}
                    ],
                    value="TDType",
                )
            ], 
            className="radio-group",
        )
    ]

    dropdown_state = [
        dbc.Label("Current State"),
        dcc.Dropdown(
                id='dropdown-currentstate',
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

    dropdown_info = [
        dbc.Label("Info OnClick"),
        dcc.Dropdown(
                id='dropdown-info',
                options=[
                    {'label': "Incident Info", 'value': "TDIncident"},
                    {'label': "Cause", 'value': "Cause"},
                    {'label': "Measure Ideal", 'value': "MeasureIdeal"},
                    {'label': "Measure Taken", 'value': "MeasureTaken"},
                ],
                value='TDIncident'
        )
    ]

    controls = radio_type_graph + radio_display + dropdown_state + dropdown_info
                
    return layout, controls



if __name__ == '__main__':
    main()
