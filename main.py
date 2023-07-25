#!/usr/bin/env python
# -*- coding: utf-8 -*-
# IRC Bot for #nightfly on DALnet, based on the pydle framework for Python 3.10 and above.

import pydle
import configparser
import os
import importlib
import sys

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


class FlyBot(pydle.Client):
    """main class for the bot"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def on_connect(self):
        await self.join(ext_channel_autojoin_list)

    # Function to load all the files in the code/ directory that has a .py file ending
    # and then load the code from the file into the bot. This allows for easy reloading
    # of code without having to restart the bot. this uses importlib to import the code
    # the path of the files ar code/ + filename.py

    def loadcode(self):
        for file in os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/code/"):
            if file.endswith(".py"):
                importlib.import_module("code." + file[:-3])
                print("Loaded " + file[:-3])
    
    # irc command to reload a particular module loaded from the code/ directory
    # this uses importlib to reload the module. command looks like !reload <module>

    @pydle.coroutine
    def on_message(self, target, by, message):
        if message.startswith("!reload"):
            if by == "zphinx":
                try:
                    module = message.split(" ")[1]
                    importlib.reload(importlib.import_module("code." + module))
                    yield from self.message(target, "Reloaded " + module)
                except Exception as e:
                    yield from self.message(target, "Error reloading module: " + str(e))
            else:
                yield from self.message(target, "You are not authorized to use this command.")
        elif message.startswith("!load"):
            if by == "zphinx":
                try:
                    module = message.split(" ")[1]
                    importlib.import_module("code." + module)
                    yield from self.message(target, "Hotloaded " + module)
                except Exception as e:
                    yield from self.message(target, "Error hotloading module: " + str(e))
            else:
                    yield from self.message(target, "You are not authorized to use this command.")
        elif message.startswith("!unload"):
            if by == "zphinx":
                try:
                    module = message.split(" ")[1]
                    del sys.modules["code." + module]
                    yield from self.message(target, "Unloaded " + module)
                except Exception as e:
                    yield from self.message(target, "Error unloading module: " + str(e))
            else:
                yield from self.message(target, "You are not authorized to use this command.")
            

    # pydle coroutine to hotload a .py file from the code/ directory by using importlib
    # is triggered by the !hotload command. command looks like !hotload <module>


client = FlyBot(src_nick, fallback_nicknames=[], username=src_ident, realname=src_realname)
client.loadcode()
client.run(ext_server_hostname, tls=False, tls_verify=False, source_address=(src_host, 0))
client.handle_forever(family=pydle.IPv6)