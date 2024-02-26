from typing import Any, Dict, List, Optional

from CynanBot.google.googleTranslation import GoogleTranslation


class GoogleTranslateTextResponse():

    def __init__(
        self,
        glossaryTranslations: Optional[List[GoogleTranslation]],
        translations: Optional[List[GoogleTranslation]]
    ):
        if glossaryTranslations is not None and not isinstance(glossaryTranslations, List):
            raise TypeError(f'glossaryTranslations argument is malformed: \"{glossaryTranslations}\"')
        elif translations is not None and not isinstance(translations, List):
            raise TypeError(f'translations argument is malformed: \"{translations}\"')

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
