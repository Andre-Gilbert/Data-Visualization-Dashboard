import dash
from app import app
from components.os_bar_charts import get_data_bar_charts, os_bar_chart
from components.os_numeric_point_chart import os_numeric_point_chart
from components.sp_numeric_point_chart import sp_numeric_point_chart
from dash.dependencies import Input, Output
from pages.ordered_spend import ordered_spend
from pages.supplier_performance import supplier_performance

from utils.data_prep import get_data

df = get_data()

df_bar_charts = get_data_bar_charts(df)


@app.callback([
    Output(component_id='page-header', component_property='children'),
    Output(component_id='numeric-point-chart', component_property='children'),
    Output(component_id='page-content', component_property='children')
], [Input(component_id='tabs', component_property='active_tab')])
def update_page(active_tab: str):
    print(active_tab)
    if active_tab == 'tab-0':
        page_header = 'Ordered Spend'
        page_numeric_point_chart = os_numeric_point_chart()
        page_content = ordered_spend()
        return page_header, page_numeric_point_chart, page_content
    elif active_tab == 'tab-1':
        page_header = 'Supplier Performance'
        page_content = supplier_performance()
        page_numeric_point_chart = sp_numeric_point_chart()
        return page_header, page_numeric_point_chart, page_content


@app.callback([
    Output(component_id='chart-id-1', component_property='children'),
    Output(component_id='chart-id-2', component_property='children'),
    Output(component_id='chart-id-3', component_property='children'),
    Output(component_id='bar-chart-os', component_property='figure')
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
    chart4 = os_bar_chart(df_bar_charts)
    return chart1, chart2, chart3, chart4
