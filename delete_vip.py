"""
Delete Virtual Server
"""

import requests
import os
import json
import urllib3
from logger import logger
from delete_pool import delete_pool
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logger()


def delete_vip(logger):

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
        payload = json.dumps(item)
        vip_name = item['name']
        url = f"https://192.168.88.100/mgmt/tm/ltm/virtual/{vip_name}"
        try:
            response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if (response.status_code == 404 or response.status_code == 400):
                logger.error(f"An error occurred while making the request:  {response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred while making the request: {e}")
        else:
            logger.info(f"Virtual Server {item['name']} has been DELETED.")


if __name__ == "__main__":
    delete_vip(logger)
    delete_pool(logger)
