import os
from ciscosparkbot import SparkBot
import command_handlers
import config

bot_email = os.getenv("SPARK_BOT_EMAIL")
spark_token = os.getenv("SPARK_BOT_TOKEN")
bot_url = os.getenv("SPARK_BOT_URL")
bot_app_name = os.getenv("SPARK_BOT_APP_NAME")
nxos_username = os.getenv("NXOS_LOGIN")
nxos_password = os.getenv("NXOS_PASSWORD")



bot = SparkBot(bot_app_name, spark_bot_token=spark_token,
               spark_bot_url=bot_url, spark_bot_email=bot_email, debug=True)

# Override default commands
bot.commands = dict()

# Register our commands
bot.add_command('version',
                "Get the running version from an NX-OS switch. \
                e.g `@{} version 10.1.1.1`".format(bot_email.split('@')[0]),
                command_handlers.version)
bot.add_command('arptable',
                'retrieve the arp table of a switch. \
                e.g. `@{} arptable 10.1.1.1`'.format(bot_email.split('@')[0]),
                command_handlers.arptable)

bot.add_command('portinfo', 'retrieve interface details. \
                e.g `@{} portinfo 10.1.1.1 Eth1/1`'.format(bot_email.split('@')[0]),
                command_handlers.getinterface)

bot.add_command('maclookup', 'find details on a specific mac address.  \
                e.g. `@{} maclookup xxxx.yyyy.zzzz`'.format(bot_email.split('@')[0]),
                command_handlers.findmac)
bot.add_command('arplookup', 'find arp entry for ip address. \
                e.g. `@{} iparp 192.168.10.1`'.format(bot_email.split('@')[0]),
                command_handlers.findip)


bot.run(host='0.0.0.0', port=5000)
