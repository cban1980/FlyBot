import requests
from bs4 import BeautifulSoup as bs
import random
from pydle import on_message

class quotes(pydle):
    def __init__(self):
        pass

    def bofh(self):
        """Return random bofh quote"""
        url_data = requests.get('http://pages.cs.wisc.edu/~ballard/bofh/excuses').text
        soup = bs(url_data, 'html.parser')
        for line in soup:
            soppa = line.splitlines()
            soppa = random.choice(soppa)
        return soppa

    # on_message pydle listener for bofh 
    def on_message(self, source, target, message):
        if message.startswith('.bofh'):
            return self.bofh()



