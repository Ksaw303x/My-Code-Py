import json
import requests
from requests.auth import HTTPBasicAuth

from credit_shield.pack.api.exceptions import NetworkError


class CreditShield:

    def __init__(self):
        self.auth = ''

    def login(self, username, password):
        self.auth = HTTPBasicAuth(username, password)

    def get(self):
        uri = 'https://api-test.itfinance.it/IT4FRest/rest/itf/account/v1/partner'
        res = requests.get(uri, auth=self.auth)
        if res.ok:
            return json.loads(res.content)
        else:
            raise NetworkError
