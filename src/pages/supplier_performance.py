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
                html.Div([
                    html.H1('Deviated Orders by Deviation Cause and Indicator', className='chart-title'),
                    dcc.Graph(id='supplier-performance-deviation-cause-and-indicator-chart', figure={})
                ],
                         className='chart-one'),
            ],
                     className='chart-container'),
            html.Div([
                html.Div([
                    html.H1('Deviated Orders by Month', className='chart-title'),
                    dcc.Graph(id='supplier-performance-by-month-chart', figure={})
                ],
                         className='chart-one'),
            ],
                     className='chart-container'),
            html.Div([
                html.Div([
                    html.H1('Deviated Orders by Purchasing Organisation', className='chart-title'),
                    dcc.Graph(id='supplier-performance-by-org-chart', figure={})
                ],
                         className='chart-one'),
            ],
                     className='chart-container'),
            html.Div([
                html.Div([
                    html.H1('Deviated Orders of Top Ten Suppliers', className='chart-title'),
                    dcc.Graph(id='supplier-performance-top-10-suppliers-chart', figure={})
                ],
                         className='chart-one'),
            ],
                     className='chart-container')
        ],
                 className='page-main')
    ],
                                    className='page')
    return supplier_performance
