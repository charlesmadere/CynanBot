from typing import Any

from ..misc import utils as utils


class GoogleTranslateTextTransliterationConfig():

    def __init__(
        self,
        enableTransliteration: bool
    ):
        if not utils.isValidBool(enableTransliteration):
            raise TypeError(f'enableTransliteration argument is malformed: \"{enableTransliteration}\"')

        self.__enableTransliteration: bool = enableTransliteration

    def getEnableTransliteration(self) -> bool:
        return self.__enableTransliteration

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'enableTransliteration': self.__enableTransliteration
        }
