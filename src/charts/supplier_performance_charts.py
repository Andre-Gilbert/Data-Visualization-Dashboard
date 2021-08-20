"""Supplier Performance Charts."""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_prep import copy_and_apply_filter


def get_data_sp_point_and_pie_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Creates the DataFrames to be used for the Supplier Performance Numeric Point and Pie Charts.

    Returns:
        df_deviated: DataFrame containing sum and count of only Orders with Deviation Cause != 0 and
            year == 2020, intended for Numeric Point and Pie Charts.
        df_all: DataFrame containing sum and count of all Orders of year == 2020, intended only for
            Numeric Point Charts."""

    group_columns = ['Company Code', 'Purchasing Org.', 'Plant', 'Material Group']
    aggregate_functions = {'Document Date': 'count', 'Net Value': 'sum'}
    rename_columns = {'Net Value': 'Ordered Spend', 'Document Date': 'Number of Orders'}

    df_all = df.loc[df['Year'] == 2020]
    df_all = df_all.groupby(group_columns).agg(aggregate_functions).reset_index().rename(columns=rename_columns)

    df_deviated = df.loc[(df['Deviation Cause'] != 0) & (df['Year'] == 2020)]
    df_deviated = df_deviated.groupby(group_columns).agg(aggregate_functions).reset_index().rename(
        columns=rename_columns)
    return df_deviated, df_all


def sp_numeric_point_chart(df_deviated: pd.DataFrame,
                           df_all: pd.DataFrame,
                           number_of_orders: bool = False,
                           company_code: str = None,
                           purchasing_org: str = None,
                           plant: str = None,
                           material_group: str = None) -> go.Figure:
    """Creates a Figure containing two Numeric Point Charts for total and percentage of
    either Ordered Spend or Number of Orders of deviated Orders this year.

    Args:
        df_deviated: First DataFrame produced by function get_data_sp_point_and_pie_charts.
        df_all: First DataFrame produced by function get_data_sp_point_and_pie_charts.
        number_of_orders: Flag that dictated whether to display Ordered Spend or Number of Orders.
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

    fig.update_layout(title_text=displayed)
    return fig


def get_data_sp_deviation_bar_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Creates the DataFrame to be used for the Supplier Performance Deviation Bar Charts."""

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


def sp_deviation_bar_chart(df: pd.DataFrame,
                           number_of_orders: bool = False,
                           company_code: str = None,
                           purchasing_org: str = None,
                           plant: str = None,
                           material_group: str = None) -> go.Figure:
    """Creates a Figure containing two Bar Charts comparing either Ordered Spend or Number
    of Orders of deviated Orders by Deviation Cause and Deviation Indicator.

    Args:
        df: DataFrame produced by function get_data_sp_deviation_bar_charts.
        number_of_orders: Flag that dictated whether to display Ordered Spend or Number of Orders.
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

    fig.update_layout(title=displayed, barmode='group', xaxis_tickangle=-45, showlegend=False)
    return fig


def get_data_sp_line_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Creates the DataFrame to be used for the Supplier Performance Line Charts."""

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


def sp_line_chart(df: pd.DataFrame,
                  company_code: str = None,
                  purchasing_org: str = None,
                  plant: str = None,
                  material_group: str = None) -> go.Figure:
    """Creates a Figure containing two Line Charts comparing Ordered Spend and Number
    of Orders of deviated Orders by Month.

    Args:
        df: DataFrame produced by function get_data_sp_line_charts.
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

    fig = make_subplots(rows=1, cols=2, subplot_titles=('Ordered Spend', 'Number of Orders'))

    fig.add_trace(go.Scatter(x=df['Month'], y=df['Ordered Spend'], mode='lines+markers', name='Ordered Spend'), 1, 1)
    fig.add_trace(go.Scatter(x=df['Month'], y=df['Number of Orders'], mode='lines+markers', name='Number of Orders'), 1,
                  2)

    fig.update_layout(title_text='Deviated Deliveries by Month', showlegend=False)

    return fig


def sp_pie_chart(df: pd.DataFrame,
                 company_code: str = None,
                 purchasing_org: str = None,
                 plant: str = None,
                 material_group: str = None) -> go.Figure:
    """Creates a Figure containing two Pie Charts comparing Ordered Spend and Number
    of Orders of deviated Orders by Purchasing Organisation.

    Args:
        df: First DataFrame produced by function get_data_sp_point_and_pie_charts.
        company_code, purchasing_org, plant, material_group: Filters from GUI."""

    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby(['Purchasing Org.']).agg({'Number of Orders': 'sum', 'Ordered Spend': 'sum'}).reset_index()

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

    fig.add_trace(
        go.Pie(labels=df['Purchasing Org.'],
               values=df['Ordered Spend'],
               name='Ordered Spend',
               title_text='Ordered Spend',
               title_position='bottom center',
               textinfo='label+percent',
               direction='clockwise'), 1, 1)
    fig.add_trace(
        go.Pie(labels=df['Purchasing Org.'],
               values=df['Number of Orders'],
               name='Number of Orders',
               title_text='Number of Orders',
               title_position='bottom center',
               textinfo='label+percent',
               direction='clockwise'), 1, 2)
    fig.update_layout(title='Deviated Deliveries by Purchasing Organisation')
    return fig


def get_data_sp_supplier_bar_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Creates the DataFrame to be used for the Supplier Performance Top 10 Suppliers Bar Charts."""

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


def sp_supplier_bar_chart(df: pd.DataFrame,
                          company_code: str = None,
                          purchasing_org: str = None,
                          plant: str = None,
                          material_group: str = None) -> go.Figure:
    """Creates a Figure containing two Bar Charts comparing Ordered Spend and Number
    of Orders of deviated Orders of Top 10 Suppliers.

    Args:
        df: DataFrame produced by function get_data_sp_supplier_bar_charts.
        company_code, purchasing_org, plant, material_group: Filters from GUI."""

    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby(['Supplier Name']).agg({'Number of Orders': 'sum', 'Ordered Spend': 'sum'}).reset_index()

    supplier_names = df.nlargest(10, ['Ordered Spend'])['Supplier Name']
    df = df.loc[df['Supplier Name'].isin(supplier_names)]

    df.sort_values('Ordered Spend', ascending=False, inplace=True)

    fig = make_subplots(rows=1, cols=2, subplot_titles=('Ordered Spend', 'Number of Orders'))
    fig.add_trace(go.Bar(
        x=df['Supplier Name'],
        y=df['Ordered Spend'],
        name='Ordered Spend',
    ), 1, 1)
    fig.add_trace(go.Bar(
        x=df['Supplier Name'],
        y=df['Number of Orders'],
        name='Number of Orders',
    ), 1, 2)

    fig.update_layout(title='Deviated Deliveries by Top 10 Suppliers',
                      barmode='group',
                      xaxis_tickangle=-45,
                      showlegend=False)
    return fig
