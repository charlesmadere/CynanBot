from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils


class GoogleTranslateTextGlossaryConfig():

    def __init__(
        self,
        ignoreCase: bool,
        glossary: Optional[str]
    ):
        if not utils.isValidBool(ignoreCase):
            raise TypeError(f'ignoreCase argument is malformed: \"{ignoreCase}\"')
        elif glossary is not None and not isinstance(glossary, str):
            raise TypeError(f'glossary argument is malformed: \"{glossary}\"')

        self.__ignoreCase: bool = ignoreCase
        self.__glossary: Optional[str] = glossary

    def getGlossary(self) -> Optional[str]:
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
