from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.language.languageEntry import LanguageEntry


class DeepLTranslationRequest():

    def __init__(self, targetLanguage: LanguageEntry, text: str):
        if not isinstance(targetLanguage, LanguageEntry):
            raise TypeError(f'targetLanguage argument is malformed: \"{targetLanguage}\"')
        elif not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        self.__targetLanguage: LanguageEntry = targetLanguage
        self.__text: str = text

    def getTargetLanguage(self) -> LanguageEntry:
        return self.__targetLanguage

    def getText(self) -> str:
        return self.__text

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'targetLanguage': self.__targetLanguage,
            'text': self.__text
        }
