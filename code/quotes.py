import requests
from bs4 import BeautifulSoup as bs
import random

class quotes:
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

    async def handle_command(self, target, by, message):
        if message.startswith("!bofh"):
            return self.bofh()
        else:
            return None



