import dash_bootstrap_components as dbc
import dash_html_components as html
from app import app


def navbar() -> html.Div:
    navbar = html.Div([
        html.Div([
            html.Div([
                html.Img(src=app.get_asset_url('logo.svg'), className='logo'),
                dbc.DropdownMenu(
                    id='dropdown',
                    label='Ordered Spend',
                    children=[
                        dbc.DropdownMenuItem('Ordered Spend', id='OS'),
                        dbc.DropdownMenuItem('Supplier Performance', id='SP')
                    ],
                )
            ],
                     className='navigation-container'),
            html.Div(html.P('SF', className='icon-text'), className='user-icon')
        ],
                 className='navbar-main')
    ],
                      className='navbar')
    return navbar
