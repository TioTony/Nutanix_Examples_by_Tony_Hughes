"""
Nutanix Prism VM Stats
"""

import requests
import urllib3
import json
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from requests.auth import HTTPBasicAuth


def main():
    """
    main entry point into the 'app'
    every function needs a Docstring in order to follow best
    practices
    """
    # load the script configuration
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)
    PC_IP = os.getenv("PC_IP")
    PC_PORT = os.getenv("PC_PORT")
    PC_USERNAME = os.getenv("PC_USERNAME")
    PC_PASSWORD = os.getenv("PC_PASSWORD")
    CLUSTER_IP = os.getenv("CLUSTER_IP")
    CLUSTER_PORT = os.getenv("CLUSTER_PORT")
    CLUSTER_USERNAME = os.getenv("CLUSTER_USERNAME")
    CLUSTER_PASSWORD = os.getenv("CLUSTER_PASSWORD")

    print(f"Cluster IP: {CLUSTER_IP}")
    print(f"Cluster Port: {CLUSTER_PORT}")
    print(f"Prism Central IP: {PC_IP}")
    print(f"Prism Central Port: {PC_PORT}")

    """
    disable insecure connection warnings
    please be advised and aware of the implications of doing this
    in a production environment!
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # setup a variable that can be used to store our JSON configuration
    raw_json = {}

    # grab and decode the category details from the included JSON file
    with open("./config.json", "r") as f:
        raw_json = json.loads(f.read())

    # setup the request that will get the VM list
    print("\nGathering disk list ...")
    endpoint = f"https://{CLUSTER_IP}:{CLUSTER_PORT}/PrismGateway/services/rest/v2.0/disks/"
    request_headers = {"Content-Type": "application/json", "charset": "utf-8"}
    # this request body instructs the v3 API to return the first available VM only
    # request_body = {"kind": "vm", "length": 1}
    request_body = {}
    print("\nFinished gathering disk list ...")

    # submit the request that will gather the VM list
    try:
        results = requests.get(
            endpoint,
            data=json.dumps(request_body),
            headers=request_headers,
            verify=False,
            auth=HTTPBasicAuth(CLUSTER_USERNAME, CLUSTER_PASSWORD),
        )

        # check the results of the request
        if results.status_code == 200 or results.status_code == 201:
            print("Request successful, disk info ...")

        print(json.dumps(results.json(), indent=4, sort_keys=True))

    except Exception as error:
        print(f"An unhandled exception has occurred: {error}")
        print(f"Exception: {error.__class__.__name__}")
        sys.exit()


if __name__ == "__main__":
    main()
