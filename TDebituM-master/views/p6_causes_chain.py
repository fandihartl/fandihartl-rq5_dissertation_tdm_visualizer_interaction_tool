
import dash_cytoscape as cyto
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from dash_app import app
from configuration import *
from ChartFactory import NetworkGraph


def get_chart(incident, display):
    return NetworkGraph(incident, display)

@app.callback(
    Output('causes-chain', 'children'),
    Input('dropdown-update-layout', 'value'),
    Input('radio-td-type-cause', 'value'))
def update_chart(incident, display):
    chart = get_chart(incident, display)

    nodes = []
    for node, classes in chart.nodes:
        nodes.append({'data': {'id': node, 'label': node}, 'classes': classes})

    edges = []
    for source, target, label in chart.edges:
        edges.append({'data': {'source': source, 'target': target, 'label': label}, 'classes': label})
    
    network_graph = cyto.Cytoscape(
        # id='cytoscape-update-layout',
        layout={'name': 'breadthfirst', 'roots': f'[id = "{incident}"]'},
        style={'width': '100%', 'height': '750px'},
        elements=nodes + edges,
        stylesheet=chart.stylesheet
    )

    return network_graph


def main():
    popover_children = [
        dbc.PopoverHeader("Page Information"),
        dbc.PopoverBody(["""
            Network Graph that shows the chain of individual TD items (light blue nodes) inside a global 
            TD incident (top square node). For each TD item is shown its Cause and to which TD type is classified.
        """]),
    ]

    layout = html.Div([
        dbc.Row(
                [
                    dbc.Col(
                        html.H2("TD Spreading / Causes Chain")
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
            children=html.Div([], id='causes-chain')
        ),
    ])

    radio_cause = [   
        dbc.Label("Display Information (orange elements)"),
        html.Div(
            [
                dbc.RadioItems(
                    id="radio-td-type-cause",
                    className="btn-group",
                    labelClassName="btn btn-primary",
                    labelCheckedClassName="active",
                    labelStyle={"width": "120px"},
                    #labelCheckedStyle={"color":"red"},
                    options=[
                        {"label": "Cause", "value": "Cause"},
                        {"label": "TD Subtype", "value": "TDSubtype"},
                        {"label": "TD Type", "value": "TDType"}
                    ],
                    value="Cause",
                )
            ], className="radio-group",
        )
    ]

    dropdown_graph = [
        dbc.Label("Choose Graph"),
        dcc.Dropdown(
            id='dropdown-update-layout',
            value='Different versions of system and product',
            clearable=False,
            options=[
                {'label': 'Example 1', 'value': "Different versions of system and product"},
                {'label': 'Example 2', 'value': "hydraulic or electric gripper, purchasing chose cheaper intial costs"},
                {'label': 'Example 3', 'value': "From the outside project looks great, but quality of docs are bad"},
                {'label': 'Example 4', 'value': "different interfaces along one plant line with different interfaces"},
                {'label': 'Example 5', 'value': "part has to be taken over, no documentation about changes existed"},
                {'label': 'Example 6', 'value': "individual code for every machine, programmed on-site"},
            ]
        )
    ]

    controls = radio_cause + dropdown_graph
               
    return layout, controls

if __name__ == '__main__':
    main()


