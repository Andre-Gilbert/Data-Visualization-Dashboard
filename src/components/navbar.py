import dash_core_components as dcc
import dash_html_components as html


def navbar():
    navbar = html.Div(children=[html.Div(children='Logo & Nav'), html.Div(children='User')])
    return navbar
