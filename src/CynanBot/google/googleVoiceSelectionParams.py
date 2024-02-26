from typing import Any, Dict

import CynanBot.misc.utils as utils
from CynanBot.google.googleVoiceGender import GoogleVoiceGender


class GoogleVoiceSelectionParams():

    def __init__(
        self,
        gender: GoogleVoiceGender,
        languageCode: str,
        name: str
    ):
        if not isinstance(gender, GoogleVoiceGender):
            raise TypeError(f'gender argument is malformed: \"{gender}\"')
        elif not utils.isValidStr(languageCode):
            raise TypeError(f'languageCode argument is malformed: \"{languageCode}\"')
        elif not utils.isValidStr(name):
            raise TypeError(f'name argument is malformed: \"{name}\"')

        self.__gender: GoogleVoiceGender = gender
        self.__languageCode: str = languageCode
        self.__name: str = name

    def getGender(self) -> GoogleVoiceGender:
        return self.__gender

    def getLanguageCode(self) -> str:
        return self.__languageCode

    def getName(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'gender': self.__gender,
            'languageCode': self.__languageCode,
            'name': self.__name
        }
