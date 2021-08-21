"""Supplier Performance Charts."""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_prep import copy_and_apply_filter


def get_data_sp_total_deviation_and_percentage_charts(df: pd.DataFrame) -> tuple[pd.DataFrame]:
    """Creates the DataFrames to be used for the Supplier Performance Total Deviation and Percentage and
    by Purchasing Organisation Charts.

    Returns:
        df_total_deviation_and_percentage_charts: DataFrame containing sum and count of only Orders with Deviation Cause
            != 0 and year == 2020, intended for functions sp_total_deviation_and_percentage_chart and sp_by_org_chart.
        df_reference: DataFrame containing sum and count of all Orders of year == 2020, intended only for
            function sp_total_deviation_and_percentage_chart."""

    group_columns = ['Company Code', 'Purchasing Org.', 'Plant', 'Material Group']
    aggregate_functions = {'Document Date': 'count', 'Net Value': 'sum'}
    rename_columns = {'Net Value': 'Ordered Spend', 'Document Date': 'Number of Orders'}

    df_total_deviation_and_percentage_charts = df.loc[df['Year'] == 2020]
    df_total_deviation_and_percentage_charts = df_total_deviation_and_percentage_charts.groupby(group_columns).agg(
        aggregate_functions).reset_index().rename(columns=rename_columns)

    df_reference = df.loc[(df['Deviation Cause'] != 0) & (df['Year'] == 2020)]
    df_reference = df_reference.groupby(group_columns).agg(aggregate_functions).reset_index().rename(
        columns=rename_columns)

    return df_reference, df_total_deviation_and_percentage_charts


def sp_total_deviation_and_percentage_chart(df_deviated: pd.DataFrame,
                                            df_all: pd.DataFrame,
                                            number_of_orders: bool = False,
                                            company_code: str = None,
                                            purchasing_org: str = None,
                                            plant: str = None,
                                            material_group: str = None) -> go.Figure:
    """Creates a Figure containing two Numeric Point Chart Traces for total and percentage of
    either Ordered Spend or Number of Deviated Orders this year.

    Args:
        df_deviated: First DataFrame produced by function get_data_sp_total_deviation_and_percentage_charts.
        df_all: Second DataFrame produced by function get_data_sp_total_deviation_and_percentage_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI."""

    df_deviated = copy_and_apply_filter(df_deviated, company_code, purchasing_org, plant, material_group)
    df_deviated = df_deviated.agg({'Number of Orders': 'sum', 'Ordered Spend': 'sum'})

    df_all = copy_and_apply_filter(df_all, company_code, purchasing_org, plant, material_group)
    df_all = df_all.agg({'Number of Orders': 'sum', 'Ordered Spend': 'sum'})

    if number_of_orders:
        displayed = 'Number of Orders'
    else:
        displayed = 'Ordered Spend'

    value_deviated = df_deviated[displayed]
    value_all = df_all[displayed]

    percentage = (value_deviated / value_all)

    fig = go.Figure()

    fig.add_trace(
        go.Indicator(mode='number',
                     value=value_deviated,
                     domain={
                         'x': [0, 0.45],
                         'y': [0, 1]
                     },
                     title='Total of Deviated Orders'))
    fig.add_trace(
        go.Indicator(mode='number',
                     value=percentage,
                     number={'valueformat': '.2%'},
                     domain={
                         'x': [0.55, 1],
                         'y': [0, 1]
                     },
                     title='Percentage of all Orders'))

    return fig


def get_data_sp_deviation_cause_and_indicator_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Creates the DataFrame to be used for the Supplier Performance Deviation Cause and Indicator Charts."""

    df_bar_charts = df.loc[(df['Deviation Cause'] != 0) & (df['Year'] == 2020)]
    df_bar_charts = df_bar_charts.groupby(
        ['Deviation Cause Text', 'Deviation Indicator', 'Company Code', 'Purchasing Org.', 'Plant',
         'Material Group']).agg({
             'Document Date': 'count',
             'Net Value': 'sum'
         }).reset_index().rename(columns={
             'Net Value': 'Ordered Spend',
             'Document Date': 'Number of Orders'
         })

    return df_bar_charts


def sp_deviation_cause_and_indicator_chart(df: pd.DataFrame,
                                           number_of_orders: bool = False,
                                           company_code: str = None,
                                           purchasing_org: str = None,
                                           plant: str = None,
                                           material_group: str = None) -> go.Figure:
    """Creates a Figure containing two Bar Chart Subplots showing either Ordered Spend or Number
    of Deviated Orders by Deviation Cause and Deviation Indicator.

    Args:
        df: DataFrame produced by function get_data_sp_deviation_cause_and_indicator_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI."""

    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)

    df_dev_cause = df.groupby(['Deviation Cause Text']).agg({
        'Number of Orders': 'sum',
        'Ordered Spend': 'sum'
    }).reset_index()
    df_dev_cause.rename(columns={'Deviation Cause Text': 'Deviation Cause'}, inplace=True)

    df_dev_indicator = df.groupby(['Deviation Indicator']).agg({
        'Number of Orders': 'sum',
        'Ordered Spend': 'sum'
    }).reset_index()

    if number_of_orders:
        displayed = 'Number of Orders'
    else:
        displayed = 'Ordered Spend'

    fig = make_subplots(rows=1, cols=2, subplot_titles=('Deviation Cause', 'Deviation Indicator'))
    fig.add_trace(go.Bar(x=df_dev_cause['Deviation Cause'], y=df_dev_cause[displayed], name='Deviation Cause'), 1, 1)
    fig.add_trace(
        go.Bar(x=df_dev_indicator['Deviation Indicator'], y=df_dev_indicator[displayed], name='Deviation Indicator'), 1,
        2)

    fig.update_layout(barmode='group', xaxis_tickangle=-45, showlegend=False)

    return fig


def get_data_sp_by_month_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Creates the DataFrame to be used for the Supplier Performance by Month Charts."""

    df_line_charts = df.loc[(df['Deviation Cause'] != 0) & (df['Year'] == 2020)]
    df_line_charts = df_line_charts.groupby(['Month', 'Company Code', 'Purchasing Org.', 'Plant',
                                             'Material Group']).agg({
                                                 'Document Date': 'count',
                                                 'Net Value': 'sum'
                                             }).reset_index().rename(columns={
                                                 'Net Value': 'Ordered Spend',
                                                 'Document Date': 'Number of Orders'
                                             })

    return df_line_charts


