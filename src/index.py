"""App.

This component is the skeleton around the actual pages, and should only
contain code that should be seen on all pages. (e.g. navigation bar).
"""
import dash_core_components as dcc
import dash_html_components as html

import utils.callbacks
from app import app
from components.app_bar import app_bar
from components.header import header
from components.navbar import navbar

app.layout = html.Div([
    app_bar(),
    navbar(),
    header(),
    html.Div(id='page-content'),
    dcc.Store(id='store'),
])

# Start application
if __name__ == '__main__':
    app.run_server(debug=True)
