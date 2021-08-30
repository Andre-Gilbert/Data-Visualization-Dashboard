from typing import Any

import dash
import dash_html_components as html
import plotly.graph_objects as go
from app import app
from components.ordered_spend_npc import ordered_spend_npc
from components.supplier_performance_npc import supplier_performance_npc
from dash.dependencies import ClientsideFunction
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, ServersideOutput, Trigger
from pages.ordered_spend import ordered_spend
from pages.supplier_performance import supplier_performance

from charts.ordered_spend_charts import (get_data_os_by_month_charts, get_data_os_top_10_suppliers_charts,
                                         get_data_os_total_by_year_charts, os_by_month_chart, os_by_org_chart,
                                         os_top_10_suppliers_chart, os_total_by_year_chart)
from charts.supplier_performance_charts import (get_data_sp_by_month_charts, get_data_sp_by_org_charts,
                                                get_data_sp_deviation_cause_and_indicator_charts,
                                                get_data_sp_top_10_suppliers_charts,
                                                get_data_sp_total_deviation_and_percentage_charts, sp_by_month_chart,
                                                sp_by_org_chart, sp_deviation_cause_and_indicator_chart,
                                                sp_top_10_suppliers_chart, sp_total_deviation_and_percentage_chart)
from utils.data_prep import copy_and_apply_filter, get_data

df = get_data()

# Ordered Spend Page
df_os_total_by_year_charts = get_data_os_total_by_year_charts(df)
df_os_by_month_charts = get_data_os_by_month_charts(df)
df_os_top_10_suppliers_charts = get_data_os_top_10_suppliers_charts(df)

# Supplier Performance Page
df_sp_total_deviation_charts, df_sp_reference = get_data_sp_total_deviation_and_percentage_charts(df)
df_sp_deviation_cause_and_indicator_charts = get_data_sp_deviation_cause_and_indicator_charts(df)
df_sp_by_month_charts = get_data_sp_by_month_charts(df)
df_sp_by_org_charts = get_data_sp_by_org_charts(df)
df_sp_top_10_suppliers_charts = get_data_sp_top_10_suppliers_charts(df)

# Function can be found here: assets/sticky_header.js
app.clientside_callback(
    ClientsideFunction('clientside', 'stickyHeader'),
    Output('header', 'id'),
    Input('header', 'id'),
)


@app.callback(
    ServersideOutput('store', 'data'),
    [
        Input('company-code', 'value'),
        Input('purchasing-org', 'value'),
        Input('plant', 'value'),
        Input('material-group', 'value'),
    ],
    memoize=True,
)
def update_store(
    company_code: int,
    purchasing_org: int,
    plant: int,
    material_group: str,
) -> dict[str, Any]:
    """Update filters based on user input.

    Args:
        company_code, purchasing_org, plant, material_group: GUI filters.

    Returns:
        A dictionary containing the filters.
    """
    return {
        'company_code': company_code,
        'purchasing_org': purchasing_org,
        'plant': plant,
        'material_group': material_group,
    }


@app.callback(
    Output('dropdown-menu', 'label'),
    [
        Trigger('ordered-spend-amount', 'n_clicks'),
        Trigger('number-of-orders', 'n_clicks'),
    ],
)
def update_dropdown_label() -> str:
    """Callback that updates the dropdown label.

    Returns:
        The updated dropdown label.
    """
    id_lookup = {'ordered-spend-amount': 'Ordered Spend Amount', 'number-of-orders': 'Number of Orders'}
    ctx = dash.callback_context

    if not ctx.triggered:
        dropdown_label = 'Ordered Spend Amount'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        dropdown_label = id_lookup[button_id]

    return dropdown_label


@app.callback(
    [
        Output('page-header', 'children'),
        Output('numeric-point-chart', 'children'),
        Output('page-content', 'children'),
    ],
    Input('tabs', 'active_tab'),
)
def update_page(active_tab: str) -> tuple[str, html.Div, html.Div]:
    """Callback that updates the page.

    Args:
        active_tab: The active tab of the page.

    Returns:
        The page header, numeric point charts and the page content.
    """
    if active_tab == 'tab-ordered-spend' or active_tab == 'tab-ordered-spend-ibcs':
        page_header = 'Ordered Spend'
        page_numeric_point_chart = ordered_spend_npc()
        page_content = ordered_spend()

    elif active_tab == 'tab-supplier-performance':
        page_header = 'Supplier Performance'
        page_numeric_point_chart = supplier_performance_npc()
        page_content = supplier_performance()

    return page_header, page_numeric_point_chart, page_content


