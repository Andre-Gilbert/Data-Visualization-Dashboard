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


@app.callback(Output(component_id='dropdown-menu', component_property='label'), [
    Input(component_id='ordered-spend', component_property='n_clicks'),
    Input(component_id='number-of-orders', component_property='n_clicks')
])
def update_dropdown_label(ordered_spend: int, number_of_orders: int) -> str:
    """Callback that updates the dropdown label.

    Args:
        ordered_spend: The number of button clicks.
        number_of_orders: The number of button clicks.

    Returns:
        The updated dropdown label.
    """
    id_lookup = {'ordered-spend': 'Ordered Spend', 'number-of-orders': 'Number of Orders'}
    ctx = dash.callback_context

    if not ordered_spend and not number_of_orders or not ctx.triggered:
        dropdown_label = 'Ordered Spend'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        dropdown_label = id_lookup[button_id]

    return dropdown_label


@app.callback([
    Output(component_id='page-header', component_property='children'),
    Output(component_id='numeric-point-chart', component_property='children'),
    Output(component_id='page-content', component_property='children')
], [Input(component_id='tabs', component_property='active_tab')])
def update_page(active_tab: str):
    """Callback that updates the page.

    Args:
        active_tab: The active_tab of the page.

    Returns:
        The page header, numeric point charts and the page content
    """
    if active_tab == 'tab-ordered-spend':
        page_header = 'Ordered Spend'
        page_numeric_point_chart = os_numeric_point_chart()
        page_content = ordered_spend()
        return page_header, page_numeric_point_chart, page_content

    elif active_tab == 'tab-supplier-performance':
        page_header = 'Supplier Performance'
        page_content = supplier_performance()
        page_numeric_point_chart = sp_numeric_point_chart()
        return page_header, page_numeric_point_chart, page_content


@app.callback(Output(component_id='bar-chart-os', component_property='figure'), [
    Input(component_id='tabs', component_property='active_tab'),
    Input(component_id='dropdown-menu', component_property='label'),
    Input(component_id='company-code', component_property='value'),
    Input(component_id='purchasing-org', component_property='value'),
    Input(component_id='plant', component_property='value'),
    Input(component_id='material-group', component_property='value')
])
def update_ordered_spend_charts(active_tab: str, dropdown_label: str, company_code: str, purchasing_org: str,
                                plant: str, material_group: str):
    """Callback that updates the ordered spend charts.

    Args:
        active_tab: The active_tab of the page.
        dropdown_label: The current dropdown label.
        company_code:
        purchasing_org:
        plant:
        material_group:

    Returns:
        The updated charts.
    """
    return os_bar_chart(df_bar_charts)


@app.callback(Output(component_id='bar-chart-sp', component_property='figure'), [
    Input(component_id='tabs', component_property='active_tab'),
    Input(component_id='dropdown-menu', component_property='label'),
    Input(component_id='company-code', component_property='value'),
    Input(component_id='purchasing-org', component_property='value'),
    Input(component_id='plant', component_property='value'),
    Input(component_id='material-group', component_property='value')
])
def update_supplier_performance_charts(active_tab: str, dropdown_label: str, company_code: str, purchasing_org: str,
                                       plant: str, material_group: str):
    """Callback that updates the supplier performance charts.

    Args:
        active_tab: The active_tab of the page.
        dropdown_label: The current dropdown label.
        company_code:
        purchasing_org:
        plant:
        material_group:

    Returns:
        The updated charts.
    """
    return os_bar_chart(df_bar_charts)
