import requests
import json
import os

"""
Modify these please
"""


def get_iparp(message):
    host = message.text.split()[-1]
    url = 'http://{}/ins'.format(host)
    switchuser = os.getenv('NXOS_LOGIN')
    switchpassword = os.getenv('NXOS_PASSWORD')

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

    except KeyError:
        arplist = []

    if len(arplist) == 0:
        response2spark = "# sorry...no arp entries exist!"

    elif isinstance(arplist,dict):
        # check for dictionary, handle single ARP entry
        response2spark = "# here is your arp table...\n"
        arp = arplist
        mac = (arp['mac'])
        ipaddr = (arp['ip-addr-out'])
        arpresult = "* Mac Address = {}, IP Address = {}, \n".format(mac, ipaddr)
        response2spark = response2spark + arpresult
    else:
        # check for list, meaning multiple arp entries

        response2spark = "# here is your arp table...\n"
        for arp in arplist:
            mac = (arp['mac'])
            ipaddr = (arp['ip-addr-out'])
            arpresult = "* Mac Address = {}, IP Address = {}, \n".format(mac, ipaddr)
            response2spark = response2spark + arpresult
    return response2spark
