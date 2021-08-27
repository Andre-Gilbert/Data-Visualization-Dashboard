"""Ordered Spend Charts IBCS."""
import pandas as pd
import plotly.graph_objects as go
from app import cache
from utils.data_prep import copy_and_apply_filter

from charts.sap_theme import (SAP_FONT, SAP_LABEL_COLOR, SAP_TEXT_COLOR, sapUiChartPaletteQualitativeHue1,
                              sapUiChartPaletteQualitativeHue1Bright, sapUiPointChartLabel, sapUiPointChartNumber,
                              sapUiPointChartNumberBrighter)

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
                'color': sapUiPointChartNumber
            }
        }]
    }
}


@cache.memoize()
def os_total_by_year_chart_ibcs(
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
            number_font_color=sapUiPointChartNumber,
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
            number_font_color=sapUiPointChartNumberBrighter,
        ))

    fig.update_traces(
        title_font_color=sapUiPointChartLabel,
        number_font_size=30,
    )

    fig.update_layout(
        height=90,
        margin={
            't': 50,
            'b': 10,
            'l': 10,
            'r': 10
        },
    )

    return fig


def os_by_month_chart_ibcs(
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
        subtitle = ' | EUR'

    title = f'Orders by Month<br><sup style="color: {SAP_LABEL_COLOR}">{displayed}{subtitle}</sup>'

    df_this_year = df.loc[df['Year'] == 2020]
    df_last_year = df.loc[df['Year'] == 2019]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df_this_year['Month'],
            y=df_this_year[displayed],
            mode='lines+markers',
            marker_color=sapUiChartPaletteQualitativeHue1,
            name=2020,
        ))

    fig.add_trace(
        go.Scatter(
            x=df_last_year['Month'],
            y=df_last_year[displayed],
            mode='lines+markers',
            marker_color=sapUiChartPaletteQualitativeHue1Bright,
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


def os_by_org_chart_ibcs(
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
        subtitle = ' | EUR'

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
            marker_color=sapUiChartPaletteQualitativeHue1Bright,
            name=2019,
            orientation='h',
            text=df_last_year[displayed],
            textposition='outside',
            texttemplate='%{text:.2s}',
        ))

    fig.add_trace(
        go.Bar(
            x=df_this_year[displayed],
            y=df_this_year['Purchasing Org.'],
            marker_color=sapUiChartPaletteQualitativeHue1,
            name=2020,
            orientation='h',
            text=df_this_year[displayed],
            textposition='outside',
            texttemplate='%{text:.2s}',
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


def os_top_10_suppliers_chart_ibcs(
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
        subtitle = ' | EUR'

    title = f'Orders of Top Ten Suppliers<br><sup style="color: {SAP_LABEL_COLOR}">{displayed}{subtitle}</sup>'

    sort_array = df.sort_values(['Year', displayed], ascending=True)
    sort_array = sort_array.loc[:, 'Supplier Name'].drop_duplicates(keep='last')

    df_this_year = df.loc[df['Year'] == 2020]
    df_last_year = df.loc[df['Year'] == 2019]

    df_this_year.sort_values([displayed], ascending=True, inplace=True)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df_last_year[displayed],
            y=df_last_year['Supplier Name'],
            marker_color=sapUiChartPaletteQualitativeHue1Bright,
            name=2019,
            orientation='h',
            text=df_last_year[displayed],
            textposition='outside',
            texttemplate='%{text:.2s}',
        ))

    fig.add_trace(
        go.Bar(
            x=df_this_year[displayed],
            y=df_this_year['Supplier Name'],
            marker_color=sapUiChartPaletteQualitativeHue1,
            name=2020,
            orientation='h',
            text=df_this_year[displayed],
            textposition='outside',
            texttemplate='%{text:.2s}',
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
