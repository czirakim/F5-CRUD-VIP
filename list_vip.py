"""
List Virtual Server
"""

import requests
import os
import sys
import json
import urllib3
from logger import logger
import logging
from rich import print_json, print
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# create a logger
logg = logging.getLogger(__name__)
logg.setLevel(logging.INFO)
# add the handler to the logger
logg.addHandler(logger())

# F5 device
IP_ADDRESS = os.environ.get('IP_ADDRESS')

# Get the current working directory and build the path for teh json file
cwd = os.getcwd()
path = f"{cwd}/{sys.argv[1]}"
data_file = f"{path}/virtual.json"


def list_vip():

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
        try:
            response = requests.request("GET", url, headers=headers, verify=False)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if (response.status_code == 404 or response.status_code == 400):
                logg.error(f"An error occurred while making the request:  {response.text}")
        except requests.exceptions.RequestException as e:
            logg.error(f"An error occurred while making the request: {e}")
        else:
            print(f"[yellow bold]\n Virtual Server name: {vip_name}[/yellow bold]")
            print_json(response.text)


if __name__ == "__main__":
    list_vip()
