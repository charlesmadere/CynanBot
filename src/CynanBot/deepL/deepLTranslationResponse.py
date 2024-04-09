from typing import Any


class DeepLTranslationResponse():

    def __init__(
        self,
        text: str
    ):
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
