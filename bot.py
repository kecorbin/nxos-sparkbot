import os
from ciscosparkbot import SparkBot

bot_email = "CHANGEME"
spark_token = "CHANGEME"
bot_url = "CHANGEME"
bot_app_name = "Version Bot"

def do_something(incoming_msg):
    return "i did what you said - {}".format(incoming_msg.text)

bot = SparkBot(bot_app_name, spark_bot_token=spark_token,
               spark_bot_url=bot_url, spark_bot_email=bot_email)

from version import get_version
bot.add_command('dosomething', 'help for do something', do_something)
bot.add_command('version', 'get the version of a switch', get_version)
bot.run(host='0.0.0.0', port=5000)
