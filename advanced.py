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
import dash_table

import medidash_be as be
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
		html.H4("Groupby"),
		dcc.Dropdown(
			id="dropdown",
			options=[
			{"label": "None", "value": None},
			{"label": "Day", "value": "D"},
			{"label": "Week", "value": "W"}
			],
			value="D",
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
	html.H3('Advanced view'),
	html.Div(id='tabs-content-advanced'),
	html.Div(id="table"),
		
])


@app.callback(
	Output('tabs-content-advanced', 'children'),
	[Input("my-slider", "value"), Input("date-picker", "start_date"),
	Input("date-picker", "end_date"), Input("dropdown", "value")])
def render_content(slider_value, start_date, end_date, dropdown_value):
	if start_date is not None:
		start_date_stmp = pd.Timestamp(start_date)
	else:
		start_date_stmp = min(be.df["timestamp"])

	end_date_stmp = pd.Timestamp(end_date)

	filtered_time = be.df["timestamp"][be.df["timestamp"] >= start_date_stmp]
	filtered_time = filtered_time[filtered_time <= end_date_stmp]
	filtered_time_cp = filtered_time
	filtered_count = np.ones(filtered_time.shape[0])

	if slider_value != 1:
		filtered_score = be.df["score"][filtered_time.index].rolling(slider_value, center=True).mean()
	else:
		filtered_score = be.df["score"][filtered_time.index]
		if dropdown_value is not None:
			filtered_score = pd.Series(filtered_score.tolist(), index=filtered_time).resample(dropdown_value).mean()
			filtered_time = filtered_score.index

			filtered_count = pd.Series(np.zeros(be.df["timestamp_medication"].shape[0]),
				index=be.df["timestamp_medication"]).resample("D").count()

	#Calculate OLS
	df = be.df["score"][filtered_time_cp.index]
	X = np.array([np.ones(len(df)), df.index.tolist()]).T
	y = df.tolist()
	Q, R = np.linalg.qr(X)
	beta = np.linalg.inv(R).dot(Q.T).dot(y)
	print(beta)

	return html.Div([
		dcc.Graph(
			figure=go.Figure(
				data=[
					go.Bar(
						x=filtered_time,
						y=filtered_count,
						yaxis="y2",
						name="Medication count"
					),
					go.Scatter(
						x=filtered_time,
						y=filtered_score,
						mode="lines",
						name="Score"
					),
					go.Scatter(
						x=filtered_time,
						y=[beta[0] + i * beta[1] for i in np.arange(len(df))],
						#xaxis="x2",
						mode="lines",
						name="Trend"
					),

				],
				layout=go.Layout(
					title="Score and medication count",
					yaxis=dict(
						range=[be.df["score"].min(), be.df["score"].max()],
						overlaying="y2",
						title="Score",
					),
					yaxis2=dict(
						side="right",
						title="Medication count",
						#overlaying="free"

					),
					xaxis=dict(
						title="Time",
					),
					
				)
			)
		)
	])


@app.callback(
	Output('table', 'children'),
	[Input("date-picker", "start_date"), Input("date-picker", "end_date")])
def render_content2(start_date, end_date):
	if start_date is not None:
		start_date_stmp = pd.Timestamp(start_date)
	else:
		start_date_stmp = min(be.df["timestamp"])

	end_date_stmp = pd.Timestamp(end_date)

	filtered_time = be.df["timestamp"][be.df["timestamp"] >= start_date_stmp]
	filtered_time = filtered_time[filtered_time <= end_date_stmp]

	#Create data table
	df = pd.DataFrame({" ": ["Mean", "Count", "Standard deviation", "10th percentile", "90th percentile"]})
	#All time
	s1 = pd.Series(be.df["score"].agg([np.mean, "count", np.std]).tolist(), name="All time")
	s1 = s1.append(pd.Series([np.percentile(be.df["score"], 10), np.percentile(be.df["score"], 90)]), ignore_index=True)
	df = pd.concat([df, s1], axis=1)
	df = df.rename(columns={0: "All time"})
	#Selected values
	filtered_score = be.df["score"][filtered_time.index]
	s2 = pd.Series(filtered_score.agg([np.mean, "count", np.std]).tolist(), name="Selected values")
	s2 = s2.append(pd.Series([np.percentile(filtered_score, 10), np.percentile(filtered_score, 90)]), ignore_index=True)
	df = pd.concat([df, s2], axis=1)
	df = df.rename(columns={0: "Selected values"})
	#Last 30days
	filter_last_month = be.df["timestamp"][be.df["timestamp"] >= pd.Timestamp(dt.now()) - pd.Timedelta(30, unit="d") ]
	if len(filter_last_month) != 0:
		last_month = be.df["score"][filter_last_month.index]
		s2 = pd.Series(last_month.agg([np.mean, "count", np.std]).tolist(), name="Last 30 days")
		s2 = s2.append(pd.Series([np.percentile(last_month, 10), np.percentile(last_month, 90)]), ignore_index=True)
		
		
	else:
		s2 = pd.Series(np.zeros(5))
	df = pd.concat([df, s2], axis=1)	
	df = df.rename(columns={0: "Last 30 days"})
	#
	#print(df)
	##

	return html.Div([
		dash_table.DataTable(
				id="table",
				columns=[{"name": i, "id": i} for i in df.columns],
    			data=df.to_dict("rows"),
    			
			)

		],style=dict(
			width=800)
		)
