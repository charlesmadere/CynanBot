from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.google.googleVoiceGender import GoogleVoiceGender


class GoogleVoiceSelectionParams():

    def __init__(
        self,
        gender: GoogleVoiceGender | None,
        languageCode: str,
        name: str | None
    ):
        if gender is not None and not isinstance(gender, GoogleVoiceGender):
            raise TypeError(f'gender argument is malformed: \"{gender}\"')
        elif not utils.isValidStr(languageCode):
            raise TypeError(f'languageCode argument is malformed: \"{languageCode}\"')
        elif name is not None and not utils.isValidStr(name):
            raise TypeError(f'name argument is malformed: \"{name}\"')

        self.__gender: GoogleVoiceGender | None = gender
        self.__languageCode: str = languageCode
        self.__name: str | None = name

    def getGender(self) -> GoogleVoiceGender | None:
        return self.__gender

    def getLanguageCode(self) -> str:
        return self.__languageCode

    def getName(self) -> str | None:
        return self.__name

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'gender': self.__gender,
            'languageCode': self.__languageCode,
            'name': self.__name
        }
