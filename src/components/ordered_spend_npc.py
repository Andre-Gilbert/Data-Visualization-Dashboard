"""Ordered Spend Numeric Point Charts."""
import dash_core_components as dcc
import dash_html_components as html
from app import cache


@cache.memoize()
def ordered_spend_npc() -> html.Div:
    """Generate the numeric point charts for ordered spend.

    The numeric point charts shows the Ordered Spend
    or Number of Orders of the current and prior year.

    Returns:
        The html containing the charts.
    """
    ordered_spend_npc = html.Div([
        html.H1('Total Orders', className='npc-title'),
        dcc.Graph(id='ordered-spend-total-by-year-chart', style={'width': '100%'}),
    ],
                                 className='numeric-point-chart')
    return ordered_spend_npc
