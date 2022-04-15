"""
02/26/2022 TH: Get disk info from PE
"""
import json
import os
import sys
from pathlib import Path

import requests
import urllib3
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth


def main():
    # load the script configuration
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)
    PC_IP = os.getenv("PC_IP")
    PC_PORT = os.getenv("PC_PORT")
    PC_USERNAME = os.getenv("PC_USERNAME")
    PC_PASSWORD = os.getenv("PC_PASSWORD")
    # West Coast HPOC
    CLUSTER_IP = "10.42.42.37"
    CLUSTER_PORT = "9440"
    CLUSTER_USERNAME = "admin"
    CLUSTER_PASSWORD = "nx2Tech254!"

    # don't worry about invalid certs
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # setup the API request
    endpoint = f"https://10.42.42.37:9440/PrismGateway/services/rest/v1/clusters?proxyClusterUuid=0005d9e3-c441-b3e0-6ddb-3cecef852de8&page=1&count=1&__=1649980258010"
    request_headers = {"Content-Type": "application/json", "charset": "utf-8"}
    request_body = {}

    # Submit the requests and get the output
    try:
        results = requests.get(
            endpoint,
            data=json.dumps(request_body),
            headers=request_headers,
            verify=False,
            auth=HTTPBasicAuth(CLUSTER_USERNAME, CLUSTER_PASSWORD),
        )

        # check the results of the request
        # if results.status_code == 200 or results.status_code == 201:
        print(json.dumps(results.json(), indent=4, sort_keys=True))

    except Exception as error:
        print(f"ERROR: {error}")
        print(f"Exception: {error.__class__.__name__}")
        sys.exit()


if __name__ == "__main__":
    main()
