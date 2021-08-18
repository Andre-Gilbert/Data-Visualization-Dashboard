"""Supplier Performance Numeric Point Charts."""
import dash_core_components as dcc
import dash_html_components as html


def supplier_performance_npc() -> html.Div:
    """Generate the numeric point charts for supplier performance.

    Summary

    Returns:
        The html containing the charts.
    """
    supplier_performance_npc = html.Div([
        html.Div([
            html.H1('Delivery Deviation', className='npc-title'),
            html.Div([
                dcc.Graph(id='supplier-performance-npc-current-year', className='npc-supplier-performance'),
                dcc.Graph(id='supplier-performance-npc-current-year', className='npc-supplier-performance'),
                dcc.Graph(id='supplier-performance-npc-current-year')
            ],
                     className='npc-chart-container')
        ],
                 className='npc-container-one')
    ])
    return supplier_performance_npc
