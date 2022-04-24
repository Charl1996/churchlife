import requests
import json


def post_request(url, data, headers):
    response = requests.post(
        url,
        data=json.dumps(data),
        headers=headers,
    )
    content = json.loads(response.content)

    errors = []
    if isinstance(content, dict):
        errors = content.get('errors', '')

    return response.status_code, content, errors


def get_request(url, headers):
    response = requests.get(
        url,
        headers=headers,
    )
    content = json.loads(response.content)

    errors = []
    if isinstance(content, dict):
        errors = content.get('errors', '')

    return response.status_code, content, errors
