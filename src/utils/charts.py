"""Chart Functions."""
from typing import Union

import numpy as np
import pandas as pd
from app import cache

from charts.config import (NUMBER_OF_ORDERS, ORDERED_SPEND, SUBTITLE_NUMBER_OF_ORDERS, SUBTITLE_ORDERED_SPEND)


def __numpy_float_is_int(x_float: Union[float, np.float64]) -> bool:
    """Check if float number is approximately an integer."""
    x_int = np.around(x_float, 0)
    x_res = x_float % x_int
    return np.isclose(x_res, 0.0)


@cache.memoize()
def format_numbers(row: pd.Series, displayed: str) -> str:
    """Format numbers to be displayed."""
    suffices = ['', 'k', 'M', 'B', 'T']
    counter = 0
    number = row[displayed]

    if number < 1000 and (isinstance(number, int) or (__numpy_float_is_int(number))):
        return f'{int(number)}'

    while number >= 1000:
        number /= 1000
        counter += 1

    return f'{number:.1f}{suffices[counter]}'


def apply_number_of_orders_flag(number_of_orders: bool) -> tuple[str]:
    """Apply chart subtitle and values to display."""
    if number_of_orders:
        displayed = NUMBER_OF_ORDERS
        subtitle = SUBTITLE_NUMBER_OF_ORDERS
    else:
        displayed = ORDERED_SPEND
        subtitle = SUBTITLE_ORDERED_SPEND

    return displayed, subtitle
