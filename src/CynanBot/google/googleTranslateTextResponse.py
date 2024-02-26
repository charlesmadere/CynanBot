from typing import Any, Dict, List, Optional

from CynanBot.google.googleTranslation import GoogleTranslation


class GoogleTranslateTextResponse():

    def __init__(
        self,
        glossaryTranslations: Optional[List[GoogleTranslation]],
        translations: Optional[List[GoogleTranslation]]
    ):
        self.__glossaryTranslations: Optional[List[GoogleTranslation]] = glossaryTranslations
        self.__translations: Optional[List[GoogleTranslation]] = translations

    def getGlossaryTranslations(self) -> Optional[List[GoogleTranslation]]:
        return self.__glossaryTranslations

    def getTranslations(self) -> Optional[List[GoogleTranslation]]:
        return self.__translations

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'glossaryTranslations': self.__glossaryTranslations,
            'translations': self.__translations
        }
