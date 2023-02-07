"""
Create profiles
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


def create_profile():
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
            payload = json.dumps(profile)
            try:
                response = requests.request("POST", f"{base_url}{type}", headers=headers, data=payload, verify=False)
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                if (response.status_code == 409):
                    logger.error(f"Profile {profile['name']} already exists so we can't override it. ### Use modify* scripts. ### ")
            except requests.exceptions.RequestException as e:
                logger.error(f"An error occurred while making the request: {e}")
            else:
                logger.info(f"Profile {profile['name']} has been created. ")


if __name__ == "__main__":
    create_profile()
