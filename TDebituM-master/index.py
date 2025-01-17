import dash
from dash import Dash, callback, html, dcc,  dash_table, Input, Output, State, MATCH, ALL

import dash_bootstrap_components as dbc

from dash.dash_table.Format import Group

from views import p1_td_types, p2_td_status, p3_solved_td, p4_measurements, p5_contagiousness, p6_causes_chain
from dash_app import app
from configuration import *



''' This is the homepage of the web application, 
    the main page where visitors can find hyperlinks 
    to other pages on the site.

Returns:
    [type]: [description]
'''
# TODO: do a class for each layout element
top_bar = html.Div([html.H2("TDebituM", className="display-4")], style=TITLE_STYLE)

location = dcc.Location(id="url")

#class method: add_new_navlink(display_name, href, style={}, disabled=False)
# class attribute: name
side_bar = html.Div(
    [
        html.H4("Views"),
        dbc.Nav(
            [                
                dbc.NavLink("Overview", href="/overview", style={"font-size": "24px"}, disabled=True),
                dbc.NavLink("- Types of TD", href="/", style={"font-size": "20px"}),
                dbc.NavLink("- Status of TD", href="/overview/td-status", style={"font-size": "20px"}),
                dbc.NavLink("- Solved TD", href="/overview/solved-td", style={"font-size": "20px"}),
                dbc.NavLink("- Measurements", href="/overview/measurements", style={"font-size": "20px"}),
                
                dbc.NavLink("TD Spreading ", href="/contagiousness/overview", style={"font-size": "24px"}, disabled=True),
                dbc.NavLink("- Contagiousness ", href="/contagiousness/overview", style={"font-size": "20px"}),
                dbc.NavLink("- Causes Chain", href="/causes-chain", style={"font-size": "20px"}),

                dbc.NavLink("Temporal View", href="/temporal-view", style={"font-size": "24px"}, disabled=True),
                dbc.NavLink("- Evolution TD", href="/temporal-view", style={"font-size": "20px"}, disabled=True),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


# todo: introduce the id inside the child inside: separate the title and the graph id
# todo: do the same with controls. combination of title and info, popover, loading, info panel
content = html.Div([], id="page-content", style=CONTENT_STYLE)
# page_title = 
# elements_info =


controls = html.Div(
    [
        dbc.Card(
            dbc.FormGroup(id="controls"),
            body=True,
            style=CONTROLS_STYLE
        )
    ]
)

# Define the general layout of the application
app.layout = html.Div([top_bar, location, side_bar, content, controls])

@app.callback(
    Output("page-content", "children"),
    Output("controls", "children"),
    [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return p1_td_types.main()

    elif pathname == "/overview/td-status":
        return p2_td_status.main()
    
    elif pathname == "/overview/solved-td":
        return p3_solved_td.main()

    elif pathname == "/overview/measurements":
        return p4_measurements.main()

    elif pathname == "/contagiousness/overview":
        return p5_contagiousness.main()
    
    elif pathname == "/causes-chain":
        return p6_causes_chain.main()


    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    ), []