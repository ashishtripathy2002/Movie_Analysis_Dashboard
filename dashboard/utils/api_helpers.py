import requests
from utils.auth_storage import get_auth_headers

def make_api_request(url, method="GET", data=None):
    headers = get_auth_headers()
    if method == "GET":
        return requests.get(url, headers=headers)

    elif method == "POST":
        return requests.post(url, json=data, headers=headers)

    elif method == "PUT":
        print(data)
        return requests.put(url, json=data, headers=headers)

    elif method == "DELETE":
        return requests.delete(url, headers=headers)
