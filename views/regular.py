from datetime import datetime as dt

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import views.medidash_be as be
from medidash import app


# <a href="#" class="myButton">turquoise</a>

# @app.callback(
# 	Output('tabs-content-regular', 'children'))
def render_content():
    return html.Div([
        html.H3('Regular view'),
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


layout = html.Div(children=[
	html.H1(children='MediDash'),
    html.A(html.Button('Advanced', className="nav-button"), href="/medidash/advanced"),
	html.Div(id='tabs-content-regular'),
    render_content()
		
])