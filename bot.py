import os
from ciscosparkbot import SparkBot
from showint import getint

bot_email = "nxosbot@sparkbot.io"
spark_token = "MjMwNjYzNTItOTkyMC00NGM3LTk4ZmYtOTI5MjVhNTA2OTlkM2U3YWUwZjItMGU5"
bot_url = "https://5675ed53.ngrok.io"
bot_app_name = "nxosbot"

def do_something(incoming_msg):
    return "i did what you said - {}".format(incoming_msg.text)

bot = SparkBot(bot_app_name, spark_bot_token=spark_token,
               spark_bot_url=bot_url, spark_bot_email=bot_email)

def getinterface(spark_msg):
    #print spark_msg.text
    portname = spark_msg.text.split()[2]
    return getint(portname)

bot.add_command('dosomething', 'help for do something', do_something)
bot.add_command('port', 'usage: @nxosbot port Eth1/1', getinterface)
bot.run(host='0.0.0.0', port=5000)
