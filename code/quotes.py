
import requests
from bs4 import BeautifulSoup as bs
import random
import pydle
import code


class quotes(code.Base):

    def __init__(self):
        pass

    def start(self):
        print("Quotes module loaded")


    def get_random_bofh_quote():
        """Return random bofh quote"""
        url_data = requests.get('http://pages.cs.wisc.edu/~ballard/bofh/excuses').text
        soup = bs(url_data, 'html.parser')
        for line in soup:
            soppa = line.splitlines()
            soppa = random.choice(soppa)
        return soppa

    # on_message pydle coroutine for triggering the bofh function and returning the quote
    # when someone writes !bofh in the channel the bot is in.


    # Define the on_message coroutine function and decorate it with @pydle.coroutine
    # @pydle.coroutine
    # def on_channel_message(self, target, by, message):
    #     if message.startswith("!bofh"):
    #         yield from self.message(target, "BOFH says: " + get_random_bofh_quote())
    #         print("BOFH says: " + quotes.get_random_bofh_quote())

