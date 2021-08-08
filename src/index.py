import dash_html_components as html

from app import app
from components.header import header
from components.navbar import navbar
from pages.ordered_spend import ordered_spend
# from pages.supplier_performance import supplier_performance
from utils.data_prep import get_data

df = get_data()

app.layout = html.Div([navbar(app), header(), ordered_spend(df)])

if __name__ == "__main__":
    app.run_server(debug=True)
