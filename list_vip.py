"""
List Virtual Server
"""

import requests
import os
import json
import urllib3
from logger import logger
from rich import print_json, print
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logger()

IP_ADDRESS = "192.168.88.100"


def list_vip():

    API_string = os.environ.get('Authorization_string')

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

    # make the request and log the response
    for item in items:
        vip_name = item['name']
        url = f"https://{IP_ADDRESS}/mgmt/tm/ltm/virtual/{vip_name}"
        try:
            response = requests.request("GET", url, headers=headers, verify=False)
            response.raise_for_status()
            reply = json.dumps(json.loads(response.text), indent=4)
        except requests.exceptions.HTTPError:
            if (response.status_code == 404 or response.status_code == 400):
                logger.error(f"An error occurred while making the request:  {response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred while making the request: {e}")
        else:
            print(f"[yellow bold]\n Pool name: {vip_name}[/yellow bold]")
            print_json(response.text)


if __name__ == "__main__":
    list_vip()
