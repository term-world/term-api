import json
import requests

from dotenv import dotenv_values

CONFIG = dotenv_values('.env')

HEADERS = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'referer': 'https://fauxton.cdr.theterm.world'
}

def get_request(view_path="/_design/latest/_view/latest-poll"):
    response = requests.get(f'https://{CONFIG["GOVERNOR_URI"]}{view_path}',
    headers=HEADERS,
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