import plotly.graph_objects as go

from dash import dcc, html, dash_table, Input, Output
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from dash_app import app
from ChartFactory import Sankey, Sunburst
from configuration import *



#todo: create function: layout = graph_layout(id)

def get_chart(party):
    return Sankey(party)

def get_chart_discipline_specific(parent, filter_party):
    return Sunburst(parent, filter_party)

@app.callback(
    Output('sankey-graph', 'figure'),
    Output('dropdown-discipline', 'style'),
    Input('dropdown-discipline', 'value'),
    Input("tabs", "active_tab"))
def update_chart(party, active_tab):
    '''Callback function to update 

    Args:
        party ([str]): selected party from a dropdown menu

    Returns:
        go.Figure: Plotly sankey Graph
    '''

    if active_tab is not None:
        if active_tab == "general":
            chart = get_chart(party)

            node = dict(pad=30, thickness=20,
                        line=dict(color="black", width=0.5),
                        label=chart.labels,
                        color=chart.color_node,
                        )
            link = dict(source=chart.source,
                        target=chart.target,
                        #customdata=chart.customdata,
                        
                        value=chart.value,  # NOTE: value is 3rd dimension
                        hovertemplate='Has %{value} TD items',
                        color=chart.color_link,
                        )

            data = go.Sankey(node=node, link=link)
            fig = go.Figure(data=data)
            fig.update_layout(height=650, margin=dict(l=0, r=0, t=5, b=5))

            return fig, {'display': 'block'}

        elif active_tab == "discipline":
            contagious_parties = get_chart_discipline_specific(parent="Party", filter_party="EE")

            data = go.Treemap(
                ids=contagious_parties.ids,      
                parents=contagious_parties.parents,
                labels=contagious_parties.labels,
                values=contagious_parties.values,
                #hovertemplate=contagious_parties.info
            )
                
            fig = go.Figure(data=data)
            fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=650, hovermode='x',)
            
            return fig, {'display': 'none'}
    else:
        return "No tab selected"


def main():
    popover_children = [
        dbc.PopoverHeader("Page Information"),
        dbc.PopoverBody(["""
            The graph shows how the TD issues that are initiated by a discipline (left side)
            affect the other disciplines (right side)
            It can also be shown single disciplines.
            The tab "Electronic Engineering Discipline" shows the disciplines 
            that initiate TD which affects EE.
        """]),
    ]

    layout = html.Div([
        dbc.Row(
                [
                    dbc.Col(
                        html.H2("TD Spreading / Contagiousness within disciplines")
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
        dbc.Tabs(
                [
                    dbc.Tab(label="General", tab_id="general"),
                    dbc.Tab(label="Electronic Engineering Discipline", tab_id="discipline"),
                ],
                id="tabs",
                active_tab="general",
            ),
        html.Div(id="tab-content", className="p-4"),
        dcc.Loading(
                id="loading",
                type="dot",
                children=html.Div([
                    dcc.Graph(id="sankey-graph")
                    ])
            ),
    ])


    dropdown_discipline = [
        dbc.Label("Initiating discipline"),
        dcc.Dropdown(
            id='dropdown-discipline',
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
            value='All',
            style= {'display': 'block'} #todo: do it with the whole Div (title+dropdown)
        ),
    ]

    controls = dropdown_discipline

    return layout, controls


if __name__ == '__main__':
    main()
