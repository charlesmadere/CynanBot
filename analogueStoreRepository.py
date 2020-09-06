from datetime import datetime, timedelta
from lxml import html
import requests

class AnalogueStoreRepository():
    def __init__(self):
        self.__storeStock = None
        self.__cacheTime = datetime.now() - timedelta(days = 1)

    def fetchStoreStock(self):
        now = datetime.now()
        delta = now - timedelta(hours = 1)

        if delta > self.__cacheTime or len(self.__storeStock) == 0:
            self.__cacheTime = now
            self.__storeStock = self.__refreshStoreStock()

        return self.__storeStock

    def __refreshStoreStock(self):
        print('Refreshing Analogue store stock...')
        rawResponse = requests.get('https://www.analogue.co/store')
        htmlTree = html.fromstring(rawResponse.content)

        if htmlTree == None:
            print(f'htmlTree is malformed: {htmlTree}')
            return None

        productTrees = htmlTree.find_class('store_product-header__1rLY-')

        if productTrees == None:
            print(f'productTrees is malformed: {productTrees}')
            return None
        elif len(productTrees) == 0:
            print(f'productTrees is empty: {productTrees}')
            return None

        inStockProducts = list()

        for productTree in productTrees:
            nameTrees = productTree.find_class('store_title__3eCzb')

            if nameTrees == None or len(nameTrees) != 1:
                continue

            name = nameTrees[0].text

            if name == None or len(name) == 0 or name.isspace():
                continue

            name = name.strip()

            if name == None or len(name) == 0 or name.isspace():
                continue
            elif '8BitDo'.lower() in name.lower():
                # don't show 8BitDo products in the final stock listing
                continue

            outOfStockElement = productTree.find_class('button_Disabled__2CEbR')

            if outOfStockElement == None or len(outOfStockElement) == 0:
                inStockProducts.append(name)

        if len(inStockProducts) == 0:
            return ""

        return ', '.join(inStockProducts)
