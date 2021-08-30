"""Dashboard Navbar."""
import dash_bootstrap_components as dbc
import dash_html_components as html


def navbar() -> html.Div:
    """Generate the navbar for the dashboard.

    The navbar allows one to switch between 3 pages:
        - Ordered Spend
        - Supplier Performance
        - Ordered Spend IBCS

    Returns:
        The html containing the tabs.
    """
    navbar = html.Div([
        html.Div(
            html.Div(
                dbc.Tabs(
                    [
                        dbc.Tab(label='Ordered Spend', tab_id='tab-ordered-spend'),
                        dbc.Tab(label='Supplier Performance', tab_id='tab-supplier-performance'),
                        dbc.Tab(label='Ordered Spend IBCS', tab_id='tab-ordered-spend-ibcs'),
                    ],
                    id='tabs',
                    active_tab='tab-ordered-spend',
                ),
                className='navbar-container',
            ),
            className='navbar',
        )
    ])

    return navbar
