from typing import Any

import CynanBot.misc.utils as utils


class GoogleTextSynthesisInput():

    def __init__(self, text: str):
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        self.__text: str = text

    def getText(self) -> str:
        return self.__text

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'text': self.__text
        }
