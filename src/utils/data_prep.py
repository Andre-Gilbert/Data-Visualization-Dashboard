"""Serves to read and prepare the data used for the dashboard."""
import os

import pandas as pd


def get_data() -> pd.DataFrame:
    """Reads the data from an Excel-File, applies the preparation required for the Dashboard and returns the data frame.
    Should be the only function called from outside.

    Returns:
        df: Prepared DataFrame, usable for the Dashboard
    """
    data_path = os.path.join(os.path.dirname(__file__), '../../data/Daten I.xlsx')
    df = pd.read_excel(data_path)

    __rename_columns(df)
    __drop_unnecessary_columns(df)
    __calculate_month_and_year(df)
    __calculate_delivery_details(df)

    return df


def copy_and_apply_filter(
    df: pd.DataFrame,
    company_code: str,
    purchasing_org: str,
    plant: str,
    material_group: str,
) -> pd.DataFrame:
    """Copies the DataFrame and applies the filters from the GUI if they are set."""
    filtered_df = df.copy(deep=True)

    if company_code:
        company_code = int(company_code)
        filtered_df = filtered_df.loc[filtered_df['Company Code'] == company_code]

    if purchasing_org:
        purchasing_org = int(purchasing_org)
        filtered_df = filtered_df.loc[filtered_df['Purchasing Org.'] == purchasing_org]

    if plant:
        plant = int(plant)
        filtered_df = filtered_df.loc[filtered_df['Plant'] == plant]

    if material_group:
        filtered_df = filtered_df.loc[filtered_df['Material Group'].astype(str) == material_group]

    return filtered_df


def __rename_columns(df: pd.DataFrame) -> None:
    """Renames columns of the DataFrame so the names are uniform and can be used in the Dashboard"""
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


def __drop_unnecessary_columns(df: pd.DataFrame) -> None:
    """Drops all columns not required for the Dashboard."""
    df.drop(columns=df.columns[-2:], axis=1, inplace=True)


def __calculate_month_and_year(df: pd.DataFrame) -> None:
    """Fills the missing values for the columns concerning month and year."""
    df['Year'] = df['Document Date'].dt.year
    df['Month'] = df['Document Date'].dt.month
    df['Year/Month'] = pd.to_datetime(df['Document Date']).dt.to_period('M')


def __determine_delivery_indicator(row: pd.DataFrame) -> str:
    """Returns the delivery indicator."""
    if row['Delivery Deviation (Days)'] <= 0:
        return 'in time'
    elif row['Delivery Deviation (Days)'] < 5:
        return 'late: < 5 days'
    elif row['Delivery Deviation (Days)'] > 10:
        return 'late: > 10 days'
    return 'late: 5 to 10 days'


def __calculate_delivery_details(df: pd.DataFrame) -> None:
    """Calculated Delivery Deviation and classifies the corresponding indicator."""
    df['Delivery Deviation (Days)'] = (df['Delivery Date'] - df['Supplier Delivery Date']).dt.days
    df['Deviation Indicator'] = df.apply(__determine_delivery_indicator, axis=1)
