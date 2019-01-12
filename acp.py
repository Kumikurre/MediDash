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
import acp_be as be
from datetime import datetime as dt

app = dash.Dash()


app.layout = html.Div(children=[
	html.H1(children='MediDash'),
	dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
		dcc.Tab(label='Regular view', value='tab-1-example'),
		dcc.Tab(label='Advanced view', value='tab-2-example'),
	]),
	html.Div([
		html.H4("Rolling value"),
		dcc.Slider(
			id='my-slider',
			min=1,
			max=5,
			step=1,
			value=1,
			marks={i+1: '{}'.format(i+1) for i in range(5)},
		)
	], style=dict(
				width=400)),
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
	),
	html.Div(id='tabs-content-example'),
		
])

@app.callback(
	Output('tabs-content-example', 'children'),
	[Input('tabs-example', 'value'), Input("my-slider", "value"),
	Input("date-picker", "start_date"), Input("date-picker", "end_date")])
def render_content(tab, value, start_date, end_date):
	if tab == 'tab-1-example':
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
	elif tab == 'tab-2-example':
		if start_date is not None:
			start_date_stmp = pd.Timestamp(start_date)
		else:
			start_date_stmp = min(be.df["timestamp"])

		end_date_stmp = pd.Timestamp(end_date)

		filtered_time = be.df["timestamp"][be.df["timestamp"] >= start_date_stmp]
		filtered_time = filtered_time[filtered_time <= end_date_stmp]
		filtered_score = be.df["score"][filtered_time.index]
		print(start_date_stmp)
		print(end_date_stmp)
		return html.Div([
			html.H3('Advanced view'),
			
			dcc.Graph(
				id='plot2',
				figure={
					'data': [
						{'x': filtered_time,
						'y': filtered_score.rolling(value, center=True).mean(),
						'type': 'line', 'name': 'Score'},
					],
					'layout': {
						'title': 'Score'
					}
				}
			)
		])


if __name__ == '__main__':
	app.run_server(debug=True)
