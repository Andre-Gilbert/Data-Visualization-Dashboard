"""Dashboard App Bar."""
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import app


def app_bar() -> html.Div:
    """Generate the app bar for the dashboard.

    The app bar allows one to switch between 2 views:
        - Ordered Spend Amount
        - Number of Orders

    Returns:
        The html containing the logo and the dropdown menu.
    """
    app_bar = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.A(
                                html.Img(src=app.get_asset_url('logo.svg'), className='logo'),
                                href='/',
                            ),
                            dbc.DropdownMenu(
                                children=[
                                    dbc.DropdownMenuItem(
                                        'Ordered Spend Amount',
                                        id='ordered-spend-amount',
                                        n_clicks=0,
                                    ),
                                    dbc.DropdownMenuItem(
                                        'Number of Orders',
                                        id='number-of-orders',
                                        n_clicks=0,
                                    )
                                ],
                                id='dropdown-menu',
                                label='Ordered Spend',
                            )
                        ],
                        className='app-bar-container',
                    ),
                    html.Div(
                        html.P('SF', className='icon-text'),
                        className='user-icon',
                    )
                ],
                className='app-bar-main',
            )
        ],
        className='app-bar',
    )

    return app_bar
