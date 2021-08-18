"""Ordered Spend Numeric Point Charts."""
import dash_core_components as dcc
import dash_html_components as html


def ordered_spend_npc() -> html.Div:
    """Generate the numeric point charts for ordered spend.

    Summary

    Returns:
        The html containing the charts.
    """
    ordered_spend_npc = html.Div([
        html.Div([
            html.H1('2020', className='npc-title'),
            html.Div([
                dcc.Graph(id='ordered-spend-npc-current-year', className='npc-chart-current-year'),
            ],
                     className='npc-chart-container')
        ],
                 className='npc-container-current-year'),
        html.Div([
            html.H1('2019', className='npc-title'),
            html.Div([
                dcc.Graph(id='ordered-spend-npc-prior-year', className='npc-chart-prior-year'),
            ],
                     className='npc-chart-container')
        ],
                 className='npc-container-prior-year')
    ],
                                 className='numeric-point-chart')
    return ordered_spend_npc
