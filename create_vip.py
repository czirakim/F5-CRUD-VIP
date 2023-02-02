import requests
from rich import print
import os
import json
from create_pool import create_pool
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


"""
Create Virtual Server
"""


def create_vip():

    API_string = os.environ.get('Authorization_string')
    url = "https://192.168.88.100/mgmt/tm/ltm/virtual"
    headers = {
        'Authorization': f'Basic {API_string}',
        'Content-Type': 'application/json'
             }

    # Open the file for reading
    with open('virtual.json', 'r') as file:
        # Read the contents of the file
        data = file.read()

    # Parse the JSON data
    items = json.loads(data)
    for item in items:
        print(item)
        payload = json.dumps(item)
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        response.raise_for_status()


if __name__ == "__main__":
    create_pool()
#    create_vip()
#    import ipdb
#    ipdb.set_trace()
