import os
from pandas import DataFrame
import json

from requests import Response


class FileRepository:
    """
        permite la creacion de un cliente para consumir archivos de la api publica de XM
    """

    def __init__(self):
        self.PATH_DOWNLOAD = os.environ["PATH_DOWNLOAD"]

    def save(self, data: DataFrame, ):
        pass
