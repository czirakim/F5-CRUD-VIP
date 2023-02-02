import requests
import os
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


"""
Create pool
"""


def create_pool(logger):

    API_string = os.environ.get('Authorization_string')
    url = "https://192.168.88.100/mgmt/tm/ltm/pool"
    headers = {
        'Authorization': f'Basic {API_string}',
        'Content-Type': 'application/json'
             }

    # Open the file for reading
    with open('pool.json', 'r') as file:
        # Read the contents of the file
        data = file.read()

    # Parse the JSON data
    items = json.loads(data)

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
                logger.error(f"Pool {item['name']} already exists so we can't override it.")
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred while making the request: {e}")
        else:
            logger.info(f"Pool {item['name']} with nodes: {node_list} has been created.")
