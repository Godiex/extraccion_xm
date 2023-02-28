import os

from pandas import DataFrame
from core.enums import FileName, Folder
from core.helper import generate_file_name


class FileRepository:
    """
        permite la creacion de un cliente para consumir archivos de la api publica de XM
    """

    def __init__(self) -> None:
        self.__PATH_DOWNLOAD = os.environ["PATH_DOWNLOAD"]

    def save(self, data: DataFrame, folder_name: Folder, file_name: FileName) -> None:
        file_name = generate_file_name(file_name.value)
        file_name = f"{file_name}.csv"
        target_path = self.__PATH_DOWNLOAD.format(complementary_url=folder_name.value, file_name=file_name)
        self.create_folder(target_path)
        data.to_csv(target_path)

    @staticmethod
    def create_folder(path: str) -> None:
        if not os.path.exists(path):
            os.mkdir(path)
