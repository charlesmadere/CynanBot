from typing import Any, Dict, Set

from CynanBot.google.googleScope import GoogleScope


class GoogleGenerateAccessTokenRequest():

    def __init__(self, scopes: Set[GoogleScope]):
        if not isinstance(scopes, Set):
            raise TypeError(f'scopes argument is malformed: \"{scopes}\"')
        elif len(scopes) == 0:
            raise ValueError(f'scopes can\'t be empty: {scopes}')

        self.__scopes: Set[GoogleScope] = scopes

    def getScopes(self) -> Set[GoogleScope]:
        return self.__scopes

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'scopes': self.__scopes
        }
