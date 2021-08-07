import dash_html_components as html


def os_numeric_point_chart():
    os_numeric_point_chart = html.Div([
        html.Div([
            html.H1('2021', className='npc-title'),
            html.Div([html.P('Chart One', className='npc-chart-one'),
                      html.P('Chart Two', className='npc-chart-two')])
        ],
                 className='npc-container-one'),
        html.Div([
            html.H1('2020', className='npc-title'),
            html.Div([html.P('Chart One', className='npc-chart-one'),
                      html.P('Chart Two', className='npc-chart-two')])
        ],
                 className='npc-container-two')
    ],
                                      className='numeric-point-chart')
    return os_numeric_point_chart
