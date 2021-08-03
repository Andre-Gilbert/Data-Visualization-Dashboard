"""Serves to read and prepare the data used for the dashboard."""
import os

import pandas as pd


def get_data() -> pd.DataFrame:
    """Reads the data from an Excel-File, applies the preparation required for the Dashboard and returns the data frame.
    Should be the only function called from outside.

    Args:
        None
    Returns:
        df: Prepared DataFrame, usable for the Dashboard"""

    data_path = os.path.join(os.path.dirname(__file__), '../../data/Daten I.xlsx')
    df = pd.read_excel(data_path)

    return df


print(get_data().info())
