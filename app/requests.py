import requests
import json


def post_request(url, data, headers):
    response = requests.post(
        url,
        data=json.dumps(data),
        headers=headers,
    )
    return response.status_code, json.loads(response.content)


def get_request(url, headers):
    response = requests.get(
        url,
        headers=headers,
    )
    return response.status_code, json.loads(response.content)
