"""Dashboard Ordered Spend Page."""
import dash_core_components as dcc
import dash_html_components as html
from utils.loading_indicator_config import INDICATOR_COLOR, INDICATOR_TYPE


def ordered_spend() -> html.Div:
    """Generate the ordered spend page.

    The Ordered Spend page contains 3 charts:
        - ordered spend by month
        - ordered spend by purchasing organization
        - ordered spend by top 10 suppliers

    Returns:
        The html of the chart containers and the charts.
    """
    ordered_spend = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        dcc.Loading(
                            dcc.Graph(id='ordered-spend-by-month-chart'),
                            color=INDICATOR_COLOR,
                            type=INDICATOR_TYPE,
                        ),
                        className='chart-container',
                    ),
                    html.Div(
                        dcc.Loading(
                            dcc.Graph(id='ordered-spend-by-org-chart'),
                            color=INDICATOR_COLOR,
                            type=INDICATOR_TYPE,
                        ),
                        className='chart-container',
                    ),
                    html.Div(
                        dcc.Loading(
                            dcc.Graph(id='ordered-spend-top-10-suppliers-chart'),
                            color=INDICATOR_COLOR,
                            type=INDICATOR_TYPE,
                        ),
                        className='chart-container',
                    )
                ],
                className='page-main',
            )
        ],
        className='page',
    )

    return ordered_spend
