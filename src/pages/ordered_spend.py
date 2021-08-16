import dash_core_components as dcc
import dash_html_components as html


def ordered_spend() -> html.Div:
    ordered_spend = html.Div([
        html.Div([
            html.Div([
                html.Div([html.H1('Title', className='chart-title'),
                          dcc.Graph(id='chart-id-1')], className='chart-one'),
                html.Div([html.H1('Title', className='chart-title'),
                          dcc.Graph(id='chart-id-2')], className='chart-two')
            ],
                     className='chart-container'),
            html.Div([
                html.Div([html.H1('Title', className='chart-title'),
                          dcc.Graph(id='chart-id-3')], className='chart-one'),
                html.Div([html.H1('Title', className='chart-title'),
                          html.P('Chart Two')], className='chart-two')
            ],
                     className='chart-container'),
            html.Div([
                html.Div([html.H1('Title', className='chart-title'),
                          dcc.Graph(id='bar-chart-os')],
                         className='chart-one'),
                html.Div([html.H1('Title', className='chart-title'),
                          html.P('Chart Two')], className='chart-two')
            ],
                     className='chart-container')
        ],
                 className='page-main')
    ],
                             className='page')
    return ordered_spend