@app.callback(
    [
        Output('company-code', 'options'),
        Output('purchasing-org', 'options'),
        Output('plant', 'options'),
        Output('material-group', 'options'),
    ],
    Input('store', 'data'),
)
def update_filters(store: dict[str, Any]) -> tuple[list[dict[str, Any]]]:
    """Update filters based on user input.

    Args:
        store GUI filters.

    Returns:
        A tuple containing lists of dictionaries with the new labels and values of the filters.
    """
    filtered_df = copy_and_apply_filter(
        df=df,
        company_code=store['company_code'],
        purchasing_org=store['purchasing_org'],
        plant=store['plant'],
        material_group=store['material_group'],
    )

    company_code_filter = [{
        'label': label,
        'value': label,
    } for label in sorted(filtered_df['Company Code'].unique())]

    purchasing_org_filter = [{
        'label': label,
        'value': label,
    } for label in sorted(filtered_df['Purchasing Org.'].unique())]

    plant_filter = [{
        'label': label,
        'value': label,
    } for label in sorted(filtered_df['Plant'].unique())]

    material_group_filter = [{
        'label': label,
        'value': label,
    } for label in sorted(filtered_df['Material Group'].unique().astype(str))]

    return (
        company_code_filter,
        purchasing_org_filter,
        plant_filter,
        material_group_filter,
    )


@app.callback(
    [
        Output('ordered-spend-total-by-year-chart', 'figure'),
        Output('ordered-spend-by-month-chart', 'figure'),
        Output('ordered-spend-by-org-chart', 'figure'),
        Output('ordered-spend-top-10-suppliers-chart', 'figure'),
    ],
    [
        Input('tabs', 'active_tab'),
        Input('dropdown-menu', 'label'),
        Input('store', 'data'),
    ],
)
def update_ordered_spend_charts(
    active_tab: str,
    dropdown_label: str,
    store: dict[str, Any],
) -> tuple[go.Figure]:
    """Callback that updates the ordered spend charts.

    Args:
        active_tab: The active tab of the page.
        dropdown_label: The current dropdown label.
        store: GUI filters.

    Returns:
        The updated charts.
    """
    if active_tab != 'tab-ordered-spend' and active_tab != 'tab-ordered-spend-ibcs':
        raise PreventUpdate

    company_code = store['company_code']
    purchasing_org = store['purchasing_org']
    plant = store['plant']
    material_group = store['material_group']

    if active_tab == 'tab-ordered-spend':
        if dropdown_label == 'Ordered Spend Amount':
            number_of_orders_para = False
        elif dropdown_label == 'Number of Orders':
            number_of_orders_para = True

        total_by_year_chart = os_total_by_year_chart(
            df=df_os_total_by_year_charts,
            number_of_orders=number_of_orders_para,
            ibcs=False,
            company_code=company_code,
            purchasing_org=purchasing_org,
            plant=plant,
            material_group=material_group,
        )

        by_month_chart = os_by_month_chart(
            df=df_os_by_month_charts,
            number_of_orders=number_of_orders_para,
            ibcs=False,
            company_code=company_code,
            purchasing_org=purchasing_org,
            plant=plant,
            material_group=material_group,
        )

        by_org_chart = os_by_org_chart(
            df=df_os_total_by_year_charts,
            number_of_orders=number_of_orders_para,
            ibcs=False,
            company_code=company_code,
            purchasing_org=purchasing_org,
            plant=plant,
            material_group=material_group,
        )

        top_10_suppliers_chart = os_top_10_suppliers_chart(
            df=df_os_top_10_suppliers_charts,
            number_of_orders=number_of_orders_para,
            ibcs=False,
            company_code=company_code,
            purchasing_org=purchasing_org,
            plant=plant,
            material_group=material_group,
        )

    elif active_tab == 'tab-ordered-spend-ibcs':
        if dropdown_label == 'Ordered Spend Amount':
            number_of_orders_para = False
        elif dropdown_label == 'Number of Orders':
            number_of_orders_para = True

        total_by_year_chart = os_total_by_year_chart(
            df=df_os_total_by_year_charts,
            number_of_orders=number_of_orders_para,
            ibcs=True,
            company_code=company_code,
            purchasing_org=purchasing_org,
            plant=plant,
            material_group=material_group,
        )

        by_month_chart = os_by_month_chart(
            df=df_os_by_month_charts,
            number_of_orders=number_of_orders_para,
            ibcs=True,
            company_code=company_code,
            purchasing_org=purchasing_org,
            plant=plant,
            material_group=material_group,
        )

        by_org_chart = os_by_org_chart(
            df=df_os_total_by_year_charts,
            number_of_orders=number_of_orders_para,
            ibcs=True,
            company_code=company_code,
            purchasing_org=purchasing_org,
            plant=plant,
            material_group=material_group,
        )

        top_10_suppliers_chart = os_top_10_suppliers_chart(
            df=df_os_top_10_suppliers_charts,
            number_of_orders=number_of_orders_para,
            ibcs=True,
            company_code=company_code,
            purchasing_org=purchasing_org,
            plant=plant,
            material_group=material_group,
        )

    return (
        total_by_year_chart,
        by_month_chart,
        by_org_chart,
        top_10_suppliers_chart,
    )


