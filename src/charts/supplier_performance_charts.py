"""Supplier Performance Charts."""
import pandas as pd
import plotly.graph_objects as go
from app import cache
from plotly.subplots import make_subplots
from utils.charts import apply_number_of_orders_flag, format_numbers
from utils.data_prep import copy_and_apply_filter

from charts.config import (CHART_HEIGHT, CHART_MARGIN, DEVIATION_CAUSE_COLORS, DISPLAY, EMPTY_GRAPH, NUMBER_OF_ORDERS,
                           ORDERED_SPEND, SAP_FONT, SAP_LABEL_COLOR, SAP_TEXT_COLOR, SAP_UI_POINT_CHART_LABEL,
                           SAP_UI_POINT_CHART_NUMBER, TEMPLATE, TITLE_FONT_SIZE)


@cache.memoize()
def get_data_sp_total_deviation_and_percentage_charts(df: pd.DataFrame) -> tuple[pd.DataFrame]:
    """Create DataFrames for total deviation and percentage of deviation by purchasing organisation."""
    group_columns = ['Company Code', 'Purchasing Org.', 'Plant', 'Material Group']
    aggregate_functions = {'Purchasing Doc.': 'nunique', 'Net Value': 'sum'}
    rename_columns = {'Net Value': ORDERED_SPEND, 'Purchasing Doc.': NUMBER_OF_ORDERS}

    # DataFrame containing sum and count of all orders of 2020
    df_total_deviation_and_percentage_charts = df.loc[df['Year'] == 2020]
    df_total_deviation_and_percentage_charts = df_total_deviation_and_percentage_charts.groupby(group_columns).agg(
        aggregate_functions).reset_index().rename(columns=rename_columns)

    # DataFrame containing sum and count of orders of 2020 with deviation cause != 0
    df_reference = df.loc[(df['Deviation Cause'] != 0) & (df['Year'] == 2020)]
    df_reference = df_reference.groupby(group_columns).agg(aggregate_functions).reset_index().rename(
        columns=rename_columns)

    return df_reference, df_total_deviation_and_percentage_charts


def sp_total_deviation_and_percentage_chart(
    df_deviated: pd.DataFrame,
    df_all: pd.DataFrame,
    number_of_orders: bool,
    company_code: str,
    purchasing_org: str,
    plant: str,
    material_group: str,
) -> go.Figure:
    """Create a figure showing the total Ordered Spend or Number of Deviated Orders of the current and prior year.

    Args:
        df_deviated: First DataFrame produced by function get_data_sp_total_deviation_and_percentage_charts.
        df_all: Second DataFrame produced by function get_data_sp_total_deviation_and_percentage_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI.

    Returns:
        Two plotly indicators.
    """
    df_deviated = copy_and_apply_filter(df_deviated, company_code, purchasing_org, plant, material_group)
    df_deviated = df_deviated.agg({
        NUMBER_OF_ORDERS: 'sum',
        ORDERED_SPEND: 'sum',
    })

    df_all = copy_and_apply_filter(df_all, company_code, purchasing_org, plant, material_group)
    df_all = df_all.agg({
        NUMBER_OF_ORDERS: 'sum',
        ORDERED_SPEND: 'sum',
    })

    if number_of_orders:
        displayed = NUMBER_OF_ORDERS
        number_suffix = ''
    else:
        displayed = ORDERED_SPEND
        number_suffix = '€'

    value_deviated = df_deviated[displayed]
    value_all = df_all[displayed]

    if not value_deviated:
        value_deviated = 0
    if not value_all:
        value_all = 0

    if value_all == 0:
        percentage = None
    else:
        percentage = (value_deviated / value_all)

    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            mode='number',
            value=value_deviated,
            domain={
                'x': [0, 0.45],
                'y': [0, 1]
            },
            title='Total Deviated Orders',
            number_suffix=number_suffix,
        ))

    fig.add_trace(
        go.Indicator(
            mode='number',
            value=percentage,
            number={'valueformat': '.2%'},
            domain={
                'x': [0.55, 1],
                'y': [0, 1]
            },
            title='Deviation',
        ))

    fig.update_traces(
        number_font_size=36,
        title_font_size=14,
        delta_font_size=14,
        number_font_family=SAP_FONT,
        title_font_family=SAP_FONT,
        number_font_color=SAP_UI_POINT_CHART_NUMBER,
        title_font_color=SAP_UI_POINT_CHART_LABEL,
        align='left',
        title_align='left',
    )

    fig.update_layout(
        height=93,
        margin={
            't': 62,
            'b': 0,
            'l': 10,
            'r': 10
        },
    )

    return fig


