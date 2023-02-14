import unittest
import requests
import os
import sys
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_http_response():

    # F5 device
    IP_ADDRESS = "192.168.88.100"

    # Get the current working directory and build the path for teh json file
    cwd = os.getcwd()
    path = f"{cwd}/{sys.argv[1]}"
    data_file = f"{path}/virtual.json"

    API_string = os.environ.get('Authorization_string')

    headers = {
        'Authorization': f'Basic {API_string}',
        'Content-Type': 'application/json'
            }

    # Open the file for reading
    with open(f'{data_file}', 'r') as file:
    # Read the contents of the file
        data = file.read()

    # Parse the JSON data
    items = json.loads(data)

    # make the request and log the response
    for item in items:
        vip_name = item['name']
        url = f"https://{IP_ADDRESS}/mgmt/tm/ltm/virtual/{vip_name}"
        response = requests.get(url, headers=headers, verify=False)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"


if __name__ == '__main__':
    test_http_response()
