from typing import Any

import CynanBot.misc.utils as utils


class DeepLTranslationResponse():

    def __init__(
        self,
        detectedSourceLanguage: str | None,
        text: str
    ):
        if detectedSourceLanguage is not None and not isinstance(detectedSourceLanguage, str):
            raise TypeError(f'detectedSourceLanguage argument is malformed: \"{detectedSourceLanguage}\"')
        elif not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        self.__detectedSourceLanguage: str | None = detectedSourceLanguage
        self.__text: str = text

    def getDetectedSourceLanguage(self) -> str | None:
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
