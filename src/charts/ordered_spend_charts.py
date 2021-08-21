"""Ordered Spend Charts."""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_prep import copy_and_apply_filter


def get_data_os_total_by_year_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Creates the DataFrame to be used for the Ordered Spend Total by Year Charts."""

    df_point_charts = df.groupby(['Year', 'Company Code', 'Purchasing Org.', 'Plant', 'Material Group']).agg({
        'Document Date': 'count',
        'Net Value': 'sum'
    }).reset_index().rename(columns={
        'Net Value': 'Ordered Spend',
        'Document Date': 'Number of Orders'
    })
    return df_point_charts


def os_total_by_year_chart(df: pd.DataFrame,
                           number_of_orders: bool = False,
                           company_code: str = None,
                           purchasing_org: str = None,
                           plant: str = None,
                           material_group: str = None) -> go.Figure:
    """Creates a Figure containing two Numeric Point Charts for Ordered Spend and Number of Orders
    this or last year.

    Args:
        df: DataFrame produced by function get_data_os_total_by_year_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI."""

    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby('Year').agg({'Number of Orders': 'sum', 'Ordered Spend': 'sum'}).reset_index()

    df_this_year = df.loc[df['Year'] == 2020]
    df_last_year = df.loc[df['Year'] == 2019]

    if number_of_orders:
        displayed = 'Number of Orders'
    else:
        displayed = 'Ordered Spend'

    value_this_year = df_this_year[displayed].iloc[0]
    value_last_year = df_last_year[displayed].iloc[0]

    fig = go.Figure()

    fig.add_trace(
        go.Indicator(mode='number+delta',
                     value=value_this_year,
                     domain={
                         'x': [0, 0.45],
                         'y': [0, 1]
                     },
                     delta={
                         'reference': value_last_year,
                         'relative': True
                     },
                     title='2020'))
    fig.add_trace(go.Indicator(mode='number', value=value_last_year, domain={
        'x': [0.55, 1],
        'y': [0, 1]
    }, title='2019'))

    return fig


def get_data_os_by_month_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Creates the DataFrame to be used for the Ordered Spend by Month Charts."""

    df_line_charts = df.groupby(['Year', 'Month', 'Company Code', 'Purchasing Org.', 'Plant', 'Material Group']).agg({
        'Document Date': 'count',
        'Net Value': 'sum'
    }).reset_index().rename(columns={
        'Net Value': 'Ordered Spend',
        'Document Date': 'Number of Orders'
    })
    return df_line_charts


def os_by_month_chart(df: pd.DataFrame,
                      number_of_orders: bool = False,
                      company_code: str = None,
                      purchasing_org: str = None,
                      plant: str = None,
                      material_group: str = None) -> go.Figure:
    """Creates a Figure containing two Line Chart Traces comparing either
    Ordered Spend or Number of Orders by Month for this and last year.

    Args:
        df: DataFrame produced by function get_data_os_by_month_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI."""

    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby(['Year', 'Month']).agg({'Number of Orders': 'sum', 'Ordered Spend': 'sum'}).reset_index()
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

    df_this_year = df.loc[df['Year'] == 2020]
    df_last_year = df.loc[df['Year'] == 2019]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_this_year['Month'], y=df_this_year[displayed], mode='lines+markers', name=2020))
    fig.add_trace(go.Scatter(x=df_last_year['Month'], y=df_last_year[displayed], mode='lines+markers', name=2019))

    return fig


def os_by_org_chart(df: pd.DataFrame,
                    number_of_orders: bool = False,
                    company_code: str = None,
                    purchasing_org: str = None,
                    plant: str = None,
                    material_group: str = None) -> go.Figure:
    """Creates a Figure containing two Bar Chart Traces comparing either Ordered Spend or
    Number of Orders by Purchasing Organisation for this and last year.

    Args:
        df: DataFrame produced by function get_data_os_total_by_year_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI."""

    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby(['Year', 'Purchasing Org.']).agg({'Number of Orders': 'sum', 'Ordered Spend': 'sum'}).reset_index()

    if number_of_orders:
        displayed = 'Number of Orders'
    else:
        displayed = 'Ordered Spend'

    df_this_year = df.loc[df['Year'] == 2020]
    df_last_year = df.loc[df['Year'] == 2019]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_this_year['Purchasing Org.'],
        y=df_last_year[displayed],
        name=2020,
    ))
    fig.add_trace(go.Bar(
        x=df_last_year['Purchasing Org.'],
        y=df_last_year[displayed],
        name=2019,
    ))

    fig.update_layout(barmode='group', xaxis_tickangle=-45)

    fig.update_xaxes(type='category')

    return fig


def get_data_os_top_10_suppliers_charts(df: pd.DataFrame) -> pd.DataFrame:
    """Creates the DataFrame to be used for the Ordered Spend by Top 10 Suppliers Charts."""

    df_bar_charts = df.groupby(['Year', 'Supplier Name', 'Company Code', 'Purchasing Org.', 'Plant',
                                'Material Group']).agg({
                                    'Document Date': 'count',
                                    'Net Value': 'sum'
                                }).reset_index().rename(columns={
                                    'Net Value': 'Ordered Spend',
                                    'Document Date': 'Number of Orders'
                                })
    return df_bar_charts


def os_top_10_suppliers_chart(df: pd.DataFrame,
                              number_of_orders: bool = False,
                              company_code: str = None,
                              purchasing_org: str = None,
                              plant: str = None,
                              material_group: str = None) -> go.Figure:
    """Creates a Figure containing two Bar Chart Traces comparing either Ordered Spend or Number of Orders by Top 10
    Suppliers for this and last year, determines Top 10 Suppliers by Ordered Spend in 2020 and filters in GUI.

    Args:
        df: DataFrame produced by function get_data_os_top_10_suppliers_charts.
        number_of_orders: Flag that dictates whether to display Ordered Spend or Number of Orders.
        company_code, purchasing_org, plant, material_group: Filters from GUI."""

    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby(['Year', 'Supplier Name']).agg({'Number of Orders': 'sum', 'Ordered Spend': 'sum'}).reset_index()

    supplier_names = df.nlargest(10, ['Year', 'Ordered Spend'])['Supplier Name']
    df = df.loc[df['Supplier Name'].isin(supplier_names)]

    if number_of_orders:
        displayed = 'Number of Orders'
    else:
        displayed = 'Ordered Spend'

    df.sort_values(displayed, ascending=False, inplace=True)

    df_this_year = df.loc[df['Year'] == 2020]
    df_last_year = df.loc[df['Year'] == 2019]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_this_year['Supplier Name'],
        y=df_last_year[displayed],
        name=2020,
    ))
    fig.add_trace(go.Bar(
        x=df_last_year['Supplier Name'],
        y=df_last_year[displayed],
        name=2019,
    ))

    fig.update_layout(barmode='group', xaxis_tickangle=-45)

    return fig