def sp_by_month_chart(df: pd.DataFrame,
                      number_of_orders: bool = False,
                      company_code: str = None,
                      purchasing_org: str = None,
                      plant: str = None,
                      material_group: str = None) -> go.Figure:
    """Creates a Line Chart showing either Ordered Spend or Number of Deviated Orders by Month.

    Args:
        df: DataFrame produced by function get_data_sp_by_month_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI."""

    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby(['Month']).agg({'Number of Orders': 'sum', 'Ordered Spend': 'sum'}).reset_index()
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

    if number_of_orders:
        displayed = 'Number of Orders'
    else:
        displayed = 'Ordered Spend'

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df['Month'],
                   y=df[displayed],
                   mode='lines+markers',
                   name=displayed,
                   title_text=displayed,
                   title_position='bottom center'))

    fig.update_layout(showlegend=False)

    return fig


def sp_by_org_chart(df: pd.DataFrame,
                    number_of_orders: bool = False,
                    company_code: str = None,
                    purchasing_org: str = None,
                    plant: str = None,
                    material_group: str = None) -> go.Figure:
    """Creates a Bar Chart Traces showing either Ordered Spend or Number of Deviated Orders by
    Purchasing Organisation.

    Args:
        df: First DataFrame produced by function get_data_sp_total_deviation_and_percentage_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI."""

    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby(['Purchasing Org.']).agg({'Number of Orders': 'sum', 'Ordered Spend': 'sum'}).reset_index()

    if number_of_orders:
        displayed = 'Number of Orders'
    else:
        displayed = 'Ordered Spend'

    fig = go.Figure()

    fig.add_trace(go.Bar(x=df['Purchasing Org.'], y=df[displayed], name=displayed))

    fig.update_layout(barmode='group', xaxis_tickangle=-45, showlegend=False)

    return fig


def get_data_sp_top_10_suppliers_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Creates the DataFrame to be used for the Supplier Performance Top 10 Suppliers Charts."""

    df_bar_charts = df.loc[(df['Deviation Cause'] != 0) & (df['Year'] == 2020)]
    df_bar_charts = df_bar_charts.groupby(
        ['Supplier Name', 'Company Code', 'Purchasing Org.', 'Plant', 'Material Group']).agg({
            'Document Date': 'count',
            'Net Value': 'sum'
        }).reset_index().rename(columns={
            'Net Value': 'Ordered Spend',
            'Document Date': 'Number of Orders'
        })

    return df_bar_charts


def sp_top_10_suppliers_chart(df: pd.DataFrame,
                              number_of_orders: bool = False,
                              company_code: str = None,
                              purchasing_org: str = None,
                              plant: str = None,
                              material_group: str = None) -> go.Figure:
    """Creates a Bar Chart Traces showing either Ordered Spend or Number of Deviated Orders of
    Top 10 Suppliers by Ordered Spend.

    Args:
        df: DataFrame produced by function get_data_sp_top_10_suppliers_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI."""

    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby(['Supplier Name']).agg({'Number of Orders': 'sum', 'Ordered Spend': 'sum'}).reset_index()

    supplier_names = df.nlargest(10, ['Ordered Spend'])['Supplier Name']
    df = df.loc[df['Supplier Name'].isin(supplier_names)]

    df.sort_values('Ordered Spend', ascending=False, inplace=True)

    if number_of_orders:
        displayed = 'Number of Orders'
    else:
        displayed = 'Ordered Spend'

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df['Supplier Name'],
            y=df[displayed],
            name=displayed,
            title_text=displayed,
            title_position='bottom center',
        ))

    fig.update_layout(barmode='group', xaxis_tickangle=-45, showlegend=False)

    return fig
