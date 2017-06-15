import requests
import json
import os

nxos_username = os.getenv("NXOS_LOGIN")
nxos_password = os.getenv("NXOS_PASSWORD")

def getint(ip, portnum):
    """
    Get the show interface details for a port.
    """
    url = 'http://{}/ins'.format(ip)
    switchuser = nxos_username
    switchpassword = nxos_password
    portnum = str(portnum)

    myheaders = {'content-type':'application/json-rpc'}
    payload = [
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "show int " + portnum,
          "version": 1
        },
        "id": 1
      }
    ]
    response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()

    try:
        portdetails = response['result']['body']['TABLE_interface']['ROW_interface']
    except KeyError, e:
        return 'Something went Wrong. Are you sure you typed the correct interface name?'
    state = portdetails['admin_state'] + '/' + portdetails['state']
    try:
        desc = portdetails['desc']
    except KeyError, e:
        desc = "undefined"
        pass
    mode = portdetails['eth_mode']
    speed = portdetails['eth_speed']
    mtu = portdetails['eth_mtu']
    mac = portdetails['eth_hw_addr']

    return 'The state for port **' + portnum + '** is **' + state + '**!  Its description is **' + desc + \
           '**. It is currently enabled as a **' + mode + '** port running at **' + speed + '**' + \
           ' and MTU is set at **' + mtu + '**'
