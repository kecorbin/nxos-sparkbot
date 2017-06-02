import requests
import json

def getint(portnum):
    url='http://ENTERIP/ins'
    switchuser='admin'
    switchpassword='cisco'
    portnum = str(portnum)
    #portnum = 'eth1/1'
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

    try:
        portdetails = response['result']['body']['TABLE_interface']['ROW_interface']
    except KeyError, e:
        print 'KEY ERROR - %s' %str(e)
        return 'Something went Wrong. Are you sure you typed the correct interface name? \
         For example: **@nxosbot port Eth1/1**'


    state = portdetails['admin_state'] + '/' + portdetails['state']
    desc = portdetails['desc']
    mode = portdetails['eth_mode']
    speed = portdetails['eth_speed']
    mtu = portdetails['eth_mtu']
    mac = portdetails['eth_hw_addr']

    return 'The state for port **' + portnum + '** is **' + state + '**!  Its description is **' + desc + \
           '**. It is currently enabled as a **' + mode + '** port running at **' + speed + '**' + \
           ' and MTU is set at **' + mtu + '**'

#print getint('eth1/1')
