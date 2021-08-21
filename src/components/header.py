"""Dashboard Header."""
import dash_core_components as dcc
import dash_html_components as html
from utils.data_prep import get_data

df = get_data()


def header() -> html.Div:
    """Generate the header for the dashboard.
    
    It provides filters to calculate values.
    The page header and the numeric point charts will be re-rendered
    when the page changes, but the filters will be applied globally.

    Returns:
        The html containing the page header, filter bar and the numeric point charts.
    """
    header = html.Div([
        html.Div([
            html.H1(id='page-header', className='page-title'),
            html.Div([
                html.Div([
                    html.P('Company Code:', className='filter-bar-label'),
                    dcc.Dropdown(
                        # access values through this id
                        id='company-code',
                        options=[{
                            'label': label,
                            'value': label
                        } for label in sorted(df['Company Code'].unique())],
                    )
                ],
                         # className for styling
                         className='filter-bar-container'),
                html.Div([
                    html.P('Purchasing Organization:', className='filter-bar-label'),
                    dcc.Dropdown(
                        id='purchasing-org',
                        options=[{
                            'label': label,
                            'value': label
                        } for label in sorted(df['Purchasing Org.'].unique())],
                    )
                ],
                         className='filter-bar-container'),
                html.Div([
                    html.P('Plant:', className='filter-bar-label'),
                    dcc.Dropdown(
                        id='plant',
                        options=[{
                            'label': label,
                            'value': label
                        } for label in sorted(df['Plant'].unique())],
                    )
                ],
                         className='filter-bar-container'),
                html.Div([
                    html.P('Material Group:', className='filter-bar-label'),
                    dcc.Dropdown(
                        id='material-group',
                        options=[{
                            'label': label,
                            'value': label
                        } for label in sorted(df['Material Group'].unique().astype(str))],
                    )
                ],
                         className='filter-bar-container')
            ],
                     className='filter-bar'),
            html.Div(id='numeric-point-chart')
        ],
                 className='header-main')
    ],
                      className='header')
    return header
