"""
02/26/2022 TH: Get disk info from PE
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

    # don't worry about invalid certs
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # setup the API request
    endpoint = f"https://{CLUSTER_IP}:{CLUSTER_PORT}/PrismGateway/services/rest/v2.0/hosts/ad3d5637-690b-4693-af55-31dd18fc0b77/"
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
