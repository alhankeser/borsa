from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from database import Database
import time

db = Database('dev')
df = db.query("select * from rpt__backtest order by ts").fetchdf()

# Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Backtest Results', style={'textAlign':'center'}),
    dcc.Dropdown(df.ts_day.unique(), '', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.ts_day==value]
    return px.line(dff, x="ts", y="strategy_profit", color="strategy_id")

if __name__ == '__main__':
    app.run(debug=True)
