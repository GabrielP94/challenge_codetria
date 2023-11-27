import json

import requests

URL = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"


def get_currencies_values(dollar_name=None):
    payload = {}
    headers = {}

    response = requests.request("GET", URL, headers=headers, data=payload)
    if not dollar_name:
        return json.loads(response.text)
    else:
        dollar_list = json.loads(response.text)
        res = next((sub for sub in dollar_list if sub['casa']['nombre'] == dollar_name), None)
        return res
