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
import plotly.figure_factory as ff

import medidash_be as be
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

def render_heatmap():
    #current_time = pd.Timestamp.now()
    current_time = pd.Timestamp(year=2018, month=12, day=4)
    start_date = pd.Timestamp(year=current_time.year, month=current_time.month, day=1)
    heatmap = np.full(6*7, 0)
    #heatmap[:start_date.dayofweek] = np.nan
    filtered_time = be.df[be.df["timestamp"] >= start_date].set_index("timestamp")
    filtered_score = filtered_time.resample("D").count()["score"].tolist()
    heatmap[start_date.dayofweek: start_date.dayofweek + len(filtered_score)] = filtered_score
    heatmap = heatmap.reshape(6, 7)[::-1]
    colorscale=[[0.0, 'rgb(255,255,255)'], ]
    days_in_month = pd.Series(start_date).dt.daysinmonth
    days = np.append(np.zeros(start_date.dayofweek), np.arange(1, days_in_month.tolist()[0] + 1))
    days = np.append(days, np.zeros(6*7 - start_date.dayofweek - days_in_month)).reshape(6, 7)[::-1]
    days = np.array([[int(day) for day in week]for week in days])
    
    display_text = list(zip(days.flatten(), heatmap.flatten()))
    display_text = ["{},\n{} meds".format(day[0], day[1]) for day in display_text]
    display_text = np.array(display_text).reshape(6, 7)

    return html.Div([
            dcc.Graph(
                figure=go.Figure(
                    data=ff.create_annotated_heatmap(
                        z=heatmap,
                        x=['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                        'Friday', "Saturday", "Sunday"],
                        annotation_text=display_text,
                        colorscale=colorscale,
                    ),
                    layout=go.Layout(
                        title="Calendar",
                        )

                )
            )
        ],
        style=dict(
            width="800px"))


layout = html.Div(children=[
    html.A(html.Button('Advanced', className="nav-button"), href="/medidash/advanced"),
	html.Div(id='tabs-content-regular'),
    render_content(),
    html.Br(),
    render_heatmap()
		
])

