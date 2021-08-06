import dash_core_components as dcc
import dash_html_components as html


def navbar(app):
    navbar = html.Div([
        html.Div([
            html.Div([
                html.Img(src=app.get_asset_url("logo.svg")),
                html.Button(
                    ['Ordered Spend',
                     html.Img(src=app.get_asset_url("arrow_down.svg"), className='arrow-down')],
                    className='nav-container')
            ],
                     className='container'),
            html.Div(html.P('SF', className='icon-text'), className='user-icon')
        ],
                 className='main-content')
    ],
                      className='navbar')
    return navbar
