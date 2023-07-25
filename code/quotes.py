import requests
from bs4 import BeautifulSoup as bs
import random
import pydle


def bofh():
    """Return random bofh quote"""
    url_data = requests.get('http://pages.cs.wisc.edu/~ballard/bofh/excuses').text
    soup = bs(url_data, 'html.parser')
    for line in soup:
        soppa = line.splitlines()
        soppa = random.choice(soppa)
    return soppa

# on_message pydle coroutine for triggering the bofh function and returning the quote
# when someone writes !bofh in the channel the bot is in.

class quotes(pydle.Client):
    # Define the on_message coroutine function and decorate it with @pydle.coroutine
    @pydle.coroutine
    def on_message(self, target, by, message):
        if message.startswith("!bofh"):
            yield from self.message(target, "BOFH says: " + bofh())
            print("BOFH says: " + bofh())

