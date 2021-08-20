import dash
import dash_html_components as html
import plotly.graph_objects as go
from app import app
from charts.ordered_spend_charts import (get_data_os_bar_charts, get_data_os_line_charts,
                                         get_data_os_numeric_point_charts, get_data_os_pie_charts, os_bar_chart,
                                         os_line_chart, os_numeric_point_chart, os_pie_chart)
from charts.supplier_performance_charts import (get_data_sp_deviation_bar_charts, get_data_sp_line_charts,
                                                get_data_sp_point_and_pie_charts, get_data_sp_supplier_bar_charts,
                                                sp_deviation_bar_chart, sp_line_chart, sp_numeric_point_chart,
                                                sp_pie_chart, sp_supplier_bar_chart)
from components.ordered_spend_npc import ordered_spend_npc
from components.supplier_performance_npc import supplier_performance_npc
from dash.dependencies import Input, Output
from pages.ordered_spend import ordered_spend
from pages.supplier_performance import supplier_performance

from utils.data_prep import get_data

df = get_data()
df_os_numeric_point_charts = get_data_os_numeric_point_charts(df)
df_os_bar_charts = get_data_os_bar_charts(df)
df_os_line_charts = get_data_os_line_charts(df)
df_os_pie_charts = get_data_os_pie_charts(df)
df_sp_point_and_pie_charts, df_all = get_data_sp_point_and_pie_charts(df)
df_sp_deviation_bar_charts = get_data_sp_deviation_bar_charts(df)
df_sp_line_charts = get_data_sp_line_charts(df)
df_sp_supplier_bar_charts = get_data_sp_supplier_bar_charts(df)


@app.callback(Output(component_id='dropdown-menu', component_property='label'), [
    Input(component_id='ordered-spend-amount', component_property='n_clicks'),
    Input(component_id='number-of-orders', component_property='n_clicks')
])
def update_dropdown_label(ordered_spend_amount: int, number_of_orders: int) -> str:
    """Callback that updates the dropdown label.

    Args:
        ordered_spend_amount: The number of button clicks.
        number_of_orders: The number of button clicks.

    Returns:
        The updated dropdown label.
    """
    id_lookup = {'ordered-spend-amount': 'Ordered Spend Amount', 'number-of-orders': 'Number of Orders'}
    ctx = dash.callback_context

    if not ordered_spend and not number_of_orders or not ctx.triggered:
        dropdown_label = 'Ordered Spend Amount'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        dropdown_label = id_lookup[button_id]

    return dropdown_label


@app.callback([
    Output(component_id='page-header', component_property='children'),
    Output(component_id='numeric-point-chart', component_property='children'),
    Output(component_id='page-content', component_property='children')
], [Input(component_id='tabs', component_property='active_tab')])
def update_page(active_tab: str) -> tuple[str, html.Div, html.Div]:
    """Callback that updates the page.

    Args:
        active_tab: The active_tab of the page.

    Returns:
        The page header, numeric point charts and the page content.
    """
    if active_tab == 'tab-ordered-spend':
        page_header = 'Ordered Spend'
        page_numeric_point_chart = ordered_spend_npc()
        page_content = ordered_spend()

    elif active_tab == 'tab-supplier-performance':
        page_header = 'Supplier Performance'
        page_numeric_point_chart = supplier_performance_npc()
        page_content = supplier_performance()

    return page_header, page_numeric_point_chart, page_content


@app.callback([
    Output(component_id='ordered-spend-npc-current-year', component_property='figure'),
    Output(component_id='ordered-spend-npc-prior-year', component_property='figure'),
    Output(component_id='ordered-spend-bar-chart', component_property='figure'),
    Output(component_id='ordered-spend-line-chart', component_property='figure'),
    Output(component_id='ordered-spend-pie-chart', component_property='figure')
], [
    Input(component_id='tabs', component_property='active_tab'),
    Input(component_id='dropdown-menu', component_property='label'),
    Input(component_id='company-code', component_property='value'),
    Input(component_id='purchasing-org', component_property='value'),
    Input(component_id='plant', component_property='value'),
    Input(component_id='material-group', component_property='value')
])
def update_ordered_spend_charts(
    active_tab: str,
    dropdown_label: str,
    company_code: str,
    purchasing_org: str,
    plant: str,
    material_group: str,
) -> tuple[go.Figure]:
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
    if active_tab == 'tab-ordered-spend':
        npc_current_year = os_numeric_point_chart(df=df_os_numeric_point_charts,
                                                  company_code=company_code,
                                                  purchasing_org=purchasing_org,
                                                  plant=plant,
                                                  material_group=material_group)
        npc_prior_year = os_numeric_point_chart(df=df_os_numeric_point_charts,
                                                last_year=True,
                                                company_code=company_code,
                                                purchasing_org=purchasing_org,
                                                plant=plant,
                                                material_group=material_group)

        if dropdown_label == 'Ordered Spend Amount':
            bar_chart = os_bar_chart(df=df_os_bar_charts,
                                     company_code=company_code,
                                     purchasing_org=purchasing_org,
                                     plant=plant,
                                     material_group=material_group)
            line_chart = os_line_chart(df=df_os_line_charts,
                                       company_code=company_code,
                                       purchasing_org=purchasing_org,
                                       plant=plant,
                                       material_group=material_group)
            pie_chart = os_pie_chart(df=df_os_pie_charts,
                                     company_code=company_code,
                                     purchasing_org=purchasing_org,
                                     plant=plant,
                                     material_group=material_group)

        elif dropdown_label == 'Number of Orders':
            bar_chart = os_bar_chart(df=df_os_bar_charts,
                                     number_of_orders=True,
                                     company_code=company_code,
                                     purchasing_org=purchasing_org,
                                     plant=plant,
                                     material_group=material_group)
            line_chart = os_line_chart(df=df_os_line_charts,
                                       number_of_orders=True,
                                       company_code=company_code,
                                       purchasing_org=purchasing_org,
                                       plant=plant,
                                       material_group=material_group)
            pie_chart = os_pie_chart(df=df_os_pie_charts,
                                     number_of_orders=True,
                                     company_code=company_code,
                                     purchasing_org=purchasing_org,
                                     plant=plant,
                                     material_group=material_group)

        return npc_current_year, npc_prior_year, bar_chart, line_chart, pie_chart


