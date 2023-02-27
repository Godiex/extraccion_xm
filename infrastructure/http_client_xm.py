import os
import requests
import json

from requests import Response


class HttpClientXm:
    """
        permite la creacion de un cliente para consumir archivos de la api publica de XM
    """

    def __init__(self):
        self.BASE_URL = os.environ["BASE_URL"]

    def get(self, complementary_base_url: str) -> Response:
        url_request = self.BASE_URL.format(complementary_base_url=complementary_base_url)
        response = requests.get(url_request)
        file_url = json.loads(response.text)
        return requests.get(file_url["url"])
