import dash_html_components as html


def ordered_spend() -> html.Div:
    ordered_spend = html.Div([
        html.Div([
            html.Div([
                html.Div([html.H1('Title', className='chart-title'),
                          html.P('Chart One')], className='chart-one'),
                html.Div([html.H1('Title', className='chart-title'),
                          html.P('Chart Two')], className='chart-two')
            ],
                     className='chart-container'),
            html.Div([
                html.Div([html.H1('Title', className='chart-title'),
                          html.P('Chart One')], className='chart-one'),
                html.Div([html.H1('Title', className='chart-title'),
                          html.P('Chart Two')], className='chart-two')
            ],
                     className='chart-container'),
            html.Div([
                html.Div([html.H1('Title', className='chart-title'),
                          html.P('Chart One')], className='chart-one'),
                html.Div([html.H1('Title', className='chart-title'),
                          html.P('Chart Two')], className='chart-two')
            ],
                     className='chart-container')
        ],
                 className='page-main')
    ],
                             className='page')
    return ordered_spend