@cache.memoize()
def get_data_sp_deviation_cause_and_indicator_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Create DataFrame for deviation cause and indicator charts."""
    df_bar_charts = df.loc[(df['Deviation Cause'] != 0) & (df['Year'] == 2020)]
    df_bar_charts = df_bar_charts.groupby([
        'Deviation Cause Text',
        'Deviation Indicator',
        'Company Code',
        'Purchasing Org.',
        'Plant',
        'Material Group',
    ]).agg({
        'Purchasing Doc.': 'nunique',
        'Net Value': 'sum',
    }).reset_index().rename(columns={
        'Net Value': ORDERED_SPEND,
        'Purchasing Doc.': NUMBER_OF_ORDERS,
    })

    return df_bar_charts


def sp_deviation_cause_and_indicator_chart(
    df: pd.DataFrame,
    number_of_orders: bool,
    company_code: str,
    purchasing_org: str,
    plant: str,
    material_group: str,
) -> go.Figure:
    """Create a figure showing Ordered Spend or Number of Deviated Orders by Deviation Cause & Deviation Indicator.

    Args:
        df: DataFrame produced by function get_data_sp_deviation_cause_and_indicator_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI.

    Returns:
        Two plotly bar chart subplots.
    """
    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)

    df_dev_cause = df.groupby([
        'Deviation Cause Text',
    ]).agg({
        NUMBER_OF_ORDERS: 'sum',
        ORDERED_SPEND: 'sum',
    }).reset_index()

    df_dev_indicator = df.groupby([
        'Deviation Indicator',
    ]).agg({
        NUMBER_OF_ORDERS: 'sum',
        ORDERED_SPEND: 'sum',
    }).reset_index()

    if df_dev_cause.empty and df_dev_indicator.empty:
        return EMPTY_GRAPH

    displayed, subtitle = apply_number_of_orders_flag(number_of_orders)

    df_dev_cause['Color'] = df_dev_cause['Deviation Cause Text'].map(DEVIATION_CAUSE_COLORS)

    title = ('Deviated Orders by Deviation Cause and Indicator<br>'
             f'<sup style="color: {SAP_LABEL_COLOR}">{subtitle}</sup>')

    df_dev_cause[DISPLAY] = df_dev_cause.apply(lambda row: format_numbers(row, displayed), axis=1)
    df_dev_indicator[DISPLAY] = df_dev_indicator.apply(lambda row: format_numbers(row, displayed), axis=1)

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=('Deviation Cause', 'Deviation Indicator'),
    )

    fig.add_trace(
        go.Bar(
            x=df_dev_cause[displayed],
            y=df_dev_cause['Deviation Cause Text'],
            marker_color=df_dev_cause['Color'],
            name='Deviation Cause',
            orientation='h',
            text=df_dev_cause[DISPLAY],
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(
            x=df_dev_indicator[displayed],
            y=df_dev_indicator['Deviation Indicator'],
            marker_color=SAP_UI_POINT_CHART_NUMBER,
            name='Deviation Indicator',
            orientation='h',
            text=df_dev_indicator[DISPLAY],
        ),
        row=1,
        col=2,
    )

    fig.update_layout(
        height=CHART_HEIGHT,
        barmode='group',
        showlegend=False,
        title=title,
        title_font_size=TITLE_FONT_SIZE,
        font_color=SAP_TEXT_COLOR,
        font_family=SAP_FONT,
        template=TEMPLATE,
        margin=CHART_MARGIN,
    )

    fig.update_yaxes(categoryorder='total ascending')
    return fig


@cache.memoize()
def get_data_sp_by_month_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Create DataFrame for supplier performance by month chart."""
    df_line_charts = df.loc[(df['Deviation Cause'] != 0) & (df['Year'] == 2020)]
    df_line_charts = df_line_charts.groupby([
        'Month',
        'Company Code',
        'Purchasing Org.',
        'Plant',
        'Material Group',
        'Deviation Cause Text',
    ]).agg({
        'Purchasing Doc.': 'nunique',
        'Net Value': 'sum',
    }).reset_index().rename(columns={
        'Net Value': ORDERED_SPEND,
        'Purchasing Doc.': NUMBER_OF_ORDERS,
    })

    return df_line_charts


