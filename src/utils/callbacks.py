import dash
from app import app
from components.os_numeric_point_chart import os_numeric_point_chart
from components.sp_numeric_point_chart import sp_numeric_point_chart
from dash.dependencies import Input, Output
from pages.ordered_spend import ordered_spend
from pages.supplier_performance import supplier_performance


@app.callback([
    Output(component_id='dropdown', component_property='label'),
    Output(component_id='page-header', component_property='children'),
    Output(component_id='numeric-point-chart', component_property='children'),
    Output(component_id='page-content', component_property='children')
], [Input(component_id='OS', component_property='n_clicks'),
    Input(component_id='SP', component_property='n_clicks')])
def update_page(*args: str):
    id_lookup = {'OS': 'Ordered Spend', 'SP': 'Supplier Performance'}
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'OS'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'OS':
        dropdown_label = id_lookup[button_id]
        page_header = 'Ordered Spend'
        page_numeric_point_chart = os_numeric_point_chart()
        page_content = ordered_spend()
        return dropdown_label, page_header, page_numeric_point_chart, page_content
    else:
        dropdown_label = id_lookup[button_id]
        page_header = 'Supplier Performance'
        page_content = supplier_performance()
        page_numeric_point_chart = sp_numeric_point_chart()
        return dropdown_label, page_header, page_numeric_point_chart, page_content


@app.callback([
    Output(component_id='chart-id-1', component_property='children'),
    Output(component_id='chart-id-2', component_property='children'),
    Output(component_id='chart-id-3', component_property='children'),
    Output(component_id='chart-id-4', component_property='children')
], [
    Input(component_id='company-code', component_property='value'),
    Input(component_id='purchasing-org', component_property='value'),
    Input(component_id='plant', component_property='value'),
    Input(component_id='material-group', component_property='value')
])
def update_charts(company_code, purchasing_org, plant, material_group):
    chart1 = company_code
    chart2 = purchasing_org
    chart3 = plant
    chart4 = material_group
    return chart1, chart2, chart3, chart4
