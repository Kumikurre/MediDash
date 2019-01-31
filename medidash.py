from datetime import datetime as dt

import flask
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

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
#app = dash.Dash(__name__, server=server, url_base_pathname='/medidash/')

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


app.config.suppress_callback_exceptions = True

