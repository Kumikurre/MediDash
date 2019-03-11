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
import plotly.figure_factory as ff

import medidash_be as be
from medidash import app

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
    html.A(html.Button('Regular', className="nav-button"), href="/medidash/regular"),
	html.H3('Advanced view'),
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
	html.Div(id='tabs-content-advanced'),
	html.Div(id="table"),
	render_heatmap(),
		
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
						y=beta.dot(X.T),
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