@app.callback(
    [
        Output('supplier-performance-total-deviation-and-percentage-chart', 'figure'),
        Output('supplier-performance-deviation-cause-and-indicator-chart', 'figure'),
        Output('supplier-performance-by-month-chart', 'figure'),
        Output('supplier-performance-by-org-chart', 'figure'),
        Output('supplier-performance-top-10-suppliers-chart', 'figure'),
    ],
    [
        Input('tabs', 'active_tab'),
        Input('dropdown-menu', 'label'),
        Input('store', 'data'),
    ],
)
def update_supplier_performance_charts(
    active_tab: str,
    dropdown_label: str,
    store: dict[str, Any],
) -> tuple[go.Figure]:
    """Callback that updates the supplier performance charts.

    Args:
        active_tab: The active_tab of the page.
        dropdown_label: The current dropdown label.
        store: GUI filters.

    Returns:
        The updated charts.
    """
    if active_tab != 'tab-supplier-performance':
        raise PreventUpdate

    company_code = store['company_code']
    purchasing_org = store['purchasing_org']
    plant = store['plant']
    material_group = store['material_group']

    if active_tab == 'tab-supplier-performance':
        if dropdown_label == 'Ordered Spend Amount':
            number_of_orders_para = False
        elif dropdown_label == "Number of Orders":
            number_of_orders_para = True

        total_deviation_and_percentage_chart = sp_total_deviation_and_percentage_chart(
            df_deviated=df_sp_total_deviation_charts,
            df_all=df_sp_reference,
            number_of_orders=number_of_orders_para,
            company_code=company_code,
            purchasing_org=purchasing_org,
            plant=plant,
            material_group=material_group,
        )

        deviation_cause_and_indicator_chart = sp_deviation_cause_and_indicator_chart(
            df=df_sp_deviation_cause_and_indicator_charts,
            number_of_orders=number_of_orders_para,
            company_code=company_code,
            purchasing_org=purchasing_org,
            plant=plant,
            material_group=material_group,
        )

        by_month_chart = sp_by_month_chart(
            df=df_sp_by_month_charts,
            number_of_orders=number_of_orders_para,
            company_code=company_code,
            purchasing_org=purchasing_org,
            plant=plant,
            material_group=material_group,
        )

        by_org_chart = sp_by_org_chart(
            df=df_sp_by_org_charts,
            number_of_orders=number_of_orders_para,
            company_code=company_code,
            purchasing_org=purchasing_org,
            plant=plant,
            material_group=material_group,
        )

        top_10_suppliers_chart = sp_top_10_suppliers_chart(
            df=df_sp_top_10_suppliers_charts,
            number_of_orders=number_of_orders_para,
            company_code=company_code,
            purchasing_org=purchasing_org,
            plant=plant,
            material_group=material_group,
        )

    return (
        total_deviation_and_percentage_chart,
        deviation_cause_and_indicator_chart,
        by_month_chart,
        by_org_chart,
        top_10_suppliers_chart,
    )
