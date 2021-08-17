import dash_bootstrap_components as dbc
import dash_html_components as html
from app import app


def navbar() -> html.Div:
    navbar = html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Img(src=app.get_asset_url('logo.svg'), className='logo'),
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem('Ordered Spend', id='ordered-spend', n_clicks=0),
                            dbc.DropdownMenuItem('Number of Orders', id='number-of-orders', n_clicks=0)
                        ],
                        id='dropdown',
                        label='Ordered Spend',
                    )
                ],
                         className='app-bar-container'),
                html.Div(html.P('SF', className='icon-text'), className='user-icon')
            ],
                     className='app-bar-main')
        ],
                 className='app-bar'),
        html.Div(html.Div(dbc.Tabs(
            [
                dbc.Tab(label='Ordered Spend', tab_id='tab-ordered-spend'),
                dbc.Tab(label='Supplier Performance', tab_id='tab-supplier-performance')
            ],
            id='tabs',
            active_tab='tab-ordered-spend',
        ),
                          className='navbar-container'),
                 className='navbar')
    ])
    return navbar
