import os
from ciscosparkbot import SparkBot
from nxos.version import get_version
from nxos.arp import get_iparp
from nxos.showint import getint

bot_email = os.getenv("SPARK_BOT_EMAIL")
spark_token = os.getenv("SPARK_BOT_TOKEN")
bot_url = os.getenv("SPARK_BOT_URL")
bot_app_name = os.getenv("SPARK_BOT_APP_NAME")
nxos_username = os.getenv("NXOS_LOGIN")
nxos_password = os.getenv("NXOS_PASSWORD")

def version(incoming_msg):
    ip = incoming_msg.text.split()[-1]
    version = get_version(ip, nxos_username, nxos_password)
    return "Switch {} is running version {}".format(ip, version)


def getinterface(spark_msg):
    ip = spark_msg.text.split()[2]
    portname = spark_msg.text.split()[3]
    return getint(portname, ip, nxos_username, nxos_password)

bot = SparkBot(bot_app_name, spark_bot_token=spark_token,
               spark_bot_url=bot_url, spark_bot_email=bot_email, debug=True)

bot.add_command('version',
                "Get the running version from an NX-OS switch. \
                e.g `@{} version 10.1.1.1`".format(bot_email.split('@')[0]),
                version)
bot.add_command('arp',
                'retrieve the arp table of a switch. \
                e.g. `@{} arp 10.1.1.1`'.format(bot_email.split('@')[0]),
                get_iparp)

bot.add_command('port', 'retrieve interface details. \
                e.g `@{} port 10.1.1.1 Eth1/1`'.format(bot_email.split('@')[0]),
                getinterface)

bot.run(host='0.0.0.0', port=5000)
