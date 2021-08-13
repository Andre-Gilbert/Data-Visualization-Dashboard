import dash_html_components as html

import utils.callbacks
from app import app
from components.header import header
from components.navbar import navbar
from utils.data_prep import get_data

df = get_data()

app.layout = html.Div([navbar(app), header(), html.Div(id='page-content')])

if __name__ == "__main__":
    app.run_server(debug=True)
