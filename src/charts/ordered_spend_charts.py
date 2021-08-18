"""Ordered Spend Charts."""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_prep import copy_and_apply_filter


def get_data_os_numeric_point_charts(df: pd.DataFrame) -> pd.DataFrame:
    """"""
    df_point_charts = df.groupby(['Year', 'Company Code', 'Purchasing Org.', 'Plant', 'Material Group']).agg({
        'Document Date': 'count',
        'Net Value': 'sum'
    }).reset_index().rename(columns={
        'Net Value': 'Ordered Spend',
        'Document Date': 'Number of Orders'
    })
    return df_point_charts


def os_numeric_point_chart(df: pd.DataFrame,
                           company_code: str,
                           purchasing_org: str,
                           plant: str,
                           material_group: str,
                           last_year: bool = False) -> go.Figure:
    """Generate a numeric point chart for ordered spend."""
    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby('Year').agg({'Number of Orders': 'count', 'Ordered Spend': 'sum'}).reset_index()

    if last_year:
        year = 2019
        mode = 'number'
        delta_os = None
        delta_no = None
    else:
        year = 2020
        mode = 'number+delta'
        delta_os = df.loc[df['Year'] == 2019, 'Ordered Spend'].iloc[0]
        delta_no = df.loc[df['Year'] == 2019, 'Number of Orders'].iloc[0]

    df = df.loc[df['Year'] == year]
    ordered_spend = df['Ordered Spend'].iloc[0]
    number_of_orders = df['Number of Orders'].iloc[0]

    fig = go.Figure()
    fig.add_trace(
        go.Indicator(mode=mode,
                     value=ordered_spend,
                     domain={
                         'x': [0, 0.45],
                         'y': [0, 1]
                     },
                     delta={
                         'reference': delta_os,
                         'relative': True
                     },
                     title='Ordered Spend'))
    fig.add_trace(
        go.Indicator(mode=mode,
                     value=number_of_orders,
                     domain={
                         'x': [0.55, 1],
                         'y': [0, 1]
                     },
                     delta={
                         'reference': delta_no,
                         'relative': True
                     },
                     title='Number of Orders'))

    fig.update_layout(title_text=year)
    return fig


def get_data_bar_charts(df: pd.DataFrame) -> pd.DataFrame:
    """"""
    df_bar_charts = df.groupby(['Year', 'Supplier Name']).agg({
        'Document Date': 'count',
        'Net Value': 'sum'
    }).reset_index().rename(columns={
        'Net Value': 'Ordered Spend',
        'Document Date': 'Number of Orders'
    })

    supplier_names = df_bar_charts.nlargest(10, ['Year', 'Ordered Spend'])['Supplier Name']
    df_bar_charts = df_bar_charts.loc[df_bar_charts['Supplier Name'].isin(supplier_names)]

    return df_bar_charts


def os_bar_chart(df: pd.DataFrame,
                 company_code: str,
                 purchasing_org: str,
                 plant: str,
                 material_group: str,
                 number_of_orders: bool = False) -> go.Figure:
    """"""
    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby(['Year', 'Supplier Name']).agg({'Number of Orders': 'count', 'Ordered Spend': 'sum'}).reset_index()
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

    fig.update_layout(title=displayed, barmode='group', xaxis_tickangle=-45)
    return fig


def get_data_os_line_charts(df: pd.DataFrame) -> pd.DataFrame:
    df_line_charts = df.groupby(['Year', 'Month', 'Company Code', 'Purchasing Org.', 'Plant', 'Material Group']).agg({
        'Document Date': 'count',
        'Net Value': 'sum'
    }).reset_index().rename(columns={
        'Net Value': 'Ordered Spend',
        'Document Date': 'Number of Orders'
    })
    return df_line_charts


def os_line_chart(df: pd.DataFrame,
                  company_code: str,
                  purchasing_org: str,
                  plant: str,
                  material_group: str,
                  number_of_orders: bool = False) -> go.Figure:
    """"""
    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby(['Year', 'Month']).agg({'Number of Orders': 'count', 'Ordered Spend': 'sum'}).reset_index()
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

    fig.update_layout(title_text=displayed)
    return fig


def get_data_os_pie_charts(df: pd.DataFrame) -> pd.DataFrame:
    """"""
    df_pie_charts = df.groupby(['Year', 'Purchasing Org.', 'Company Code', 'Plant', 'Material Group']).agg({
        'Document Date': 'count',
        'Net Value': 'sum'
    }).reset_index().rename(columns={
        'Net Value': 'Ordered Spend',
        'Document Date': 'Number of Orders'
    })

    return df_pie_charts


def os_pie_chart(df: pd.DataFrame,
                 company_code: str,
                 purchasing_org: str,
                 plant: str,
                 material_group: str,
                 number_of_orders: bool = False) -> go.Figure:

    df = copy_and_apply_filter(df, company_code, purchasing_org, plant, material_group)
    df = df.groupby(['Year', 'Purchasing Org.']).agg({
        'Number of Orders': 'count',
        'Ordered Spend': 'sum'
    }).reset_index()

    if number_of_orders:
        displayed = 'Number of Orders'
    else:
        displayed = 'Ordered Spend'

    df_this_year = df.loc[df['Year'] == 2020]
    df_last_year = df.loc[df['Year'] == 2019]

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

    fig.add_trace(
        go.Pie(labels=df_this_year['Purchasing Org.'],
               values=df_this_year[displayed],
               name=2020,
               textinfo='label+percent',
               direction='clockwise'), 1, 1)
    fig.add_trace(
        go.Pie(labels=df_last_year['Purchasing Org.'],
               values=df_last_year[displayed],
               name=2019,
               textinfo='label+percent',
               direction='clockwise'), 1, 2)
    fig.update_layout(title=displayed)
    return fig
