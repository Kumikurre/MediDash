import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import render_template, request, send_file, redirect

from medidash import app
import regular, advanced

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Link(
        rel='stylesheet',
        href='/static/style.css'
    ),
    html.Link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css?family=Overpass|Roboto"),
    html.H1(children='MediDash'),
    html.Div(id='page-content')
    
])

@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/medidash/regular':
         return regular.layout
    elif pathname == '/medidash/advanced':
         return advanced.layout
    else:
        return regular.layout

if __name__ == '__main__':
    app.run_server(debug=True)