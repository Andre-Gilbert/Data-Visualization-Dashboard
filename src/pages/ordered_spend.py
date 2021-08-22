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
            html.Div([dcc.Graph(id='ordered-spend-by-month-chart')], className='chart-container'),
            html.Div([dcc.Graph(id='ordered-spend-by-org-chart')], className='chart-container'),
            html.Div([
                dcc.Graph(id='ordered-spend-top-10-suppliers-chart'),
            ], className='chart-container')
        ],
                 className='page-main')
    ],
                             className='page')
    return ordered_spend
