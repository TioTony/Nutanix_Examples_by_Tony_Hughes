# Tony's Nutanix Samples

NOTE from 12/28/2022 - This project is continually in a state of change and refactoring.  Use it if you like and feel free to open bugs against it."

The origin of this project was twofold.  First I wanted to script a mechanism for starting Nutanix clusters from a cold stated and also stopping a cluster and returning it to a cold state in my home lab simply as a time saving measure.  Second, I wanted to start exploring what else I could automate.  I started by simply exploring the v2 and v3 APIs with atomic calls to gain an understanding of how they work and what features may be available.  

I plan to continue adding other content that seems relevant as I explore my own use cases.

## Environment Details

- My environment consists of PyCharm Community Edition running on an Ubuntu 20.04 VM.  I patch it on a regular basis.
- The requirements.txt file should have all the related python requirements.  
- I used python 3.7 and 3.8 to create these scripts.
- I used pip3 for python package management
- Update the  `.env` file with the correct info.

## General Usage Information
- I have done my best to document each file
- Folders should contain the bulk of anything they need.  For example, something in the 100 level folder shouldn't be calling anything in the 200 level folder and vice versa.
- I may leave some common use files in the root folder
- For everything else you are on your own.

Current
- 100 - API Examples
  - These examples are meant to be atomic calls to a single API to demonstrate usage and output.  
- WIP - Work In Progress
  - Anything in here is not currently working or may not be finalized but I am sharing under the assumption something is better than nothing if you are looking for examples.
  - This folder may also contain things that I have yet to find a home for.
Future
- Ansible
- Terraform
- Calm
- Playbooks
- Hands on Lab Workflows
- 200 - Basic operations
- 300 - Complex operations
- 400 - Full deployments
