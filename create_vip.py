"""
Create Virtual Server
"""


import requests
import os
import json
from create_pool import create_pool
import urllib3
from logger import logger
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logger()


IP_ADDRESS = "192.168.88.100"


def create_vip():

    API_string = os.environ.get('Authorization_string')
    url = f"https://{IP_ADDRESS}/mgmt/tm/ltm/virtual"
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
        payload = json.dumps(item)
        pool = item['pool']
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if (response.status_code == 409):
                logger.error(f"Virtual Server {item['name']} already exists so we can't override it. ### Use modify* scripts. ###")
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred while making the request: {e}")
        else:
            logger.info(f"Virtual Server {item['name']} --> {pool} has been created.")


if __name__ == "__main__":
    create_pool(logger, IP_ADDRESS)
    create_vip()
#    import ipdb
#    ipdb.set_trace()
