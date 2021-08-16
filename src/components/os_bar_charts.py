import pandas as pd
import plotly.graph_objects as go


def get_data_bar_charts(df):
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


def os_bar_chart(df, number_of_orders=False):
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