def sp_by_month_chart(
    df: pd.DataFrame,
    number_of_orders: bool,
    company_code: str,
    purchasing_org: str,
    plant: str,
    material_group: str,
) -> go.Figure:
    """Create a chart showing Ordered Spend or Number of Deviated Orders by month.

    Args:
        df: DataFrame produced by function get_data_sp_by_month_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI.

    Returns:
        A plotly line chart.
    """
    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby([
        'Month',
        'Deviation Cause Text',
    ]).agg({
        NUMBER_OF_ORDERS: 'sum',
        ORDERED_SPEND: 'sum',
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
        return EMPTY_GRAPH

    displayed, subtitle = apply_number_of_orders_flag(number_of_orders)

    title = f'Deviated Orders by Month<br><sup style="color: {SAP_LABEL_COLOR}">{subtitle}</sup>'

    fig = go.Figure()

    deviation_causes = df['Deviation Cause Text'].unique()

    for deviation_cause in deviation_causes:
        trace_df = df.loc[df['Deviation Cause Text'] == deviation_cause]

        fig.add_trace(
            go.Scatter(
                x=trace_df['Month'],
                y=trace_df[displayed],
                mode='lines+markers',
                marker_color=DEVIATION_CAUSE_COLORS[deviation_cause],
                name=deviation_cause,
                stackgroup='one',
            ))

    fig.update_layout(
        height=CHART_HEIGHT,
        title=title,
        title_font_size=TITLE_FONT_SIZE,
        font_color=SAP_TEXT_COLOR,
        font_family=SAP_FONT,
        template=TEMPLATE,
        margin=CHART_MARGIN,
    )

    return fig


@cache.memoize()
def get_data_sp_by_org_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Create DataFrame for top 10 suppliers chart."""
    df_bar_charts = df.loc[(df['Deviation Cause'] != 0) & (df['Year'] == 2020)]
    df_bar_charts = df_bar_charts.groupby([
        'Company Code',
        'Purchasing Org.',
        'Plant',
        'Material Group',
        'Deviation Cause Text',
    ]).agg({
        'Purchasing Doc.': 'nunique',
        'Net Value': 'sum',
    }).reset_index().rename(columns={
        'Net Value': ORDERED_SPEND,
        'Purchasing Doc.': NUMBER_OF_ORDERS,
    })

    return df_bar_charts


def sp_by_org_chart(
    df: pd.DataFrame,
    number_of_orders: bool,
    company_code: str,
    purchasing_org: str,
    plant: str,
    material_group: str,
) -> go.Figure:
    """Create a chart showing Ordered Spend or Number of Deviated Orders by purchasing organisation.

    Args:
        df: First DataFrame produced by function get_data_sp_total_deviation_and_percentage_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: GUI Filters.

    Returns:
        A plotly bar chart.
    """
    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby([
        'Purchasing Org.',
        'Deviation Cause Text',
    ]).agg({
        NUMBER_OF_ORDERS: 'sum',
        ORDERED_SPEND: 'sum',
    }).reset_index()

    if df.empty:
        return EMPTY_GRAPH

    displayed, subtitle = apply_number_of_orders_flag(number_of_orders)

    title = (f'Deviated Orders by Purchasing Organisation'
             f'<br><sup style="color: {SAP_LABEL_COLOR}">{subtitle}</sup>')

    fig = go.Figure()

    deviation_causes = df['Deviation Cause Text'].unique()

    for deviation_cause in deviation_causes:
        trace_df = df.loc[df['Deviation Cause Text'] == deviation_cause]
        trace_df[DISPLAY] = trace_df.apply(lambda row: format_numbers(row, displayed), axis=1)

        fig.add_trace(
            go.Bar(
                x=trace_df[displayed],
                y=trace_df['Purchasing Org.'],
                marker_color=DEVIATION_CAUSE_COLORS[deviation_cause],
                name=deviation_cause,
                orientation='h',
                text=trace_df[DISPLAY],
            ))

    fig.update_layout(
        barmode='stack',
        height=CHART_HEIGHT,
        title=title,
        title_font_size=TITLE_FONT_SIZE,
        font_color=SAP_TEXT_COLOR,
        font_family=SAP_FONT,
        template=TEMPLATE,
        margin=CHART_MARGIN,
    )

    fig.update_yaxes(
        type='category',
        categoryorder='total ascending',
    )

    return fig


@cache.memoize()
def get_data_sp_top_10_suppliers_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Create DataFrame for top 10 suppliers chart."""
    df_bar_charts = df.loc[(df['Deviation Cause'] != 0) & (df['Year'] == 2020)]
    df_bar_charts = df_bar_charts.groupby([
        'Supplier Name',
        'Company Code',
        'Purchasing Org.',
        'Plant',
        'Material Group',
        'Deviation Cause Text',
    ]).agg({
        'Purchasing Doc.': 'nunique',
        'Net Value': 'sum',
    }).reset_index().rename(columns={
        'Net Value': ORDERED_SPEND,
        'Purchasing Doc.': NUMBER_OF_ORDERS,
    })

    return df_bar_charts


def sp_top_10_suppliers_chart(
    df: pd.DataFrame,
    number_of_orders: bool,
    company_code: str,
    purchasing_org: str,
    plant: str,
    material_group: str,
) -> go.Figure:
    """Create a chart showing the top 10 suppliers by ordered spend.

    Args:
        df: DataFrame produced by function get_data_sp_top_10_suppliers_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: GUI filters.

    Returns:
        A plotly bar chart.
    """
    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby([
        'Supplier Name',
        'Deviation Cause Text',
    ]).agg({
        NUMBER_OF_ORDERS: 'sum',
        ORDERED_SPEND: 'sum',
    }).reset_index()

    supplier_names = df.nlargest(10, [ORDERED_SPEND])['Supplier Name']
    df = df.loc[df['Supplier Name'].isin(supplier_names)]

    if df.empty:
        return EMPTY_GRAPH

    df.sort_values(ORDERED_SPEND, ascending=False, inplace=True)

    displayed, subtitle = apply_number_of_orders_flag(number_of_orders)

    title = f'Deviated Orders of Top Ten Suppliers<br><sup style="color: {SAP_LABEL_COLOR}">{subtitle}</sup>'

    fig = go.Figure()

    deviation_causes = df['Deviation Cause Text'].unique()

    for deviation_cause in deviation_causes:
        trace_df = df.loc[df['Deviation Cause Text'] == deviation_cause]
        trace_df[DISPLAY] = trace_df.apply(lambda row: format_numbers(row, displayed), axis=1)

        fig.add_trace(
            go.Bar(
                x=trace_df[displayed],
                y=trace_df['Supplier Name'],
                marker_color=DEVIATION_CAUSE_COLORS[deviation_cause],
                name=deviation_cause,
                orientation='h',
                text=trace_df[DISPLAY],
            ))

    fig.update_layout(
        barmode='stack',
        height=CHART_HEIGHT,
        title=title,
        title_font_size=TITLE_FONT_SIZE,
        font_color=SAP_TEXT_COLOR,
        font_family=SAP_FONT,
        template=TEMPLATE,
        margin=CHART_MARGIN,
    )

    fig.update_yaxes(categoryorder='total ascending')
    return fig
