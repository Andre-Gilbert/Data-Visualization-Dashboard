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
                        id='dropdown',
                        label='Ordered Spend',
                        children=[
                            dbc.DropdownMenuItem('Ordered Spend', id='OS'),
                            dbc.DropdownMenuItem('Number of Orders', id='NO')
                        ],
                    )
                ],
                         className='app-bar-container'),
                html.Div(html.P('SF', className='icon-text'), className='user-icon')
            ],
                     className='app-bar-main')
        ],
                 className='app-bar'),
        html.Div(dbc.Tabs(
            [dbc.Tab(label='Ordered Spend', id='tab-0'),
             dbc.Tab(label='Supplier Performance', id='tab-1')],
            id='tabs',
            active_tab='tab-0'),
                 className='navbar')
    ])
    return navbar
