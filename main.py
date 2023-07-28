#!/usr/bin/env python
# -*- coding: utf-8 -*-
# IRC Bot for #nightfly on DALnet, based on the pydle framework for Python 3.7 and above.

import pydle
import configparser
import os
import platform
import ircfunctions
# Use configparser to read the config file from the same directory as the script

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + "/config.ini")
src_nick = config.get('bot', 'nick')
src_ident = config.get('bot', 'ident')
src_realname = config.get('bot', 'realname')
src_host = config.get('bot', 'host')
ext_server_hostname = config.get('server', 'hostname')
ext_port = config.getint('server', 'port')
ext_channel_autojoin_list = config.get('server', 'autojoin')

# Ctcp variables.
ctcp_version = config.get('ctcp', 'version')

class FlyBot(pydle.Client):
    """main class for the bot"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modules = {}
    
    async def on_connect(self):
        await self.join(ext_channel_autojoin_list)
        print("Connected to: " + ext_server_hostname + " with hostname: " + src_host + " using nickname: " + src_nick)
        print("Joined channels: " + ext_channel_autojoin_list)
        print("Loaded " + str(len(ircfunctions.__dict__)) + " functions from ircfunctions.py")
    
    # pydle settings to handle ctcp responses for version.
    async def on_ctcp_version(self, by, target, contents):
        await self.ctcp_reply(by, 'VERSION', ctcp_version)

    # now we handle on_channel_message events, with a whole lot of elifs.

    async def on_channel_message(self, target, by, message):
        if message.lower().startswith('!sv'):
            await self.message(target, "I'm " + ctcp_version + " running on Python " + platform.python_version())
        elif message.lower().startswith('!tr'):
            fran = message.split(' ')[1]
            till = message.split(' ')[2]
            mening = message.partition(till)[2]
            oversattning = ircfunctions.tr(fran, till, mening)
            await self.message(target, "{}: {}".format(by, oversattning))
        elif message.lower().startswith('!lk'):
            lk = ircfunctions.lk()
            await self.message(target, "{}'s lyckokaka: {}".format(by, lk))
        elif message.lower().startswith('!väder'):
            arg = message.split(' ', 1)[1:]
            arg2 = ' '.join(arg)
            arg2 = arg2.capitalize()
            vader = ircfunctions.vader(arg2)
            await self.message(target, "{}: {}".format(by, vader))
        elif message.lower().startswith('!tinyurl'):
            arg = message.split(' ', 1)[1:]
            arg = ' '.join(arg)
            output = ircfunctions.tinyurl(arg)
            await self.message(target, "{}'s förkortade länk: {}".format(by, output))
        # every time the nick livet joins the channel #nightfly send to the channel "Welcome back livet!"
        elif message.lower() == "!help":
            await self.message(target, "Available commands: !sv, !tr, !lk, !väder, !tinyurl, !help")
        elif message.lower().startswith('!'):
            await self.message(target, "Unknown command, try !help")



    
    # Function to handle ! commands on IRC from users, functions live in the ircfunctions.py file.
    # This function is called from the pydle framework when a message is received.
    # The message is parsed and if it starts with !, the command is executed.

client = FlyBot(src_nick, fallback_nicknames=[], username=src_ident, realname=src_realname)
client.run(ext_server_hostname, tls=False, tls_verify=False, source_address=(src_host, 0))
client.handle_forever(family=pydle.IPv6)