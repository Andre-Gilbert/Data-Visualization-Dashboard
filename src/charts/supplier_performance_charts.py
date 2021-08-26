"""Supplier Performance Charts."""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_prep import copy_and_apply_filter

from charts.sap_theme import (SAP_FONT, SAP_TEXT_COLOR, sapUiChartPaletteQualitativeHue1, sapUiPointChartLabel,
                              sapUiPointChartNumber)

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

template = 'plotly_white'


def get_data_sp_total_deviation_and_percentage_charts(df: pd.DataFrame) -> tuple[pd.DataFrame]:
    """Create DataFrames for total deviation and percentage of deviation by purchasing organisation."""
    group_columns = ['Company Code', 'Purchasing Org.', 'Plant', 'Material Group']
    aggregate_functions = {'Document Date': 'count', 'Net Value': 'sum'}
    rename_columns = {'Net Value': 'Ordered Spend', 'Document Date': 'Number of Orders'}

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
        'Number of Orders': 'sum',
        'Ordered Spend': 'sum',
    })

    df_all = copy_and_apply_filter(df_all, company_code, purchasing_org, plant, material_group)
    df_all = df_all.agg({
        'Number of Orders': 'sum',
        'Ordered Spend': 'sum',
    })

    if number_of_orders:
        displayed = 'Number of Orders'
    else:
        displayed = 'Ordered Spend'

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
            title='Total of Deviated Orders',
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
            title='Percentage of all Orders',
        ))

    fig.update_traces(
        number_font_color=sapUiPointChartNumber,
        title_font_color=sapUiPointChartLabel,
    )

    fig.update_layout(
        height=200,
        margin={
            't': 50,
            'b': 10,
            'l': 10,
            'r': 10
        },
    )

    return fig


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
        'Document Date': 'count',
        'Net Value': 'sum',
    }).reset_index().rename(columns={
        'Net Value': 'Ordered Spend',
        'Document Date': 'Number of Orders',
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
        'Number of Orders': 'sum',
        'Ordered Spend': 'sum',
    }).reset_index()

    df_dev_cause.rename(columns={'Deviation Cause Text': 'Deviation Cause'}, inplace=True)

    df_dev_indicator = df.groupby([
        'Deviation Indicator',
    ]).agg({
        'Number of Orders': 'sum',
        'Ordered Spend': 'sum',
    }).reset_index()

    if df_dev_cause.empty and df_dev_indicator.empty:
        return empty_graph

    if number_of_orders:
        displayed = 'Number of Orders'
    else:
        displayed = 'Ordered Spend'

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=('Deviation Cause', 'Deviation Indicator'),
    )

    fig.add_trace(
        go.Bar(x=df_dev_cause[displayed],
               y=df_dev_cause['Deviation Cause'],
               marker_color=sapUiChartPaletteQualitativeHue1,
               name='Deviation Cause',
               orientation='h',
               text=df_dev_cause[displayed],
               textposition='outside',
               texttemplate='%{text:.2s}'),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(x=df_dev_indicator[displayed],
               y=df_dev_indicator['Deviation Indicator'],
               marker_color=sapUiChartPaletteQualitativeHue1,
               name='Deviation Indicator',
               orientation='h',
               text=df_dev_indicator[displayed],
               textposition='outside',
               texttemplate='%{text:.2s}'),
        row=1,
        col=2,
    )

    fig.update_layout(height=600,
                      barmode='group',
                      showlegend=False,
                      title='Deviated Orders by Deviation Cause and Indicator',
                      title_font_size=20,
                      font_color=SAP_TEXT_COLOR,
                      font_family=SAP_FONT,
                      template=template)

    fig.update_yaxes(categoryorder='total ascending')

    return fig


def get_data_sp_by_month_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Create DataFrame for supplier performance by month chart."""
    df_line_charts = df.loc[(df['Deviation Cause'] != 0) & (df['Year'] == 2020)]
    df_line_charts = df_line_charts.groupby([
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
    else:
        displayed = 'Ordered Spend'

    fig = go.Figure(
        go.Scatter(
            x=df['Month'],
            y=df[displayed],
            mode='lines+markers',
            marker_color=sapUiChartPaletteQualitativeHue1,
            name=displayed,
        ))

    fig.update_layout(height=520,
                      showlegend=False,
                      title='Deviated Orders by Month',
                      title_font_size=20,
                      font_color=SAP_TEXT_COLOR,
                      font_family=SAP_FONT,
                      template=template)

    return fig


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
    ]).agg({
        'Number of Orders': 'sum',
        'Ordered Spend': 'sum',
    }).reset_index()

    if df.empty:
        return empty_graph

    if number_of_orders:
        displayed = 'Number of Orders'
    else:
        displayed = 'Ordered Spend'

    fig = go.Figure(
        go.Bar(x=df[displayed],
               y=df['Purchasing Org.'],
               marker_color=sapUiChartPaletteQualitativeHue1,
               name=displayed,
               orientation='h',
               text=df[displayed],
               textposition='outside',
               texttemplate='%{text:.2s}'))

    fig.update_layout(height=520,
                      barmode='group',
                      showlegend=False,
                      title='Deviated Orders by Purchasing Organisation',
                      title_font_size=20,
                      font_color=SAP_TEXT_COLOR,
                      font_family=SAP_FONT,
                      template=template)

    fig.update_yaxes(type='category', categoryorder='total ascending')

    return fig


def get_data_sp_top_10_suppliers_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Create DataFrame for top 10 suppliers chart."""
    df_bar_charts = df.loc[(df['Deviation Cause'] != 0) & (df['Year'] == 2020)]
    df_bar_charts = df_bar_charts.groupby([
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
    ]).agg({
        'Number of Orders': 'sum',
        'Ordered Spend': 'sum',
    }).reset_index()

    supplier_names = df.nlargest(10, ['Ordered Spend'])['Supplier Name']
    df = df.loc[df['Supplier Name'].isin(supplier_names)]

    if df.empty:
        return empty_graph

    df.sort_values('Ordered Spend', ascending=False, inplace=True)

    if number_of_orders:
        displayed = 'Number of Orders'
    else:
        displayed = 'Ordered Spend'

    fig = go.Figure(
        go.Bar(x=df[displayed],
               y=df['Supplier Name'],
               marker_color=sapUiChartPaletteQualitativeHue1,
               name=displayed,
               orientation='h',
               text=df[displayed],
               textposition='outside',
               texttemplate='%{text:.2s}'))

    fig.update_layout(height=520,
                      barmode='group',
                      showlegend=False,
                      title='Deviated Orders of Top Ten Suppliers',
                      title_font_size=20,
                      font_color=SAP_TEXT_COLOR,
                      font_family=SAP_FONT,
                      template=template)

    fig.update_yaxes(categoryorder='total ascending')

    return fig
