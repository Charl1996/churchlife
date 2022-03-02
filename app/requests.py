import requests
import json


def post_request(url, data, headers):
    return requests(
        url,
        data=json.dumps(data),
        headers=headers,
    )
