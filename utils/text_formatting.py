def printHeader(text):
    print(f'\n-------------------------------------\n{text}\n-------------------------------------')


def printSmallHeader(text):
    print(f'------------{text}------------')


def fmt_num(number):
    formatted_number = format(int(number), ",")
    return formatted_number


def fmt_time(milliseconds):
    time = int(milliseconds)
    seconds, milliseconds = divmod(time, 1000)
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"
