from typing import Any, Dict

import CynanBot.misc.utils as utils


class GoogleTranslateTextGlossaryConfig():

    def __init__(
        self,
        ignoreCase: bool,
        glossary: str
    ):
        if not utils.isValidBool(ignoreCase):
            raise TypeError(f'ignoreCase argument is malformed: \"{ignoreCase}\"')
        elif not utils.isValidStr(glossary):
            raise TypeError(f'glossary argument is malformed: \"{glossary}\"')

        self.__ignoreCase: bool = ignoreCase
        self.__glossary: str = glossary

    def getGlossary(self) -> str:
        return self.__glossary

    def getIgnoreCase(self) -> bool:
        return self.__ignoreCase

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'glossary': self.__glossary,
            'ignoreCase': self.__ignoreCase
        }
