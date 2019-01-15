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

import views.medidash_be as be
from medidash import app

layout = html.Div(children=[
	html.H1(children='MediDash'),
    html.A(html.Button('Regular', className="nav-button"), href="/medidash/regular"),
	html.Div([
		html.H4("Rolling value"),
		dcc.Slider(
			id='my-slider',
			min=1,
			max=5,
			step=1,
			value=1,
			marks={i+1: '{}'.format(i+1) for i in range(5)},
		),
		html.Br(),
		html.Br(),
		dcc.DatePickerRange(
			id="date-picker",
			minimum_nights=1,
			clearable=True,
			with_portal=False,
			start_date=min(be.df["timestamp"]),
			end_date=dt.now(),
			display_format="DD.MM.YYYY"
		)], style=dict(
				width=400)),
	html.Div(id='tabs-content-advanced'),
		
])


@app.callback(
	Output('tabs-content-advanced', 'children'),
	[Input("my-slider", "value"),
	Input("date-picker", "start_date"), Input("date-picker", "end_date")])
def render_content(value, start_date, end_date):
	if start_date is not None:
		start_date_stmp = pd.Timestamp(start_date)
	else:
		start_date_stmp = min(be.df["timestamp"])

	end_date_stmp = pd.Timestamp(end_date)

	filtered_time = be.df["timestamp"][be.df["timestamp"] >= start_date_stmp]
	filtered_time = filtered_time[filtered_time <= end_date_stmp]
	filtered_score = be.df["score"][filtered_time.index].rolling(value, center=True).mean()

	return html.Div([
		html.H3('Advanced view'),
		dcc.Graph(
			figure=go.Figure(
				data=[go.Scatter(x=filtered_time,
					y= filtered_score,
					mode="lines",
					name="Score"
				)],
				layout=go.Layout(
					title="Score",
					yaxis=dict(
						range=[be.df["score"].min(), be.df["score"].max()]
					)
				)
			)
		)
	])


