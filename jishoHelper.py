import locale
import urllib
from typing import List

import requests
from lxml import html

import CynanBotCommon.utils as utils


class JishoHelper():

    def __init__(self):
        pass

    def search(self, query: str):
        if not utils.isValidStr(query):
            raise ValueError(f'query argument is malformed: \"{query}\"')

        query = query.strip()
        print(f'Looking up \"{query}\"...')

        encodedQuery = urllib.parse.quote(query)
        url = f'https://jisho.org/search/{encodedQuery}'

        rawResponse = requests.get(url)

        htmlTree = html.fromstring(rawResponse.content)
        if htmlTree is None:
            print(f'htmlTree is malformed: \"{htmlTree}\"')
            return None

        parentElements = htmlTree.find_class('concept_light-representation')
        if not utils.hasItems(parentElements):
            print(f'parentElements is malformed: \"{parentElements}\"')
            return None

        textElements = parentElements[0].find_class('text')
        if textElements is None or len(textElements) != 1:
            print(f'textElements is malformed: \"{textElements}\"')
            return None

        word = utils.cleanStr(textElements[0].text_content())
        if len(word) == 0:
            print(f'word is malformed: \"{word}\"')
            return None

        definitionElements = htmlTree.find_class('meaning-meaning')
        if not utils.hasItems(definitionElements):
            print(f'definitionElements is malformed: \"{definitionElements}\"')
            return None

        definitions = list()

        for definitionElement in definitionElements:
            breakUnitElements = definitionElement.find_class('break-unit')
            if breakUnitElements is None or len(breakUnitElements) != 0:
                continue

            definition = utils.cleanStr(definitionElement.text_content())
            if len(definition) == 0:
                continue

            number = locale.format_string("%d", len(definitions) + 1, grouping=True)
            definitions.append(f'#{number} {definition}')

            if len(definitions) >= 3:
                # keep from adding tons of definitions
                break

        if len(definitions) == 0:
            print(f'Found no definitions within definitionElements: \"{definitionElements}\"')
            return None

        furigana = None
        furiganaElements = htmlTree.find_class('furigana')
        if utils.hasItems(furiganaElements):
            furigana = utils.cleanStr(furiganaElements[0].text_content())

        return JishoResult(
            definitions=definitions,
            furigana=furigana,
            url=url,
            word=word
        )


class JishoResult():

    def __init__(
        self,
        definitions: List[str],
        furigana: str,
        url: str,
        word: str
    ):
        if not utils.hasItems(definitions):
            raise ValueError(f'definitions argument is malformed: \"{definitions}\"')
        elif not utils.isValidStr(url):
            raise ValueError(f'url argument is malformed: \"{url}\"')
        elif not utils.isValidStr(word):
            raise ValueError(f'word argument is malformed: \"{word}\"')

        self.__definitions = definitions
        self.__furigana = furigana
        self.__url = url
        self.__word = word

    def getDefinitions(self):
        return self.__definitions

    def getFurigana(self):
        return self.__furigana

    def getUrl(self):
        return self.__url

    def getWord(self):
        return self.__word

    def hasFurigana(self):
        return utils.isValidStr(self.__furigana)

    def toStr(self, definitionDelimiter: str = ' '):
        if definitionDelimiter is None:
            raise ValueError(f'definitionDelimiter argument is malformed: \"{definitionDelimiter}\"')

        furigana = ''
        if self.hasFurigana():
            furigana = f'({self.__furigana}) '

        definitions = definitionDelimiter.join(self.__definitions)
        return f'{furigana}{self.__word} — {definitions}'
