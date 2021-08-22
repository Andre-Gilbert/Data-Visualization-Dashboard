import dash
import dash_html_components as html
import plotly.graph_objects as go
from app import app
from charts.ordered_spend_charts import (get_data_os_by_month_charts, get_data_os_top_10_suppliers_charts,
                                         get_data_os_total_by_year_charts, os_by_month_chart, os_by_org_chart,
                                         os_top_10_suppliers_chart, os_total_by_year_chart)
from charts.supplier_performance_charts import (get_data_sp_by_month_charts,
                                                get_data_sp_deviation_cause_and_indicator_charts,
                                                get_data_sp_top_10_suppliers_charts,
                                                get_data_sp_total_deviation_and_percentage_charts, sp_by_month_chart,
                                                sp_by_org_chart, sp_deviation_cause_and_indicator_chart,
                                                sp_top_10_suppliers_chart, sp_total_deviation_and_percentage_chart)
from components.ordered_spend_npc import ordered_spend_npc
from components.supplier_performance_npc import supplier_performance_npc
from dash.dependencies import Input, Output
from pages.ordered_spend import ordered_spend
from pages.supplier_performance import supplier_performance

from utils.data_prep import get_data

df = get_data()

df_os_total_by_year_charts = get_data_os_total_by_year_charts(df)
df_os_by_month_charts = get_data_os_by_month_charts(df)
df_os_top_10_suppliers_charts = get_data_os_top_10_suppliers_charts(df)

df_sp_total_deviation_charts, df_sp_reference = get_data_sp_total_deviation_and_percentage_charts(df)
df_sp_deviation_cause_and_indicator_charts = get_data_sp_deviation_cause_and_indicator_charts(df)
df_sp_by_month_charts = get_data_sp_by_month_charts(df)
df_sp_top_10_suppliers_charts = get_data_sp_top_10_suppliers_charts(df)


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
    if active_tab == 'tab-ordered-spend' or active_tab == "tab-ordered-spend-ibcs":
        page_header = 'Ordered Spend'
        page_numeric_point_chart = ordered_spend_npc()
        page_content = ordered_spend()

    elif active_tab == 'tab-supplier-performance':
        page_header = 'Supplier Performance'
        page_numeric_point_chart = supplier_performance_npc()
        page_content = supplier_performance()

    return page_header, page_numeric_point_chart, page_content


