from charts.config import (NUMBER_OF_ORDERS, ORDERED_SPEND, SUBTITLE_NUMBER_OF_ORDERS, SUBTITLE_ORDERED_SPEND)

suffices = ['', 'k', 'M', 'B', 'T']


def format_numbers(row, displayed):
    counter = 0
    number = row[displayed]
    if (number < 1000) and (type(number) == int):
        return f'{int(number)}'
    while number >= 1000:
        number /= 1000
        counter += 1
    return f'{number:.1f}{suffices[counter]}'


def apply_number_of_orders_flag(number_of_orders: bool) -> tuple[str]:
    if number_of_orders:
        displayed = NUMBER_OF_ORDERS
        subtitle = SUBTITLE_NUMBER_OF_ORDERS
    else:
        displayed = ORDERED_SPEND
        subtitle = SUBTITLE_ORDERED_SPEND
    return displayed, subtitle