import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import render_template, request, send_file

from medidash import app
import regular, advanced

device_id = "'2bb0b3f1-23db-4e57-a8bb-a5cdc03d784d'"

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Link(
        rel='stylesheet',
        href='/static/style.css'
    ),
    html.Div(id='page-content')
])

@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)

@app.server.route('/')
def index():
    return render_template('login.html')

@app.server.route("/login", methods=["GET", "POST"])
def login():
    """Login form."""
    if request.method != 'POST':
        return render_template('login.html')
    else:
        print(request.method, request.values['device_id'])
        if request.form['device_id'] == device_id:
            return redirect(request.args.get("next"))
        else:
            flash('Invalid email address.', 'danger')
            return render_template('login.html')

        

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/medidash/regular':
         return regular.layout
    elif pathname == '/medidash/advanced':
         return advanced.layout
    else:
        return regular.layout

# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if request.args['device_id'] == device_id:
#         if pathname == '/medidash/regular':
#             return regular.layout
#         elif pathname == '/medidash/advanced':
#             return advanced.layout
#         else:
#             return regular.layout
#     else:
#         return render_template('login.html')

if __name__ == '__main__':
    app.run_server(debug=True)