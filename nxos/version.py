import requests
import json
import os

nxos_username = os.getenv("NXOS_LOGIN")
nxos_password = os.getenv("NXOS_PASSWORD")

def get_version(ip):
    """
    Get the NX-OS version from a switch
    """
    url='http://{}/ins'.format(ip)

    myheaders={'content-type':'application/json'}
    payload={
      "ins_api": {
        "version": "1.0",
        "type": "cli_show",
        "chunk": "0",
        "sid": "1",
        "input": "show version",
        "output_format": "json"
      }
    }
    response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(nxos_username,nxos_password))
    resp = response.json()['ins_api']['outputs']['output']['body']['kickstart_ver_str']
    return resp
