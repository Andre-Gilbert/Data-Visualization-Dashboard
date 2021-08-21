"""Dashboard Ordered Spend Page."""
import dash_core_components as dcc
import dash_html_components as html


def ordered_spend() -> html.Div:
    """Generate the ordered spend page.

    Summary

    Returns:
        The html of the chart containers and the charts.
    """
    ordered_spend = html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H1('Orders by Month', className='chart-title'),
                    dcc.Graph(id='ordered-spend-by-month-chart', figure={})
                ],
                         className='chart-one'),
            ],
                     className='chart-container'),
            html.Div([
                html.Div([
                    html.H1('Orders by Purchsing Organisation', className='chart-title'),
                    dcc.Graph(id='ordered-spend-by-org-chart', figure={})
                ],
                         className='chart-one'),
            ],
                     className='chart-container'),
            html.Div([
                html.Div([
                    html.H1('Orders by Top Ten Suppliers', className='chart-title'),
                    dcc.Graph(id='ordered-spend-top-10-suppliers-chart', figure={})
                ],
                         className='chart-one'),
            ],
                     className='chart-container')
        ],
                 className='page-main')
    ],
                             className='page')
    return ordered_spend
