import requests
import json
import os

nxos_username = os.getenv("NXOS_LOGIN")
nxos_password = os.getenv("NXOS_PASSWORD")

def find_mac(ip, mac):
    """
    Returns (vlan,interface) or None
    """
    url='http://{}/ins'.format(ip)
    switchuser=nxos_username
    switchpassword=nxos_password

    myheaders={'content-type':'application/json'}
    payload={
      "ins_api": {
        "version": "1.0",
        "type": "cli_show",
        "chunk": "0",
        "sid": "1",
        "input": "show mac address-table address {}".format(mac),
        "output_format": "json"
      }
    }

    try:
        response_from_switch = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
        vlan = response_from_switch['ins_api']['outputs']['output']['body']['TABLE_mac_address']['ROW_mac_address']['disp_vlan']
        interface = response_from_switch['ins_api']['outputs']['output']['body']['TABLE_mac_address']['ROW_mac_address']['disp_port']
        return (vlan, interface)
    except:
        return None
