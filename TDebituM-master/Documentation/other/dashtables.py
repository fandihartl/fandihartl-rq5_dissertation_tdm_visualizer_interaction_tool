import dash
import dash_table
import pandas as pd

from py2neo import Graph
from configuration import *

graph = Graph(scheme=SCHEME, host=HOST, auth=(USERNAME, PASSWORD))



query = """
        MATCH (mS:MeasureSoll)--(c:Cause)--(tds:TDSubtype)--(tdt:TDType)
        RETURN  tdt.name AS TDType, tds.name as TDSubtype, mS.name as Measure
        """
result = graph.run(query)
df = result.to_data_frame()

# print(df)
# print(type(df))
info = "Causes of TD: <br>"

# df = pd.read_csv(
#     'https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

# print(df)
data = df.to_dict('records')
# print(data)

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    # style_header={'backgroundColor': 'rgb(30, 30, 30)'},
    sort_action='native',
    style_cell={
        'whiteSpace': 'normal',
        'height': 'auto',
        'textAlign': 'left',
        # 'backgroundColor': 'rgb(50, 50, 50)',
        # 'color': 'white'
    },
    style_data_conditional=[
        {
            'if': {
                'filter_query': '{TDType} =' + f'"{td}"',
                'column_id': 'TDType'
            },
            'backgroundColor': TD_TYPES_COLORS[td],
            'color': 'black'
        }
        for td in TD_TYPES],
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=data,
)

if __name__ == '__main__':
    app.run_server(debug=True)
