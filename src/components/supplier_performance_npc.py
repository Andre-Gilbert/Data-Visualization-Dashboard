"""Supplier Performance Numeric Point Charts."""
import dash_core_components as dcc
import dash_html_components as html


def supplier_performance_npc() -> html.Div:
    """Generate the numeric point charts for supplier performance.

    The numeric point charts shows the total Ordered Spend
    or Number of Deviated Orders of the current and prior year.

    Returns:
        The html containing the charts.
    """
    supplier_performance_npc = html.Div([
        dcc.Graph(id='supplier-performance-total-deviation-and-percentage-chart', style={'width': '100%'}),
    ],
                                        className='numeric-point-chart')
    return supplier_performance_npc
