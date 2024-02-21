from typing import List, Optional

import CynanBot.misc.utils as utils


class JishoVariant():

    def __init__(
        self,
        definitions: List[str],
        partsOfSpeech: Optional[List[str]],
        furigana: Optional[str],
        word: Optional[str]
    ):
        if not utils.areValidStrs(definitions):
            raise ValueError(f'definitions argument is malformed: \"{definitions}\"')

        self.__definitions: List[str] = definitions
        self.__partsOfSpeech: Optional[List[str]] = partsOfSpeech
        self.__furigana: Optional[str] = furigana
        self.__word: Optional[str] = word

    def getDefinitions(self) -> List[str]:
        return self.__definitions

    def getFurigana(self) -> Optional[str]:
        return self.__furigana

    def getPartsOfSpeech(self) -> Optional[List[str]]:
        return self.__partsOfSpeech

    def getWord(self) -> Optional[str]:
        return self.__word

    def hasFurigana(self) -> bool:
        return utils.isValidStr(self.__furigana)

    def hasPartsOfSpeech(self) -> bool:
        return utils.areValidStrs(self.__partsOfSpeech)

    def hasWord(self) -> bool:
        return utils.isValidStr(self.__word)

    def toStr(self, definitionDelimiter: str = ', ') -> str:
        assert isinstance(definitionDelimiter, str), f"malformed {definitionDelimiter=}"

        word = ''
        if self.hasWord():
            word = self.__word

        furigana = ''
        if self.hasFurigana():
            if utils.isValidStr(word):
                furigana = f' ({self.__furigana})'
            else:
                furigana = self.__furigana

        definitionsList: List[str] = list()
        for definition in self.__definitions:
            definitionsList.append(definition)

        definitions = definitionDelimiter.join(definitionsList)
        return f'{word}{furigana} — {definitions}'
