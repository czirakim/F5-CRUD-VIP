"""
Create profiles
"""

import requests
import os
import sys
import json
import urllib3
from logger import logger
import logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# create a logger
logg = logging.getLogger(__name__)
logg.setLevel(logging.INFO)
# add the handler to the logger
logg.addHandler(logger())


# F5 device
IP_ADDRESS = os.environ.get('IP_ADDRESS')

# Get the current working directory and build the path for the json file
cwd = os.getcwd()
path = f"{cwd}/{sys.argv[1]}"
data_file = f"{path}/profiles.json"


def create_profile():
    API_string = os.environ.get('Authorization_string')
    base_url = f"https://{IP_ADDRESS}/mgmt/tm/ltm/profile/"
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
        profiles = item['profiles']
        type = item['type']
        for profile in profiles:
            payload = json.dumps(profile)
            try:
                response = requests.post(f"{base_url}{type}", headers=headers, data=payload, verify=False)
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                if (response.status_code == 409):
                    logg.error(f"Profile {profile['name']} already exists so we can't override it. ### Use modify* scripts. ### ")
                elif (response.status_code == 404 or response.status_code == 400):
                    logg.error(f"There is a missing object that you need to configure first. {response.text}")
            except requests.exceptions.RequestException as e:
                logg.error(f"An error occurred while making the request: {e}")
            else:
                logg.info(f"Profile {profile['name']} has been created. ")


if __name__ == "__main__":
    create_profile()
