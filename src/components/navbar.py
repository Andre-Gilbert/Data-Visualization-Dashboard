import dash_core_components as dcc
import dash_html_components as html


def navbar(app):
    navbar = html.Div([
        html.Div([
            html.Div([
                html.Img(src=app.get_asset_url("logo.svg")),
                dcc.Dropdown(id='display-switch',
                             options=[{
                                 'label': 'Ordered Spend',
                                 'value': 'OS'
                             }, {
                                 'label': 'Supplier Performance',
                                 'value': 'SP'
                             }],
                             value='OS',
                             clearable=False,
                             searchable=False)
            ],
                     className='container'),
            html.Div(html.P('SF', className='icon-text'), className='user-icon')
        ],
                 className='main-content')
    ],
                      className='navbar')
    return navbar
