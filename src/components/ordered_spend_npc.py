"""Ordered Spend Numeric Point Charts."""
import dash_core_components as dcc
import dash_html_components as html
from utils.loading_indicator_config import LOADING_COLOR, LOADING_TYPE


def ordered_spend_npc() -> html.Div:
    """Generate the numeric point charts for ordered spend.

    The numeric point charts shows the Ordered Spend
    or Number of Orders of the current and prior year.

    Returns:
        The html containing the charts.
    """
    ordered_spend_npc = html.Div(
        [
            dcc.Loading(
                dcc.Graph(
                    id='ordered-spend-total-by-year-chart',
                    style={'height': '9.7rem'},
                ),
                color=LOADING_COLOR,
                type=LOADING_TYPE,
            ),
        ],
        className='numeric-point-chart',
    )

    return ordered_spend_npc
