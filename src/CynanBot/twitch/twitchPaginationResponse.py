from typing import Any, Dict

import CynanBot.misc.utils as utils


class TwitchPaginationResponse():

    def __init__(self, cursor: str):
        if not utils.isValidStr(cursor):
            raise ValueError(f'cursor argument is malformed: \"{cursor}\"')

        self.__cursor: str = cursor

    def getCursor(self) -> str:
        return self.__cursor

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'cursor': self.__cursor
        }
