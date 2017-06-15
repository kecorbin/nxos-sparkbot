import os
from nxos.version import get_version
from nxos.interface import getint
from nxos.arp import get_arp_table, get_arp_entry
from nxos.interface import getint
from nxos.mac import find_mac
import config

"""
command_handlers.py

These functions are used to responsible for processing command specific spark
messages, performing appropriate actions and formatting responses back to spark_token

"""

switches = os.getenv("NXOS_SWITCHES")

def version(incoming_msg):
    ip = incoming_msg.text.split()[-1]
    version = get_version(ip)
    return "### Switch {} is running version {}".format(ip, version)

def getinterface(spark_msg):
    ip = spark_msg.text.split()[2]
    portname = spark_msg.text.split()[3]
    return getint(ip, portname)

def arptable(spark_msg):
    host = spark_msg.text.split()[-1]
    arplist = get_arp_table(host)
    if arplist:
        if isinstance(arplist,dict):
            # check for dictionary, handle single ARP entry
            response2spark = "### ARP table for **{}**\n".format(host)
            arp = arplist
            mac = (arp['mac'])
            ipaddr = (arp['ip-addr-out'])
            arpresult = "* Mac Address = {}, IP Address = {}, \n".format(mac, ipaddr)
            response2spark = response2spark + arpresult
        else:
            # check for list, meaning multiple arp entries

            response2spark = "### ARP table for **{}**\n".format(host)
            for arp in arplist:
                mac = (arp['mac'])
                ipaddr = (arp['ip-addr-out'])
                arpresult = "* Mac Address = {}, IP Address = {}, \n".format(mac, ipaddr)
                response2spark = response2spark + arpresult
        return response2spark
    else:
        return "### No ARP entries exist on {}".format(host)


def findmac(spark_msg):
    mac = spark_msg.text.split()[-1]
    header = "### Details for MAC address {}**\n".format(mac)
    response_to_spark = ''
    for switch in config.switches:
        response_from_switch = find_mac(switch, mac)
        if response_from_switch:
            vlan, port = response_from_switch
            response_to_spark += "* {} see's **{}** on vlan **{}**, port **{}**\n".format(switch,
                                                                                          mac,
                                                                                          vlan,
                                                                                          port)
    if len(response_to_spark) > 1:
        return header + response_to_spark
    else:
        return "Could not find any information on **{}**".format(mac)

def findip(spark_msg):
    ip = spark_msg.text.split()[-1]
    header = "### ARP entries for IP address {}**\n".format(ip)
    response_to_spark = ''

    for switch in config.switches:
        mac = get_arp_entry(switch, ip)

        if mac:
            response_to_spark += "* {} has ARP entry for {} which is **{}**\n".format(switch, ip, mac)
    if len(response_to_spark) > 1:
        return header + response_to_spark
    else:
        return "Could not find an ARP entry for {}".format(ip)
