"""Serves to read and prepare the data used for the dashboard."""
import os

import pandas as pd
from app import cache


@cache.memoize()
def get_data() -> pd.DataFrame:
    """Read and prepare the data.

    Reads the data from an Excel-File, applies
    the preparation required for the Dashboardand returns the data frame.

    Returns:
        Prepared DataFrame.
    """
    data_path = os.path.join(os.path.dirname(__file__), '../../data/Daten I.xlsx')
    df = pd.read_excel(data_path)

    _rename_columns(df)
    _drop_unnecessary_columns(df)
    _calculate_month_and_year(df)
    _calculate_delivery_details(df)

    return df


@cache.memoize()
def copy_and_apply_filter(
    df: pd.DataFrame,
    company_code: int,
    purchasing_org: int,
    plant: int,
    material_group: str,
) -> pd.DataFrame:
    """Copy the DataFrame and apply the filters from the GUI.

    Args:
        df: The DataFrame used for the dashboard.
        company_code, purchasing_org, plant, material_group: GUI filters.

    Returns:
        The filtered data as a DataFrame.
    """
    filtered_df = df.copy(deep=True)

    if company_code:
        filtered_df = filtered_df.loc[filtered_df['Company Code'] == company_code]

    if purchasing_org:
        filtered_df = filtered_df.loc[filtered_df['Purchasing Org.'] == purchasing_org]

    if plant:
        filtered_df = filtered_df.loc[filtered_df['Plant'] == plant]

    if material_group:
        filtered_df = filtered_df.loc[filtered_df['Material Group'].astype(str) == material_group]

    return filtered_df


def _rename_columns(df: pd.DataFrame) -> None:
    """Rename columns of the DataFrame."""
    name_dict = {
        'supplier delivery date': 'Supplier Delivery Date',
        'delivery date': 'Delivery Date',
        'Supplier name': 'Supplier Name',
        'Postal code': 'Postal Code',
        'Supplier\ncountry': 'Supplier Country',
        'Net price': 'Net Price',
        'ORDERED Quantity': 'Ordered Quantity',
        'Delivered QTY': 'Delivered Quantity',
        'open quantity': 'Open Quantity',
        'Delivery deviation  in days': 'Delivery Deviation (Days)',
        'deviation indicator': 'Deviation Indicator',
        'deviation cause': 'Deviation Cause',
        'deviation cause text': 'Deviation Cause Text'
    }
    df.rename(columns=name_dict, inplace=True)


def _drop_unnecessary_columns(df: pd.DataFrame) -> None:
    """Drop unnecessary columns of the DataFrame."""
    df.drop(columns=df.columns[-2:], axis=1, inplace=True)


def _calculate_month_and_year(df: pd.DataFrame) -> None:
    """Fill the missing values for the columns concerning month and year."""
    df['Year'] = df['Document Date'].dt.year
    df['Month'] = df['Document Date'].dt.month
    df['Year/Month'] = pd.to_datetime(df['Document Date']).dt.to_period('M')


def _determine_delivery_indicator(row: pd.Series) -> str:
    """Return the delivery indicator."""
    if row['Delivery Deviation (Days)'] <= 0:
        return 'in time'
    elif row['Delivery Deviation (Days)'] < 5:
        return 'late: < 5 days'
    elif row['Delivery Deviation (Days)'] > 10:
        return 'late: > 10 days'

    return 'late: 5 to 10 days'


def _calculate_delivery_details(df: pd.DataFrame) -> None:
    """Calculate the delivery deviation and classify the corresponding indicator."""
    df['Delivery Deviation (Days)'] = (df['Delivery Date'] - df['Supplier Delivery Date']).dt.days
    df['Deviation Indicator'] = df.apply(_determine_delivery_indicator, axis=1)
