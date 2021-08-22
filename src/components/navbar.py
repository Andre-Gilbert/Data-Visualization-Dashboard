"""Dashboard Navbar."""
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import app


def navbar() -> html.Div:
    """Generate the navbar for the dashboard.

    The navbar allows one to switch between two views:
        - Ordered Spend
        - Number of Orders

    Returns:
        The html containing the logo and the dropdown menu.
    """
    navbar = html.Div([
        # blue app-bar to switch views
        html.Div([
            html.Div([
                html.Div([
                    html.A([html.Img(src=app.get_asset_url('logo.svg'), className='logo')], href='/'),
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem('Ordered Spend Amount', id='ordered-spend-amount', n_clicks=0),
                            dbc.DropdownMenuItem('Number of Orders', id='number-of-orders', n_clicks=0)
                        ],
                        # access values through this id
                        id='dropdown-menu',
                        label='Ordered Spend',
                    )
                ],
                         # className for styling
                         className='app-bar-container'),
                html.Div(html.P('SF', className='icon-text'), className='user-icon')
            ],
                     className='app-bar-main')
        ],
                 className='app-bar'),
        
        # grey nav-bar with tabs
        html.Div(html.Div(dbc.Tabs(
            [
                dbc.Tab(label='Ordered Spend', tab_id='tab-ordered-spend'),
                dbc.Tab(label='Supplier Performance', tab_id='tab-supplier-performance'),
                dbc.Tab(label='Ordered Spend IBCS', tab_id='tab-ordered-spend-ibcs'),
            ],
            id='tabs',
            # default tab
            active_tab='tab-ordered-spend',
        ),
                          className='navbar-container'),
                 className='navbar')
    ])
    return navbar
