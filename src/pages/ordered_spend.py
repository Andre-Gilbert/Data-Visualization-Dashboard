import dash_html_components as html


def ordered_spend():
    ordered_spend = html.Div([
        html.Div([
            html.Div('chart', className='chart-container'),
            html.Div('chart', className='chart-container'),
            html.Div('chart', className='chart-container')
        ],
                 className='main-content')
    ],
                             className='page')
    return ordered_spend
