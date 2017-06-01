import requests
import json


def get_version(message):
    """
    Modify these please
    """
    host = message.text.split()[-1]
    url='http://{}/ins'.format(host)
    switchuser='CHANGEME'
    switchpassword='CHANGEME'

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
    response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()

    resp = response['ins_api']['outputs']['output']['body']['kickstart_ver_str']
    return "this switch is running version {}".format(resp)
