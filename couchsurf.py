import json
import requests

from dotenv import dotenv_values

CONFIG = dotenv_values('.env')

HEADERS = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'referer': f'https://{CONFIG["GOVERNOR_HOST"]}'
}

def get_request(view_path="latest-poll",**kwargs):
    response = requests.get(
        f'https://{CONFIG["GOVERNOR_URI"]}/_design/latest/_view/{view_path}',
        headers=HEADERS,
        params=json.dumps({
            "keys":[value for value in kwargs.values()]
        })
    )
    return response.text

def post_request(doc):
    response = requests.post(
        f'https://{CONFIG["GOVERNOR_URI"]}',
        headers=HEADERS,
        data=json.dumps(doc)
    )
    confirmation = json.loads(response.text)
    print(f'A new doc has been posted at id: {confirmation["id"]}')