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
