"""Dashboard Header."""
import dash_core_components as dcc
import dash_html_components as html


def header() -> html.Div:
    """Generate the header for the dashboard.

    The page header and the numeric point charts will be re-rendered
    when the page changes, but the filters will be applied globally.

    Returns:
        The html containing the page header, filter bar and the numeric point charts.
    """
    header = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(id='page-header', className='page-title'),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.P('Company Code:', className='filter-bar-label'),
                                            dcc.Dropdown(id='company-code'),
                                        ],
                                        className='filter-bar-container',
                                    ),
                                    html.Div(
                                        [
                                            html.P('Purchasing Org.:', className='filter-bar-label'),
                                            dcc.Dropdown(id='purchasing-org'),
                                        ],
                                        className='filter-bar-container',
                                    ),
                                    html.Div(
                                        [
                                            html.P('Plant:', className='filter-bar-label'),
                                            dcc.Dropdown(id='plant'),
                                        ],
                                        className='filter-bar-container',
                                    ),
                                    html.Div(
                                        [
                                            html.P('Material Group:', className='filter-bar-label'),
                                            dcc.Dropdown(id='material-group'),
                                        ],
                                        className='filter-bar-container',
                                    )
                                ],
                                className='filter-bar',
                            )
                        ],
                        className='header-flex-container',
                    ),
                    html.Div(id='numeric-point-chart')
                ],
                className='header-main',
            )
        ],
        id='header',
    )

    return header
