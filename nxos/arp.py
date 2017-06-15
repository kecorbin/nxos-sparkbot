import requests
import json
import os

nxos_username = os.getenv("NXOS_LOGIN")
nxos_password = os.getenv("NXOS_PASSWORD")


def get_arp_entry(switch, ip):
    """
    Returns mac address for IP or None
    """
    url='http://{}/ins'.format(switch)
    switchuser=nxos_username
    switchpassword=nxos_password
    myheaders = {'content-type': 'application/json'}
    payload={
      "ins_api": {
        "version": "1.0",
        "type": "cli_show",
        "chunk": "0",
        "sid": "1",
        "input": "show ip arp {}".format(ip),
        "output_format": "json"
      }
    }

    try:
        response_from_switch = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(switchuser, switchpassword)).json()
        mac = response_from_switch['ins_api']['outputs']['output']['body']['TABLE_vrf']['ROW_vrf']['TABLE_adj']['ROW_adj']['mac']
        return mac
    except:
        return None


def get_arp_table(host):
    url = 'http://{}/ins'.format(host)
    switchuser = nxos_username
    switchpassword = nxos_password

    myheaders = {'content-type': 'application/json-rpc'}
    payload = [
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "show ip arp",
          "version": 1
        },
        "id": 1
      }
    ]
    response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(switchuser, switchpassword)).json()

    # we will either have nothing, a list or a dictionary
    # check for nothing, return no apr entries exist
    try:
        arplist = response['result']['body']['TABLE_vrf']['ROW_vrf']['TABLE_adj']['ROW_adj']
        return arplist
    except KeyError:
        return None
