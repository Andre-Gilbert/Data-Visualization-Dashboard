"""Ordered Spend Charts."""
import pandas as pd
import plotly.graph_objects as go
from app import cache
from utils.chart_display import format_numbers
from utils.data_prep import copy_and_apply_filter

from charts.sap_theme import (SAP_FONT, SAP_LABEL_COLOR, SAP_TEXT_COLOR, SAP_UI_POINT_CHART_LABEL,
                              SAP_UI_POINT_CHART_NUMBER, sapUiChartPaletteSequentialHue1Dark2,
                              sapUiChartPaletteSequentialNeutral)

display_column = 'Display'
template = 'plotly_white'
empty_graph = {
    'layout': {
        'xaxis': {
            'visible': False
        },
        'yaxis': {
            'visible': False
        },
        'annotations': [{
            'text': 'No matching data found',
            'xref': 'paper',
            'yref': 'paper',
            'showarrow': False,
            'font': {
                'size': 28,
                'color': SAP_UI_POINT_CHART_NUMBER
            }
        }]
    }
}


@cache.memoize()
def get_data_os_total_by_year_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Create DataFrame for total Ordered Spend by year charts."""
    df_point_charts = df.groupby([
        'Year',
        'Company Code',
        'Purchasing Org.',
        'Plant',
        'Material Group',
    ]).agg({
        'Document Date': 'count',
        'Net Value': 'sum',
    }).reset_index().rename(columns={
        'Net Value': 'Ordered Spend',
        'Document Date': 'Number of Orders',
    })

    return df_point_charts


def os_total_by_year_chart(
    df: pd.DataFrame,
    number_of_orders: bool,
    company_code: str,
    purchasing_org: str,
    plant: str,
    material_group: str,
) -> go.Figure:
    """Creates a figure showing Ordered Spend or Number of Orders of the current and prior year.

    Args:
        df: DataFrame produced by function get_data_os_total_by_year_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI.

    Returns:
        Two plotly indicators.
    """
    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby('Year').agg({
        'Number of Orders': 'sum',
        'Ordered Spend': 'sum',
    }).reset_index()

    df_this_year = df.loc[df['Year'] == 2020]
    df_last_year = df.loc[df['Year'] == 2019]

    if number_of_orders:
        displayed = 'Number of Orders'
    else:
        displayed = 'Ordered Spend'

    try:
        value_this_year = df_this_year[displayed].iloc[0]
    except IndexError:
        value_this_year = 0

    try:
        value_last_year = df_last_year[displayed].iloc[0]
    except IndexError:
        value_last_year = 0

    if value_last_year == 0:
        reference_value = None
    else:
        reference_value = value_last_year

    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            mode='number+delta',
            value=value_this_year,
            domain={
                'x': [0, 0.45],
                'y': [0, 1]
            },
            delta={
                'reference': reference_value,
                'relative': True
            },
            title='2020',
        ))

    fig.add_trace(
        go.Indicator(
            mode='number+delta',
            value=value_last_year,
            domain={
                'x': [0.55, 1],
                'y': [0, 1]
            },
            delta={
                'reference': value_last_year,
                'relative': True,
            },
            title='2019',
        ))

    fig.update_traces(
        number_font_color=SAP_UI_POINT_CHART_NUMBER,
        title_font_color=SAP_UI_POINT_CHART_LABEL,
        number_font_size=30,
    )

    fig.update_layout(
        height=90,
        margin={
            't': 30,
            'b': 10,
            'l': 10,
            'r': 10
        },
    )

    return fig


@cache.memoize()
def get_data_os_by_month_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Create DataFrame for the Ordered Spend by month chart."""
    df_line_charts = df.groupby([
        'Year',
        'Month',
        'Company Code',
        'Purchasing Org.',
        'Plant',
        'Material Group',
    ]).agg({
        'Document Date': 'count',
        'Net Value': 'sum',
    }).reset_index().rename(columns={
        'Net Value': 'Ordered Spend',
        'Document Date': 'Number of Orders',
    })

    return df_line_charts


def os_by_month_chart(
    df: pd.DataFrame,
    number_of_orders: bool,
    company_code: str,
    purchasing_org: str,
    plant: str,
    material_group: str,
) -> go.Figure:
    """Create a figure showing Ordered Spend or Number of Orders by month for the current and prior year.

    Args:
        df: DataFrame produced by function get_data_os_by_month_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI.

    Returns:
        Two line chart subplots.
    """
    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby([
        'Year',
        'Month',
    ]).agg({
        'Number of Orders': 'sum',
        'Ordered Spend': 'sum',
    }).reset_index()

    df.replace(
        {
            'Month': {
                1: 'Jan',
                2: 'Feb',
                3: 'Mar',
                4: 'Apr',
                5: 'May',
                6: 'Jun',
                7: 'Jul',
                8: 'Aug',
                9: 'Sep',
                10: 'Oct',
                11: 'Nov',
                12: 'Dec'
            }
        },
        inplace=True)

    if df.empty:
        return empty_graph

    if number_of_orders:
        displayed = 'Number of Orders'
        subtitle = ''
    else:
        displayed = 'Ordered Spend'
        subtitle = ' (in EUR)'

    title = f'Orders by Month<br><sup style="color: {SAP_LABEL_COLOR}">{displayed}{subtitle}</sup>'

    df_this_year = df.loc[df['Year'] == 2020]
    df_last_year = df.loc[df['Year'] == 2019]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df_this_year['Month'],
            y=df_this_year[displayed],
            mode='lines+markers',
            marker_color=sapUiChartPaletteSequentialHue1Dark2,
            name=2020,
        ))

    fig.add_trace(
        go.Scatter(
            x=df_last_year['Month'],
            y=df_last_year[displayed],
            mode='lines+markers',
            marker_color=sapUiChartPaletteSequentialNeutral,
            name=2019,
        ))

    fig.update_layout(
        height=600,
        title=title,
        title_font_size=20,
        font_color=SAP_TEXT_COLOR,
        font_family=SAP_FONT,
        template=template,
    )

    return fig


