from typing import Any, Dict

import CynanBot.misc.utils as utils


class TtsRaidInfo():

    def __init__(self, viewers: int):
        if not utils.isValidInt(viewers):
            raise TypeError(f'viewers argument is malformed: \"{viewers}\"')
        elif viewers < 0 or viewers > utils.getIntMaxSafeSize():
            raise ValueError(f'viewers argument is out of bounds: {viewers}')

        self.__viewers: int = viewers

    def getViewers(self) -> int:
        return self.__viewers

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'viewers': self.__viewers
        }
