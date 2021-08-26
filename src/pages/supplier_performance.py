"""Dashboard Supplier Performance Page."""
import dash_core_components as dcc
import dash_html_components as html
from app import cache


@cache.memoize()
def supplier_performance() -> html.Div:
    """Generate the supplier performance page.

    The Supplier Performance page contains 4 charts:
        - supplier performance by month
        - supplier performance by purchasing organization
        - supplier performance by top 10 suppliers
        - supplier performance by deviation cause and indicator

    Returns:
        The html of the chart containers and the charts.
    """
    supplier_performance = html.Div([
        html.Div([
            html.Div(dcc.Graph(id='supplier-performance-by-month-chart'), className='chart-container'),
            html.Div(dcc.Graph(id='supplier-performance-by-org-chart'), className='chart-container'),
            html.Div(dcc.Graph(id='supplier-performance-top-10-suppliers-chart'), className='chart-container'),
            html.Div(dcc.Graph(id='supplier-performance-deviation-cause-and-indicator-chart'),
                     className='chart-container')
        ],
                 className='page-main')
    ],
                                    className='page')
    return supplier_performance
