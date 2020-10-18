import requests
from lxml import html

from jishoResult import JishoResult


class JishoHelper():

    def __init__(self):
        pass

    def search(self, query: str):
        if query == None or len(query) == 0 or query.isspace():
            raise ValueError(f'query argument is malformed: \"{query}\"')

        query = query.strip()
        print(f'Looking up \"{query}\"...')

        rawResponse = requests.get(f'https://jisho.org/search/{query}')
        htmlTree = html.fromstring(rawResponse.content)

        if htmlTree == None:
            print(f'htmlTree is malformed: \"{htmlTree}\"')
            return None

        parentElements = htmlTree.find_class('concept_light-representation')
        if parentElements == None or len(parentElements) == 0:
            print(f'parentElements is malformed: \"{parentElements}\"')
            return None

        textElements = parentElements[0].find_class('text')
        if textElements == None or len(textElements) != 1:
            print(f'textElements is malformed: \"{textElements}\"')
            return None

        word = textElements[0].text_content()
        if word == None or len(word) == 0 or word.isspace():
            print(f'word is malformed: \"{word}\"')
            return None

        word = word.strip()

        definitionElements = htmlTree.find_class('meaning-meaning')
        if definitionElements == None or len(definitionElements) == 0:
            print(f'definitionElements is malformed: \"{definitionElements}\"')
            return None

        definitions = list()

        for definitionElement in definitionElements:
            breakUnitElements = definitionElement.find_class('break-unit')
            if breakUnitElements == None or len(breakUnitElements) != 0:
                continue

            definition = definitionElement.text_content()
            if definition == None or len(definition) == 0 or definition.isspace():
                continue

            definitions.append(f'({len(definitions) + 1}) {definition.strip()}')

            if len(definitions) >= 3:
                # keep from adding tons of definitions
                break

        if len(definitions) == 0:
            print(f'Found no definitions within definitionElements: \"{definitionElements}\"')
            return None

        furigana = None
        furiganaElement = htmlTree.find_class('kanji-1-up')
        if furiganaElement != None and len(furiganaElement) != 0:
            furigana = furiganaElement[0].text_content()

            if furigana == None or len(furigana) == 0 or furigana.isspace():
                furigana = None
            else:
                furigana = furigana.strip()

        return JishoResult(
            definitions = definitions,
            furigana = furigana,
            word = word
        )