@app.callback([
    Output(component_id='supplier-performance-npc-current-year', component_property='figure'),
    Output(component_id='supplier-performance-npc-prior-year', component_property='figure'),
    Output(component_id='supplier-performance-deviation-bar-chart', component_property='figure'),
    Output(component_id='supplier-performance-line-chart', component_property='figure'),
    Output(component_id='supplier-performance-pie-chart', component_property='figure'),
    Output(component_id='supplier-performance-supplier-bar-chart', component_property='figure')
], [
    Input(component_id='tabs', component_property='active_tab'),
    Input(component_id='dropdown-menu', component_property='label'),
    Input(component_id='company-code', component_property='value'),
    Input(component_id='purchasing-org', component_property='value'),
    Input(component_id='plant', component_property='value'),
    Input(component_id='material-group', component_property='value')
])
def update_supplier_performance_charts(
    active_tab: str,
    dropdown_label: str,
    company_code: str,
    purchasing_org: str,
    plant: str,
    material_group: str,
) -> tuple[go.Figure]:
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
    if active_tab == 'tab-supplier-performance':
        npc_current_year = sp_numeric_point_chart(df_deviated=df_sp_point_and_pie_charts,
                                                  df_all=df_all,
                                                  company_code=company_code,
                                                  purchasing_org=purchasing_org,
                                                  plant=plant,
                                                  material_group=material_group)
        npc_prior_year = sp_numeric_point_chart(df_deviated=df_sp_point_and_pie_charts,
                                                df_all=df_all,
                                                number_of_orders=True,
                                                company_code=company_code,
                                                purchasing_org=purchasing_org,
                                                plant=plant,
                                                material_group=material_group)

        if dropdown_label == 'Ordered Spend Amount':
            deviation_bar_chart = sp_deviation_bar_chart(df=df_sp_deviation_bar_charts,
                                                         company_code=company_code,
                                                         purchasing_org=purchasing_org,
                                                         plant=plant,
                                                         material_group=material_group)
            line_chart = sp_line_chart(df=df_sp_line_charts,
                                       company_code=company_code,
                                       purchasing_org=purchasing_org,
                                       plant=plant,
                                       material_group=material_group)
            pie_chart = sp_pie_chart(df=df_sp_point_and_pie_charts,
                                     company_code=company_code,
                                     purchasing_org=purchasing_org,
                                     plant=plant,
                                     material_group=material_group)
            supplier_bar_chart = sp_supplier_bar_chart(df=df_sp_supplier_bar_charts,
                                                       company_code=company_code,
                                                       purchasing_org=purchasing_org,
                                                       plant=plant,
                                                       material_group=material_group)

        elif dropdown_label == 'Number of Orders':
            deviation_bar_chart = sp_deviation_bar_chart(df=df_os_bar_charts,
                                                         number_of_orders=True,
                                                         company_code=company_code,
                                                         purchasing_org=purchasing_org,
                                                         plant=plant,
                                                         material_group=material_group)
            line_chart = sp_line_chart(df=df_os_line_charts,
                                       number_of_orders=True,
                                       company_code=company_code,
                                       purchasing_org=purchasing_org,
                                       plant=plant,
                                       material_group=material_group)
            pie_chart = sp_pie_chart(df=df_os_pie_charts,
                                     number_of_orders=True,
                                     company_code=company_code,
                                     purchasing_org=purchasing_org,
                                     plant=plant,
                                     material_group=material_group)
            supplier_bar_chart = sp_supplier_bar_chart(df=df_sp_supplier_bar_charts,
                                                       number_of_orders=True,
                                                       company_code=company_code,
                                                       purchasing_org=purchasing_org,
                                                       plant=plant,
                                                       material_group=material_group)

        return npc_current_year, npc_prior_year, deviation_bar_chart, line_chart, pie_chart, supplier_bar_chart
