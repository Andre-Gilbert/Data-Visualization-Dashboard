import dash_html_components as html


def supplier_performance():
    supplier_performance = html.Div([
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
                     className='chart-container'),
            html.Div([
                html.Div([html.H1('Title', className='chart-title'),
                          html.P('Chart One')], className='chart-one'),
                html.Div([html.H1('Title', className='chart-title'),
                          html.P('Chart Two')], className='chart-two')
            ],
                     className='chart-container')
        ],
                 className='main-content')
    ],
                                    className='page')
    return supplier_performance
