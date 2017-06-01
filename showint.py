import requests
import json

def getint(portnum):
    url='http://10.10.20.58/ins'
    switchuser='admin'
    switchpassword='cisco123'
    portnum = str(portnum)
    portnum = 'eth1/1'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
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
    portdetails = response['result']['body']['TABLE_interface']['ROW_interface']


    state = portdetails['admin_state'] + '/' + portdetails['state']
    desc = portdetails['desc']
    mode = portdetails['eth_mode']
    speed = portdetails['eth_speed']
    mtu = portdetails['eth_mtu']
    mac = portdetails['eth_hw_addr']

    return 'The state for port **' + portnum + '** is **' + state + '**!  Its description is **' + desc + \
           '** and is currently enabled as a **' + mode + '** port running at **' + speed + '**'

#print getint('eth1/1')
