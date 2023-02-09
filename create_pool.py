"""
Create pool
"""

import requests
import os
import sys
import json
from logger import logger
import logging
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# create a logger
logg = logging.getLogger(__name__)
logg.setLevel(logging.INFO)
# add the handler to the logger
logg.addHandler(logger())

# F5 device
IP_ADDRESS = "192.168.88.100"

# Get the current working directory and build the path for teh json file
cwd = os.getcwd()
path = f"{cwd}/{sys.argv[1]}"
data_file = f"{path}/pool.json"


def create_pool():

    API_string = os.environ.get('Authorization_string')
    url = f"https://{IP_ADDRESS}/mgmt/tm/ltm/pool"
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
        payload = json.dumps(item)
        nodes = item['members']
        node_list = []
        for n in nodes:
            node_list.append(n['name'])
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if (response.status_code == 409):
                logg.error(f"Pool {item['name']} already exists so we can't override it. ### Use modify* scripts. ###")
            elif (response.status_code == 404 or response.status_code == 400):
                logg.error(f"There is a missing object that you need to configure first. {response.text}")
        except requests.exceptions.RequestException as e:
            logg.error(f"An error occurred while making the request: {e}")
        else:
            logg.info(f"Pool {item['name']} with nodes: {node_list} has been created.")


if __name__ == "__main__":
    create_pool()
