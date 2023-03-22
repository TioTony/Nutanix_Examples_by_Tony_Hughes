"""
03/16/2023 TH: Initiate a recovery plan
"""
import datetime
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
    #env_path = Path(".") / ".env"
    #load_dotenv(dotenv_path=env_path)
    #PC_IP = os.getenv("PC_IP")
    #PC_PORT = os.getenv("PC_PORT")
    #PC_USERNAME = os.getenv("PC_USERNAME")
    #PC_PASSWORD = os.getenv("PC_PASSWORD")
    #CLUSTER_IP = os.getenv("CLUSTER_IP")
    #CLUSTER_PORT = os.getenv("CLUSTER_PORT")
    #CLUSTER_USERNAME = os.getenv("CLUSTER_USERNAME")
    #CLUSTER_PASSWORD = os.getenv("CLUSTER_PASSWORD")

    PC_IP = "10.42.10.39"
    PC_PORT = "9440"
    PC_USERNAME = "admin"
    PC_PASSWORD = "nx2Tech714!"

    # Set the time this is being executed
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M%S2Z')

    # don't worry about invalid certs
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # setup the API request
    endpoint = f"https://{PC_IP}:{PC_PORT}/api/nutanix/v3/recovery_plan_jobs"
    request_headers = {"Content-Type": "application/json", "charset": "utf-8"}
    # To find the contents for the request_body I manually ran a failover from the GUI
    # and then use the recover_plan_jobs/list API to output the job details which I then
    # picked through and grabbed the pieces I needed.
    request_body = {
        "spec": {
            "name": "CCLM",
            "resources": {
                "recovery_plan_reference": {
                    "kind": "recovery_plan",
                    "name": "CCLM",
                    "uuid": "7f35a247-7c66-470b-ac3e-9351421bd8ec"
                },
                "execution_parameters": {
                    "recovery_availability_zone_list": [
                        {
                            "cluster_reference_list": [
                                {
                                    "kind": "cluster",
                                    "uuid": "0005f703-26db-d4bd-0000-00000000d1a8"
                                }
                            ],
                            "availability_zone_url": "824f0517-8b64-40e8-a5aa-ef756be0f81d"
                        }
                    ],
                    "failed_availability_zone_list": [
                        {
                            "cluster_reference_list": [
                                {
                                    "kind": "cluster",
                                    "uuid": "0005f703-2cc5-a99e-0000-00000000d16a"
                                }
                            ],
                            "availability_zone_url": "824f0517-8b64-40e8-a5aa-ef756be0f81d"
                        }
                    ],
                    "action_type": "LIVE_MIGRATE",
                    "should_continue_on_validation_failure": True
                }
            }
        },
        "metadata": {
            "kind": "recovery_plan_job"
            },
    }

    # Submit the requests and get the output
    try:
        results = requests.post(
            endpoint,
            data=json.dumps(request_body),
            headers=request_headers,
            verify=False,
            auth=HTTPBasicAuth(PC_USERNAME, PC_PASSWORD),
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
