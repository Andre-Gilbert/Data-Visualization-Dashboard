"""Dashboard Supplier Performance Page."""
import dash_core_components as dcc
import dash_html_components as html


def supplier_performance() -> html.Div:
    """Generate the supplier performance page.

    Summary

    Returns:
        The html of the chart containers and the charts.
    """
    supplier_performance = html.Div([
        html.Div([
            html.Div([
                html.Div([html.H1('Title', className='chart-title'),
                          dcc.Graph(id='chart-id-1', figure={})],
                         className='chart-one'),
            ],
                     className='chart-container'),
            html.Div([
                html.Div([html.H1('Title', className='chart-title'),
                          dcc.Graph(id='chart-id-2', figure={})],
                         className='chart-one'),
            ],
                     className='chart-container'),
            html.Div([
                html.Div([html.H1('Title', className='chart-title'),
                          dcc.Graph(id='chart-id-3', figure={})],
                         className='chart-one'),
            ],
                     className='chart-container'),
            html.Div([
                html.Div([html.H1('Title', className='chart-title'),
                          dcc.Graph(id='bar-chart-sp', figure={})],
                         className='chart-one'),
            ],
                     className='chart-container')
        ],
                 className='page-main')
    ],
                                    className='page')
    return supplier_performance
