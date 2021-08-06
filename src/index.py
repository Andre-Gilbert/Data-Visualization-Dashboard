import dash_core_components as dcc
import dash_html_components as html

from app import app
from components.navbar import navbar

app.layout = html.Div(navbar(app))

if __name__ == "__main__":
    app.run_server(debug=True)
