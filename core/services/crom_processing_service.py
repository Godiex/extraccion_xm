import os
import tempfile
from datetime import date
import calendar

from infrastructure import HttpClientXm


class CromProcessingService:
    __COMPLEMENTARY_BASE_URL = "CROM/Resultados definitivos/{year}/{month_number}. {diminutive_month_name}/Resultados" \
                               "CROMdefinitivo_{month_name}{year}.xlsx"
    __MONTHS = {
        "1": {
            "month_name": "Enero",
            "month_number": "01",
            "diminutive_month_name": "Ene",
        },
        "2": {
            "month_name": "Febrero",
            "month_number": "02",
            "diminutive_month_name": "Feb",
        },
        "3": {
            "month_name": "Marzo",
            "month_number": "03",
            "diminutive_month_name": "Mar",
        },
        "4": {
            "month_name": "Abril",
            "month_number": "04",
            "diminutive_month_name": "Abr",
        },
        "5": {
            "month_name": "Mayo",
            "month_number": "05",
            "diminutive_month_name": "May",
        },
        "6": {
            "month_name": "Junio",
            "month_number": "06",
            "diminutive_month_name": "Jun",
        },
        "7": {
            "month_name": "Julio",
            "month_number": "07",
            "diminutive_month_name": "Jul",
        },
        "8": {
            "month_name": "Agosto",
            "month_number": "08",
            "diminutive_month_name": "Ago",
        },
        "9": {
            "month_name": "Septiembre",
            "month_number": "09",
            "diminutive_month_name": "Sep",
        },
        "10": {
            "month_name": "Octubre",
            "month_number": "10",
            "diminutive_month_name": "Oct",
        },
        "11": {
            "month_name": "Noviembre",
            "month_number": "11",
            "diminutive_month_name": "Nov",
        },
        "12": {
            "month_name": "Diciembre",
            "month_number": "12",
            "diminutive_month_name": "Dic",
        },
    }
    __FILE_TEMPORARY_NAME = "CROM{detail_date}.xls"
    __temporary_directory: str

    def __init__(self, http_client_xm: HttpClientXm):
        self.http_client_xm = http_client_xm
        self.PATH_DOWNLOAD = os.environ["PATH_DOWNLOAD"]

    def get(self) -> None:
        year = date.today().year
        previos_mounth = self.get_previous_month_number()
        month_info = self.__MONTHS[str(previos_mounth)]
        complementary_url = self.__COMPLEMENTARY_BASE_URL.format(
            year=year,
            month_number=month_info["month_number"],
            diminutive_month_name=month_info["diminutive_month_name"],
            month_name=month_info["month_name"]
        )
        file_xm = self.http_client_xm.get(complementary_base_url=complementary_url)
        self.download_crom_of_xm(file_xm)

    @staticmethod
    def get_previous_month_number():
        december_number_month = 12
        month = date.today().month
        previous_month_number = month - 1
        if previous_month_number == 0:
            return december_number_month
        return previous_month_number

    def download_crom_of_xm(self, file_xm):
        file_name = self.generate_file_name()
        self.__temporary_directory = str(tempfile.TemporaryDirectory())
        with open(f"{self.PATH_DOWNLOAD}/{file_name}", 'wb') as file:
            file.write(file_xm.content)

    def generate_file_name(self):
        current_date = date.today()
        last_day_of_previous_month = self.get_last_day_of_previous_month()
        file_name = self.__FILE_TEMPORARY_NAME.format(detail_date=f"-{current_date.year}-{current_date.month}"
                                                                  f"-{last_day_of_previous_month}")
        return file_name

    def get_last_day_of_previous_month(self) -> int:
        current_date = date.today()
        previous_month_number = self.get_previous_month_number()
        return calendar.monthrange(current_date.year, previous_month_number)[1]
