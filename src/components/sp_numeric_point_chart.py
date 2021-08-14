import dash_html_components as html


def sp_numeric_point_chart() -> html.Div:
    sp_numeric_point_chart = html.Div([
        html.Div([
            html.H1('Delivery Deviation', className='npc-title'),
            html.Div([
                html.P('Chart One', className='npc-supplier-performance'),
                html.P('Chart Two', className='npc-supplier-performance'),
                html.P('Chart Three')
            ],
                     className='npc-chart-container')
        ],
                 className='npc-container-one')
    ])
    return sp_numeric_point_chart
