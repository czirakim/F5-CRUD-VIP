"""
delete profiles
"""

import requests
import os
import json
import urllib3
from logger import logger
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logger()

# F5 device
IP_ADDRESS = "192.168.88.100"


def delete_profile():
    API_string = os.environ.get('Authorization_string')
    base_url = f"https://{IP_ADDRESS}/mgmt/tm/ltm/profile/"
    headers = {
        'Authorization': f'Basic {API_string}',
        'Content-Type': 'application/json'
             }

    # Open the file for reading
    with open('profiles.json', 'r') as file:
        # Read the contents of the file
        data = file.read()

    # Parse the JSON data
    items = json.loads(data)

    # make the request and log the response
    for item in items:
        profiles = item['profiles']
        type = item['type']
        for profile in profiles:
            try:
                response = requests.request("DELETE", f"{base_url}{type}/{profile['name']}", headers=headers, verify=False)
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                if (response.status_code == 404 or response.status_code == 400):
                    logger.error(f"An error occurred while making the request:  {response.text}")
            except requests.exceptions.RequestException as e:
                logger.error(f"An error occurred while making the request: {e}")
            else:
                logger.info(f"Profile {profile['name']} has been DELETED. ")


if __name__ == "__main__":
    delete_profile()