@app.callback([
    Output(component_id='ordered-spend-total-by-year-chart', component_property='figure'),
    Output(component_id='ordered-spend-by-month-chart', component_property='figure'),
    Output(component_id='ordered-spend-by-org-chart', component_property='figure'),
    Output(component_id='ordered-spend-top-10-suppliers-chart', component_property='figure')
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
        if dropdown_label == 'Ordered Spend Amount':
            total_by_year_chart = os_total_by_year_chart(df=df_os_total_by_year_charts,
                                                         company_code=company_code,
                                                         purchasing_org=purchasing_org,
                                                         plant=plant,
                                                         material_group=material_group)
            by_month_chart = os_by_month_chart(df=df_os_by_month_charts,
                                               company_code=company_code,
                                               purchasing_org=purchasing_org,
                                               plant=plant,
                                               material_group=material_group)
            by_org_chart = os_by_org_chart(df=df_os_total_by_year_charts,
                                           company_code=company_code,
                                           purchasing_org=purchasing_org,
                                           plant=plant,
                                           material_group=material_group)
            top_10_suppliers_chart = os_top_10_suppliers_chart(df=df_os_top_10_suppliers_charts,
                                                               company_code=company_code,
                                                               purchasing_org=purchasing_org,
                                                               plant=plant,
                                                               material_group=material_group)

        elif dropdown_label == 'Number of Orders':
            total_by_year_chart = os_total_by_year_chart(df=df_os_total_by_year_charts,
                                                         number_of_orders=True,
                                                         company_code=company_code,
                                                         purchasing_org=purchasing_org,
                                                         plant=plant,
                                                         material_group=material_group)
            by_month_chart = os_by_month_chart(df=df_os_by_month_charts,
                                               number_of_orders=True,
                                               company_code=company_code,
                                               purchasing_org=purchasing_org,
                                               plant=plant,
                                               material_group=material_group)
            by_org_chart = os_by_org_chart(df=df_os_total_by_year_charts,
                                           number_of_orders=True,
                                           company_code=company_code,
                                           purchasing_org=purchasing_org,
                                           plant=plant,
                                           material_group=material_group)
            top_10_suppliers_chart = os_top_10_suppliers_chart(df=df_os_top_10_suppliers_charts,
                                                               number_of_orders=True,
                                                               company_code=company_code,
                                                               purchasing_org=purchasing_org,
                                                               plant=plant,
                                                               material_group=material_group)
    elif active_tab == 'tab-ordered-spend-ibcs':
        if dropdown_label == 'Ordered Spend Amount':
            total_by_year_chart = os_total_by_year_chart(df=df_os_total_by_year_charts,
                                                         company_code=company_code,
                                                         purchasing_org=purchasing_org,
                                                         plant=plant,
                                                         material_group=material_group)
            by_month_chart = os_by_month_chart(df=df_os_by_month_charts,
                                               company_code=company_code,
                                               purchasing_org=purchasing_org,
                                               plant=plant,
                                               material_group=material_group)
            by_org_chart = os_by_org_chart(df=df_os_total_by_year_charts,
                                           company_code=company_code,
                                           purchasing_org=purchasing_org,
                                           plant=plant,
                                           material_group=material_group)
            top_10_suppliers_chart = os_top_10_suppliers_chart(df=df_os_top_10_suppliers_charts,
                                                               company_code=company_code,
                                                               purchasing_org=purchasing_org,
                                                               plant=plant,
                                                               material_group=material_group)

        elif dropdown_label == 'Number of Orders':
            total_by_year_chart = os_total_by_year_chart(df=df_os_total_by_year_charts,
                                                         number_of_orders=True,
                                                         company_code=company_code,
                                                         purchasing_org=purchasing_org,
                                                         plant=plant,
                                                         material_group=material_group)
            by_month_chart = os_by_month_chart(df=df_os_by_month_charts,
                                               number_of_orders=True,
                                               company_code=company_code,
                                               purchasing_org=purchasing_org,
                                               plant=plant,
                                               material_group=material_group)
            by_org_chart = os_by_org_chart(df=df_os_total_by_year_charts,
                                           number_of_orders=True,
                                           company_code=company_code,
                                           purchasing_org=purchasing_org,
                                           plant=plant,
                                           material_group=material_group)
            top_10_suppliers_chart = os_top_10_suppliers_chart(df=df_os_top_10_suppliers_charts,
                                                               number_of_orders=True,
                                                               company_code=company_code,
                                                               purchasing_org=purchasing_org,
                                                               plant=plant,
                                                               material_group=material_group)
    else:
        total_by_year_chart = None
        by_month_chart = None
        by_org_chart = None
        top_10_suppliers_chart = None

    return total_by_year_chart, by_month_chart, by_org_chart, top_10_suppliers_chart


@app.callback([
    Output(component_id='supplier-performance-total-deviation-and-percentage-chart', component_property='figure'),
    Output(component_id='supplier-performance-deviation-cause-and-indicator-chart', component_property='figure'),
    Output(component_id='supplier-performance-by-month-chart', component_property='figure'),
    Output(component_id='supplier-performance-by-org-chart', component_property='figure'),
    Output(component_id='supplier-performance-top-10-suppliers-chart', component_property='figure')
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
        if dropdown_label == 'Ordered Spend Amount':
            total_deviation_and_percentage_chart = sp_total_deviation_and_percentage_chart(
                df_deviated=df_sp_total_deviation_charts,
                df_all=df_sp_reference,
                company_code=company_code,
                purchasing_org=purchasing_org,
                plant=plant,
                material_group=material_group)
            deviation_cause_and_indicator_chart = sp_deviation_cause_and_indicator_chart(
                df=df_sp_deviation_cause_and_indicator_charts,
                company_code=company_code,
                purchasing_org=purchasing_org,
                plant=plant,
                material_group=material_group)
            by_month_chart = sp_by_month_chart(df=df_sp_by_month_charts,
                                               company_code=company_code,
                                               purchasing_org=purchasing_org,
                                               plant=plant,
                                               material_group=material_group)
            by_org_chart = sp_by_org_chart(df=df_sp_total_deviation_charts,
                                           company_code=company_code,
                                           purchasing_org=purchasing_org,
                                           plant=plant,
                                           material_group=material_group)
            top_10_suppliers_chart = sp_top_10_suppliers_chart(df=df_sp_top_10_suppliers_charts,
                                                               company_code=company_code,
                                                               purchasing_org=purchasing_org,
                                                               plant=plant,
                                                               material_group=material_group)

        elif dropdown_label == 'Number of Orders':
            total_deviation_and_percentage_chart = sp_total_deviation_and_percentage_chart(
                df_deviated=df_sp_total_deviation_charts,
                df_all=df_sp_reference,
                number_of_orders=True,
                company_code=company_code,
                purchasing_org=purchasing_org,
                plant=plant,
                material_group=material_group)
            deviation_cause_and_indicator_chart = sp_deviation_cause_and_indicator_chart(
                df=df_sp_deviation_cause_and_indicator_charts,
                number_of_orders=True,
                company_code=company_code,
                purchasing_org=purchasing_org,
                plant=plant,
                material_group=material_group)
            by_month_chart = sp_by_month_chart(df=df_sp_by_month_charts,
                                               number_of_orders=True,
                                               company_code=company_code,
                                               purchasing_org=purchasing_org,
                                               plant=plant,
                                               material_group=material_group)
            by_org_chart = sp_by_org_chart(df=df_sp_total_deviation_charts,
                                           number_of_orders=True,
                                           company_code=company_code,
                                           purchasing_org=purchasing_org,
                                           plant=plant,
                                           material_group=material_group)
            top_10_suppliers_chart = sp_top_10_suppliers_chart(df=df_sp_top_10_suppliers_charts,
                                                               number_of_orders=True,
                                                               company_code=company_code,
                                                               purchasing_org=purchasing_org,
                                                               plant=plant,
                                                               material_group=material_group)
    else:
        total_deviation_and_percentage_chart = None
        deviation_cause_and_indicator_chart = None
        by_month_chart = None
        by_org_chart = None
        top_10_suppliers_chart = None

    return total_deviation_and_percentage_chart, deviation_cause_and_indicator_chart, by_month_chart, by_org_chart, top_10_suppliers_chart  # noqa: E501
