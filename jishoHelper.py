from jishoResult import JishoResult
from lxml import html
import requests

class JishoHelper():

    def __init__(self):
        pass

    def search(self, query: str):
        if query == None or len(query) == 0 or query.isspace():
            raise ValueError(f'query argument is malformed: \"{query}\"')

        query = query.strip()
        rawResponse = requests.get(f'https://jisho.org/search/{query}')
        htmlTree = html.fromstring(rawResponse.content)

        if htmlTree == None:
            print(f'htmlTree is malformed: {htmlTree}')
            return None

        wordSpan = htmlTree.find_class("//span[@class='text'")
        wordText = wordSpan.text_content()
