from typing import List, Optional

from CynanBot.google.googleTranslateTextEntry import GoogleTranslateTextEntry


class GoogleTranslateTextResponse():

    def __init__(
        self,
        glossaryTranslations: Optional[List],
        translations: Optional[List]
    ):
        self.__glossaryTranslations: Optional[List] = glossaryTranslations
        self.__translations: Optional[List] = translations
