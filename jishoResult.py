from typing import List


class JishoResult():

    def __init__(
        self,
        definitions: List[str],
        furigana: str,
        url: str,
        word: str
    ):
        if definitions == None or len(definitions) == 0:
            raise ValueError(f'definitions argument is malformed: \"{definitions}\"')
        elif url == None or len(url) == 0 or url.isspace():
            raise ValueError(f'url argument is malformed: \"{url}\"')
        elif word == None or len(word) == 0 or word.isspace():
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
        return self.__furigana != None and len(self.__furigana) != 0 and not self.__furigana.isspace()
