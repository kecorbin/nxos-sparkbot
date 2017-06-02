import requests
import json


def get_version(ip, user, passwd):
    """
    Get the NX-OS version from a switch
    """
    url='http://{}/ins'.format(ip)
    switchuser=user
    switchpassword=passwd

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
    response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword))
    resp = response.json()['ins_api']['outputs']['output']['body']['kickstart_ver_str']
    return resp
