import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import acp_be as be

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='MediDash'),
        dcc.Graph(
        id='plot1',
        figure={
            'data': [
                {'x': be.df["timestamp"], 'y': be.df["score"], 'type': 'line', 'name': 'Score'},
            ],
            'layout': {
                'title': 'Score'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)