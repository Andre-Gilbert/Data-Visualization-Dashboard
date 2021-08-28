"""Dashboard Supplier Performance Page."""
import dash_core_components as dcc
import dash_html_components as html
from utils.loading_indicator_config import LOADING_COLOR, LOADING_TYPE


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
    supplier_performance = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        dcc.Loading(
                            dcc.Graph(id='supplier-performance-by-month-chart'),
                            color=LOADING_COLOR,
                            type=LOADING_TYPE,
                        ),
                        className='chart-container',
                    ),
                    html.Div(
                        dcc.Loading(
                            dcc.Graph(id='supplier-performance-by-org-chart'),
                            color=LOADING_COLOR,
                            type=LOADING_TYPE,
                        ),
                        className='chart-container',
                    ),
                    html.Div(
                        dcc.Loading(
                            dcc.Graph(id='supplier-performance-top-10-suppliers-chart'),
                            color=LOADING_COLOR,
                            type=LOADING_TYPE,
                        ),
                        className='chart-container',
                    ),
                    html.Div(
                        dcc.Loading(
                            dcc.Graph(id='supplier-performance-deviation-cause-and-indicator-chart'),
                            color=LOADING_COLOR,
                            type=LOADING_TYPE,
                        ),
                        className='chart-container',
                    )
                ],
                className='page-main',
            )
        ],
        className='page',
    )

    return supplier_performance
