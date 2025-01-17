from optparse import Values
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import scipy.stats as stats
import dash_table
from dash import Dash

import dash_bootstrap_components as dbc
import dash_core_components as dcc

from views import p1_td_types, p2_td_status, p3_solved_td, p4_measurements, p5_contagiousness, p6_causes_chain, p7_P_Values
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
                dbc.NavLink("Correlations", href="/correlations", style={"font-size": "24px"}, disabled=True),
                dbc.NavLink("- P-values", href="/correlationsP-values", style={"font-size": "20px"}),

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
    
    elif pathname == "/correlationsP-values":
        return p7_P_Values.main()
    

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    ), []
# callback function to make interactive actions between the dropdowns and the table in P-values page
@app.callback(
    [Output(component_id='update_table',component_property='children'),
     Output(component_id='update_correlation',component_property='children')],
    [Input(component_id='trigger_button',component_property='n_clicks')],
    [State(component_id='first_dropdown',component_property='value'),
    State(component_id='second_dropdown',component_property='value')]
)
def update_my_graph(n,selected_value_1, selected_value_2):
    print(f"The first dropdown is: {selected_value_1}")
    print(f"The second dropdown is: {selected_value_2}")
    print(type(selected_value_1))
    xl_file_Tabelle1 = pd.read_excel("C:\\Users\\sarya\\Downloads\\TD_datasource_71.xlsx", sheet_name= "Tabelle1")
    first_column = xl_file_Tabelle1[selected_value_1]
    second_column = xl_file_Tabelle1[selected_value_2]
    xl_file_p_value = pd.read_excel("C:\\Users\\sarya\\Downloads\\TD_datasource_71.xlsx", sheet_name= "Sheet1")
    first_list = list(dict.fromkeys(list(first_column)))
    second_list = list(dict.fromkeys(list(second_column)))
    first_list.pop()
    second_list.pop()
    xl_file_ChiSquare = pd.read_excel("C:\\Users\\sarya\\Downloads\\TD_datasource_71.xlsx", sheet_name= "Python correlations")

    # adapting Python correlations sheet to the selected columns 

    items = first_list + second_list
    xl_file_ChiSquare = pd.DataFrame(xl_file_ChiSquare, columns = items)
    #print(xl_file_ChiSquare)
    items = list(dict.fromkeys(items))
    
    # assiging the names of the columns and rows to the columns chosen by the user 

    xl_file_p_value = pd.DataFrame(xl_file_p_value, index = items)
    xl_file_p_value = pd.DataFrame(xl_file_p_value, columns = items)
    #print(xl_file_p_value)
    #print (xl_file_Tabelle1)

    # Creating a new excel sheet displaying the number of occurence of the items selected by the users in a certain TD incident 

    for item in items:
        for ind, row in xl_file_ChiSquare.iterrows():
            if item in first_list:
                occurance = sum(xl_file_Tabelle1[xl_file_Tabelle1["#NumberofTDincident"]== ind+1][selected_value_1] == item)
                xl_file_ChiSquare.loc[ind,item] = occurance
            if item in second_list:
                occurance = sum(xl_file_Tabelle1[xl_file_Tabelle1["#NumberofTDincident"]== ind+1][selected_value_2] == item)
                xl_file_ChiSquare.loc[ind,item] = occurance
    #print(xl_file_ChiSquare)

    xl_file_ChiSquare.to_excel("C:\\Users\\sarya\\Downloads\\ChiSquare.xlsx")
    xl_file_ChiSquare = pd.read_excel("C:\\Users\\sarya\\Downloads\\ChiSquare.xlsx")
    for item_1 in items:
        for item_2 in items:
            if item_1 == item_2:
                continue  
            xl_file_ChiSquare[item_1].replace([2,3,4,5,6, 7,8,9,10,11,12,13,14,15],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],inplace=True)
            xl_file_ChiSquare[item_2].replace([2,3,4,5,6, 7,8,9,10,11,12,13,14,15],[1,1,1,1,1,1,1,1,1,1,1,1,1,1],inplace=True)
            xl_file_ChiSquare_chi_Square_table = pd.crosstab(xl_file_ChiSquare[item_1], xl_file_ChiSquare[item_2])
            print(xl_file_ChiSquare_chi_Square_table)
            observed_values = xl_file_ChiSquare_chi_Square_table.values
            print("Observed Values :-\n",observed_values)
            val = stats.chi2_contingency(xl_file_ChiSquare_chi_Square_table)
            print(val)
            expected_values = val[3]
            print("Expected Values :-\n", expected_values)
            no_of_rows = len(xl_file_ChiSquare_chi_Square_table.iloc[0:2,0])
            no_of_columns = len(xl_file_ChiSquare_chi_Square_table.iloc[0,0:2])
            DOF = (no_of_columns-1)*(no_of_rows-1)
            print("Degree of freedem = ",DOF)
            alpha = 0.05

            # P-value and Chi-Square value

            from scipy.stats import chi2 
            chi_square = sum ([(o-e)**2./e for o,e in zip(observed_values,expected_values)])
            print(chi_square)
            chi_square_value = chi_square[0]+chi_square[1]
            print("Chi Square Value :- ", chi_square_value)
            p_value =round(1 - chi2.cdf(x=chi_square_value,df=DOF),3)
            print("P-value :- ", p_value)
             

       
        # checking the dependacy by comparing the P-value with Significance level (alpha)
        
            check_validation = expected_values[0][0] > 5 and expected_values[0][1] > 5 and expected_values [1][0] > 5 and expected_values[1][1] > 5

            if p_value > alpha and check_validation :
                print("Fail to reject the Null Hypothesis (H0)")
            elif p_value <= alpha and check_validation:
                print("Reject H0 and accept the alternative Hypothesis, they are dependent")
            else:
                p_value = 1
                print("test result is invalid because one or more expected value is(are) less than 5")
            xl_file_p_value.loc[item_1, item_2] = p_value # assigning the P-value to the its cell in the P-value sheet

    
    xl_file_p_value.to_excel("C:\\Users\\sarya\\Downloads\\pValue.xlsx")
    xl_file_p_value = pd.read_excel("C:\\Users\\sarya\\Downloads\\pValue.xlsx")

    # creating a new table showing the dependent items 
    
    df = xl_file_p_value[~(xl_file_p_value.iloc[1:len(xl_file_p_value),1:len(xl_file_p_value)] > 0.05)]
    colu = list(xl_file_p_value.columns)

    for row,value in df.iterrows():
        for col in df.columns:
            if df.loc[row,col] < 0.05:
                df.loc[row,col]=colu[row+1]
    df.dropna(how="all",inplace=True)
    df.dropna(how="all",axis=1, inplace=True)
    df.to_excel("C:\\Users\\sarya\\Downloads\\tra.xlsx") 
             
            
    print(df)
    #print(xl_file_p_value)
    
    return [html.Div([
            dash_table.DataTable(
                data = xl_file_p_value.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in xl_file_p_value.columns],
                page_size=20,
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'height': 'auto',
                    # all three widths are needed
                    'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                    'whiteSpace': 'normal'
                    },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(220, 220, 220)',
                        'if': {
                            'filter_query': '{{{}}} < 0.05'.format(col),
                            'column_id': col
                              },
                        'backgroundColor': '#3D9970',
                        'color': 'white'
                    } for col in xl_file_p_value
                                        ],
                style_header={
                        'backgroundColor': 'rgb(210, 210, 210)',
                        'color': 'black',
                        'fontWeight': 'bold'
                            }
                )
        
        ]
    ),
            html.Div([
            dash_table.DataTable(
                data = df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                page_size=20,
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'height': 'auto',
                    # all three widths are needed
                    'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                    'whiteSpace': 'normal'
                    },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(220, 220, 220)'
                   
                    }],
                style_header={
                        'backgroundColor': 'rgb(210, 210, 210)',
                        'color': 'black',
                        'fontWeight': 'bold'
                            }                    
                                    )
            ]
            )
            ]