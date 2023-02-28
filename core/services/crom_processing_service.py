import tempfile
from datetime import date

import pandas as pd
from pandas import DataFrame
from requests import Response

from core.helper import generate_file_name, get_previous_month_number
from core.enums import FileName, Folder
from infrastructure import HttpClientXm
from infrastructure import FileRepository


class CromProcessingService:
    __PERIOD_NUMBER = 60
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
    __FILE_TEMPORARY_NAME = "CROM"
    __temporary_directory = str
    __temp_folder: {}

    def __init__(self, http_client_xm: HttpClientXm, file_repository: FileRepository) -> None:
        self.http_client_xm = http_client_xm
        self.file_repository = file_repository

    def process_crom(self) -> None:
        xm_response = self.get()
        self.save_temporary_crom(xm_response.content)
        crom_1, crom_2 = self.adjust_crom()
        self.file_repository.save(data=crom_1, folder_name=Folder.CROM, file_name=FileName.CROM1)
        self.file_repository.save(data=crom_2, folder_name=Folder.CROM, file_name=FileName.CROM2)

    def get(self) -> Response:
        year = date.today().year
        previos_mounth = get_previous_month_number()
        month_info = self.__MONTHS[str(previos_mounth)]
        complementary_url = self.__COMPLEMENTARY_BASE_URL.format(
            year=year,
            month_number=month_info["month_number"],
            diminutive_month_name=month_info["diminutive_month_name"],
            month_name=month_info["month_name"]
        )
        return self.http_client_xm.get(complementary_base_url=complementary_url)

    def save_temporary_crom(self, file_xm: bytes) -> None:
        file_name = generate_file_name(self.__FILE_TEMPORARY_NAME)
        self.__temp_folder = tempfile.TemporaryDirectory()
        self.__temporary_directory = self.__temp_folder.name
        with open(f"{self.__temporary_directory}\\{file_name}.xls", 'wb') as file:
            file.write(file_xm)

    def adjust_crom(self) -> tuple[DataFrame, DataFrame]:
        file_name = generate_file_name(self.__FILE_TEMPORARY_NAME)
        crom_path = f"{self.__temporary_directory}\\{file_name}.xls"
        crom_1 = pd.read_excel(crom_path, sheet_name="CROM 1")
        crom_2 = pd.read_excel(crom_path, sheet_name="CROM 2")
        self.adjust_data(crom_1, '1')
        self.adjust_data(crom_2, '2')
        return crom_1, crom_2

    def adjust_data(self, crom: DataFrame, crom_number: str):
        crom.drop(index=[0, 1], axis=0, inplace=True)
        crom.drop(['Unnamed: 0', f'Publicación Definitiva CROM{crom_number}'], axis=1, inplace=True)
        columns = ['Agente', 'Sigla', 'No SUI']
        for i in range(1, self.__PERIOD_NUMBER + 1):
            columns.append(f'P{i}')
        crom.columns = columns
