"""Supplier Performance Numeric Point Charts."""
import dash_core_components as dcc
import dash_html_components as html
from utils.loading_indicator_config import LOADING_COLOR, LOADING_TYPE


def supplier_performance_npc() -> html.Div:
    """Generate the numeric point charts for supplier performance.

    The numeric point charts shows the total Ordered Spend
    or Number of Deviated Orders of the current and prior year.

    Returns:
        The html containing the charts.
    """
    supplier_performance_npc = html.Div(
        [
            dcc.Loading(
                dcc.Graph(
                    id='supplier-performance-total-deviation-and-percentage-chart',
                    style={'height': '9.7rem'},
                ),
                color=LOADING_COLOR,
                type=LOADING_TYPE,
            ),
        ],
        className='numeric-point-chart',
    )

    return supplier_performance_npc
