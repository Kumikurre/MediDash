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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='MediDash',
        style={
            'marginRight':'0',
            'float':'left',
            'fontSize':'2em'}),
        html.H1(children='Patients',
            style={
                'textAlign':'right',
                'marginTop':'0',
                'marginLeft':'0',
                'fontSize':'2em'}),
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
        ),
        html.Div(
            html.Button(children='Give access',
                style={
                    'margin':'auto',
                    'display':'block',
                    'padding':'5px 20px',
                    'width':'33%',
                    'height':'100px',
                    'fontSize':'3vw'}),
            style={
                'textAlign':'center',
                'wordWrap':'breakWord'
            }),
])

if __name__ == '__main__':
    app.run_server(debug=True)