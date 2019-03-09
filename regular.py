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


import medidash_be as be
from medidash import app


# <a href="#" class="myButton">turquoise</a>

# @app.callback(
# 	Output('tabs-content-regular', 'children'))
def render_content():
    return html.Div([
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



def calculate_score(days=30):
    """Calculates the score from the last x days,
    the paremeter days = x"""
    start_date = pd.Timestamp(year=2018, month=12, day=9)
    #Replace start_date with dt.now() for actual data
    filter_last_days = be.df["timestamp"][be.df["timestamp"] >= start_date - pd.Timedelta(days, unit="d")]
    last_days_score = be.df["score"][filter_last_days.index]
    return int(round(last_days_score.mean(), 0))

def determine_color(score=be.df["score"].mean()):
    """Determines the color by comparing the given score to the overall avg score.
    If the score is lower than 5% of the avg score we return red, 5% higher green
    else yellow"""
    avg_score = int(round(be.df["score"].mean(), 0))
    if score < avg_score * 0.95:
        return "red"
    elif score > avg_score * 1.05:
        return "green"
    else:
        return "yellow"



layout = html.Div(children=[
	html.H1(children='MediDash'),
    html.A(html.Button('Advanced', className="nav-button"), href="/medidash/advanced"),
    html.H3('Regular view'),

    html.P("You average score from all time: {}".format(int(round(be.df["score"].mean(), 0)))),
    html.P("Your average score from the last 30 days: {}".format(calculate_score()),
        style=dict(color=determine_color(calculate_score()))),
    html.P("Your average score from the last 7 days: {}".format(calculate_score(7)),
        style=dict(color=determine_color(calculate_score(7)))),
    html.P("Your average score from the last day: {}".format(calculate_score(1)),
        style=dict(color=determine_color(calculate_score(1)))),
    html.H3("Share with your doctor"),
	html.Div(id='tabs-content-regular'),
    render_content(),
    html.Br(),
		
])