def os_by_org_chart(
    df: pd.DataFrame,
    number_of_orders: bool,
    company_code: str,
    purchasing_org: str,
    plant: str,
    material_group: str,
) -> go.Figure:
    """Create a figure showing Ordered Spend or Number of Orders by Purchasing Organisation for this & last year.

    Args:
        df: DataFrame produced by function get_data_os_total_by_year_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI.

    Returns:
        Two bar chart subplots.
    """
    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby([
        'Year',
        'Purchasing Org.',
    ]).agg({
        'Number of Orders': 'sum',
        'Ordered Spend': 'sum',
    }).reset_index()

    if df.empty:
        return empty_graph

    if number_of_orders:
        displayed = 'Number of Orders'
        subtitle = ''
    else:
        displayed = 'Ordered Spend'
        subtitle = ' (in EUR)'

    df[display_column] = df.apply(lambda row: format_numbers(row, displayed), axis=1)

    title = f'Orders by Purchasing Organisation<br><sup style="color: {SAP_LABEL_COLOR}">{displayed}{subtitle}</sup>'

    sort_array = df.sort_values(['Year', displayed], ascending=True)
    sort_array = sort_array.loc[:, 'Purchasing Org.'].drop_duplicates(keep='last')

    df_this_year = df.loc[df['Year'] == 2020]
    df_last_year = df.loc[df['Year'] == 2019]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df_last_year[displayed],
            y=df_last_year['Purchasing Org.'],
            marker_color=sapUiChartPaletteSequentialNeutral,
            name=2019,
            orientation='h',
            text=df_last_year[display_column],
            textposition='outside',
        ))

    fig.add_trace(
        go.Bar(
            x=df_this_year[displayed],
            y=df_this_year['Purchasing Org.'],
            marker_color=sapUiChartPaletteSequentialHue1Dark2,
            name=2020,
            orientation='h',
            text=df_this_year[display_column],
            textposition='outside',
        ))

    fig.update_layout(
        height=600,
        barmode='group',
        title=title,
        title_font_size=20,
        font_color=SAP_TEXT_COLOR,
        font_family=SAP_FONT,
        template=template,
        legend_traceorder='reversed',
    )

    fig.update_yaxes(
        type='category',
        categoryorder='array',
        categoryarray=sort_array,
    )

    return fig


@cache.memoize()
def get_data_os_top_10_suppliers_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Create DataFrame for the Ordered Spend by top 10 suppliers chart."""
    df_bar_charts = df.groupby([
        'Year',
        'Supplier Name',
        'Company Code',
        'Purchasing Org.',
        'Plant',
        'Material Group',
    ]).agg({
        'Document Date': 'count',
        'Net Value': 'sum',
    }).reset_index().rename(columns={
        'Net Value': 'Ordered Spend',
        'Document Date': 'Number of Orders',
    })

    return df_bar_charts


def os_top_10_suppliers_chart(
    df: pd.DataFrame,
    number_of_orders: bool,
    company_code: str,
    purchasing_org: str,
    plant: str,
    material_group: str,
) -> go.Figure:
    """Create a figure showing Ordered Spend or Number of Orders by top 10 suppliers for this & last year.

    Args:
        df: DataFrame produced by function get_data_os_top_10_suppliers_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI.

    Returns:
        Two bar chart subplots.
    """
    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby([
        'Year',
        'Supplier Name',
    ]).agg({
        'Number of Orders': 'sum',
        'Ordered Spend': 'sum',
    }).reset_index()

    supplier_names = df.nlargest(10, ['Year', 'Ordered Spend'])['Supplier Name']
    df = df.loc[df['Supplier Name'].isin(supplier_names)]

    if df.empty:
        return empty_graph

    if number_of_orders:
        displayed = 'Number of Orders'
        subtitle = ''
    else:
        displayed = 'Ordered Spend'
        subtitle = ' (in EUR)'

    df[display_column] = df.apply(lambda row: format_numbers(row, displayed), axis=1)

    title = f'Orders of Top Ten Suppliers<br><sup style="color: {SAP_LABEL_COLOR}">{displayed}{subtitle}</sup>'

    sort_array = df.sort_values(['Year', displayed], ascending=True)
    sort_array = sort_array.loc[:, 'Supplier Name'].drop_duplicates(keep='last')

    df_this_year = df.loc[df['Year'] == 2020]
    df_last_year = df.loc[df['Year'] == 2019]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df_last_year[displayed],
            y=df_last_year['Supplier Name'],
            marker_color=sapUiChartPaletteSequentialNeutral,
            name=2019,
            orientation='h',
            text=df_last_year[display_column],
            textposition='outside',
        ))

    fig.add_trace(
        go.Bar(
            x=df_this_year[displayed],
            y=df_this_year['Supplier Name'],
            marker_color=SAP_UI_POINT_CHART_NUMBER,
            name=2020,
            orientation='h',
            text=df_this_year[display_column],
            textposition='outside',
        ))

    fig.update_layout(
        height=600,
        barmode='group',
        title=title,
        title_font_size=20,
        font_color=SAP_TEXT_COLOR,
        font_family=SAP_FONT,
        template=template,
        legend_traceorder='reversed',
    )

    fig.update_yaxes(
        categoryorder='array',
        categoryarray=sort_array,
    )

    return fig
