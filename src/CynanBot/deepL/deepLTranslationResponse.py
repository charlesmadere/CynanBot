from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.language.languageEntry import LanguageEntry


class DeepLTranslationResponse():

    def __init__(
        self,
        detectedSourceLanguage: LanguageEntry | None,
        text: str
    ):
        if detectedSourceLanguage is not None and not isinstance(detectedSourceLanguage, LanguageEntry):
            raise TypeError(f'detectedSourceLanguage argument is malformed: \"{detectedSourceLanguage}\"')
        elif not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        self.__detectedSourceLanguage: LanguageEntry | None = detectedSourceLanguage
        self.__text: str = text

    def getDetectedSourceLanguage(self) -> LanguageEntry | None:
        return self.__detectedSourceLanguage

    def getText(self) -> str:
        return self.__text

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'detectedSourceLanguage': self.__detectedSourceLanguage,
            'text': self.__text
        }
