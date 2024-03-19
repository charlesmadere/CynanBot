from typing import Any

from CynanBot.google.googleScope import GoogleScope


class GoogleGenerateAccessTokenRequest():

    def __init__(self, scopes: set[GoogleScope]):
        if not isinstance(scopes, set):
            raise TypeError(f'scopes argument is malformed: \"{scopes}\"')
        elif len(scopes) == 0:
            raise ValueError(f'scopes can\'t be empty: {scopes}')

        self.__scopes: set[GoogleScope] = scopes

    def getScopes(self) -> set[GoogleScope]:
        return self.__scopes

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'scopes': self.__scopes
        }
