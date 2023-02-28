from datetime import date
import calendar


def generate_file_name(base_name: str) -> str:
    current_date = date.today()
    last_day_of_previous_month = get_last_day_of_previous_month()
    base_name = base_name + "{detail_date}"
    file_name = base_name.format(detail_date=f"-{current_date.year}-{current_date.month}"
                                             f"-{last_day_of_previous_month}")
    return file_name


def get_last_day_of_previous_month() -> int:
    current_date = date.today()
    previous_month_number = get_previous_month_number()
    return calendar.monthrange(current_date.year, previous_month_number)[1]


def get_previous_month_number() -> int:
    december_number_month = 12
    month = date.today().month
    previous_month_number = month - 1
    return december_number_month if previous_month_number == 0 else previous_month_number
