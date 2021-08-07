import dash_core_components as dcc
import dash_html_components as html

from components.os_numeric_point_chart import os_numeric_point_chart


def header():
    header = html.Div([
        html.Div([
            html.H1('Ordered Spend', className='page-title'),
            html.Div([
                html.Div([
                    html.P('Company Code:', className='filter-bar-label'),
                    dcc.Input(id='input-company-code', type='search')
                ],
                         className='filter-bar-container'),
                html.Div([
                    html.P('Purchasing Organization:', className='filter-bar-label'),
                    dcc.Input(id='input-purchasing-org', type='search')
                ],
                         className='filter-bar-container'),
                html.Div([html.P('Plant:', className='filter-bar-label'),
                          dcc.Input(id='input-plant', type='search')],
                         className='filter-bar-container'),
                html.Div([
                    html.P('Material Group:', className='filter-bar-label'),
                    dcc.Input(id='input-material-group', type='search')
                ],
                         className='filter-bar-container')
            ],
                     className='filter-bar'),
            os_numeric_point_chart()
        ],
                 className='main-content')
    ],
                      className='header')
    return header
