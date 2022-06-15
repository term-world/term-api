import re
import json
import requests

from dotenv import dotenv_values

CONFIG = dotenv_values('.env')

HEADERS = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'referer': f'https://{CONFIG["GOVERNOR_HOST"]}'
}

def get_request(view_path="latest-poll", **kwargs):
    params = None
    if kwargs:
        params = {
            "keys": json.dumps([value for value in kwargs.values()])
        }
    response = requests.get(
        f'https://{CONFIG["GOVERNOR_URI"]}/_design/latest/_view/{view_path}',
        headers = HEADERS,
        params = params
    )
    return response.text

def query_request(**kwargs):
    query = {
        "selector":{
            "user": {
                "$regex":",".join([re.escape(value) for value in kwargs.values()])
            }
        }
    }
    result = post_request(query, "_find")
    return result

def post_request(doc, op=""):
    response = requests.post(
        f'https://{CONFIG["GOVERNOR_URI"]}/{op}',
        headers=HEADERS,
        data=json.dumps(doc)
    )
    confirmation = json.loads(response.text)
    return confirmation

def put_request(doc_id, updated_doc):
    response = requests.put(
        f'https://{CONFIG["GOVERNOR_URI"]}/{doc_id}',
        headers=HEADERS,
        data=json.dumps(updated_doc)
    )
    confirmation = json.loads(response.text)
    return confirmation