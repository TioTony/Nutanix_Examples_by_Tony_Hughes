"""
Shutdown a single VM Prism Central.  This will not stop scale-out Prism Central.
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
    # Set variables
    # IP Address for a CVM or the Prism Element Cluster VIP
    CLUSTER_IP = "10.0.0.133"
    # Cluster port
    CLUSTER_PORT = "9440"
    # Prism Element Local Admin account
    CLUSTER_USERNAME = "admin"
    # Prism Element Admin Password.  I realise this is my password, but it is on a segmented network in my home lab.
    CLUSTER_PASSWORD = "nx2Tech1242!"

    # don't worry about invalid certs
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # setup the API request
    # This is API endpoint to change the powerstate of a VM to "ACPI_SHUTDOWN" which should gracefully
    # shutdown and power-off the Prism Central..
    # Update the UUID to the proper value for the Prism Central VM
    # The UUID can be found by using the 100 Level Prism_Element_v2_GET_vms-no_parameters.py
    # The output may be long, you are looking for something like this. note the UUID entry:
    """
    {
            "allow_live_migrate": true,
            "description": "NutanixPrismCentral",
            "gpus_assigned": false,
            "ha_priority": 0,
            "machine_type": "pc",
            "memory_mb": 31744,
            "name": "PrismCentral",
            "num_cores_per_vcpu": 1,
            "num_vcpus": 6,
            "power_state": "off",
            "timezone": "UTC",
            "uuid": "f70018b1-794e-42f6-aa39-0f9048ee335c",
            "vm_features": {
                "AGENT_VM": false,
                "VGA_CONSOLE": true
            },
    """
    endpoint = f"https://{CLUSTER_IP}:{CLUSTER_PORT}/PrismGateway/services/rest/v2.0/vms/f70018b1-794e-42f6-aa39-0f9048ee335c/set_power_state"
    request_headers = {"Content-Type": "application/json", "charset": "utf-8"}
    # Power off Prism Central
    request_body = {"transition": "ACPI_SHUTDOWN"}

    # Submit the requests and get the output
    try:
        results = requests.post(
            endpoint,
            data=json.dumps(request_body),
            headers=request_headers,
            verify=False,
            auth=HTTPBasicAuth(CLUSTER_USERNAME, CLUSTER_PASSWORD),
        )

        # Print the results of the request
        # It should be a task_uuid for the request to power off the Prism Central VM
        print(json.dumps(results.json(), indent=4, sort_keys=True))

    # Print Errors if any are present
    except Exception as error:
        print(f"ERROR: {error}")
        print(f"Exception: {error.__class__.__name__}")
        sys.exit()


if __name__ == "__main__":
    main()
