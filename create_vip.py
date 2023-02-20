"""
Create Virtual Server

"""


import requests
import os
import sys
import json
import urllib3
from create_pool import create_pool
from create_irules import create_irule
from create_profiles import create_profile
from logger import logger
import logging
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
data_file = f"{path}/virtual.json"


def create_vip():

    API_string = os.environ.get('Authorization_string')
    url = f"https://{IP_ADDRESS}/mgmt/tm/ltm/virtual"
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
        pool = item['pool']
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if (response.status_code == 409):
                logg.error(f"Virtual Server {item['name']} already exists so we can't override it. ### Use modify* scripts. ###")
            elif (response.status_code == 404 or response.status_code == 400):
                logg.error(f"There is a missing object that you need to configure first. {response.text}")
        except requests.exceptions.RequestException as e:
            logg.error(f"An error occurred while making the request: {e}")
        else:
            logg.info(f"Virtual Server {item['name']} --> {pool} has been created.")


if __name__ == "__main__":
    create_pool()
    create_profile()
    create_irule()
    create_vip()
#    import ipdb
#    ipdb.set_trace()
