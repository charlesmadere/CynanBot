from datetime import datetime, timedelta
from lxml import html
import requests

class AnalogueStoreRepository():
    def __init__(self):
        self.__storeStock = ""
        self.__cacheTime = datetime.now() - timedelta(days = 1)

    def fetchStoreStock(self):
        now = datetime.now()
        delta = now - timedelta(hours = 8)

        if delta > self.__cacheTime or len(self.__storeStock) == 0:
            self.__cacheTime = now
            self.__refreshStoreStock()

        return self.__storeStock

    def __refreshStoreStock(self):
        rawResponse = requests.get('https://www.analogue.co/store')
        tree = html.fromstring(rawResponse.content)

        
