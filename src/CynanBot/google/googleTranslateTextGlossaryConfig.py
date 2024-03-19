from typing import Any

import CynanBot.misc.utils as utils


class GoogleTranslateTextGlossaryConfig():

    def __init__(
        self,
        ignoreCase: bool,
        glossary: str | None
    ):
        if not utils.isValidBool(ignoreCase):
            raise TypeError(f'ignoreCase argument is malformed: \"{ignoreCase}\"')
        elif glossary is not None and not isinstance(glossary, str):
            raise TypeError(f'glossary argument is malformed: \"{glossary}\"')

        self.__ignoreCase: bool = ignoreCase
        self.__glossary: str | None = glossary

    def getGlossary(self) -> str | None:
        return self.__glossary

    def getIgnoreCase(self) -> bool:
        return self.__ignoreCase

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'glossary': self.__glossary,
            'ignoreCase': self.__ignoreCase
        }
