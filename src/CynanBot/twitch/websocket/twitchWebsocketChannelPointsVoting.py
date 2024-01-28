from typing import Any, Dict

import CynanBot.misc.utils as utils


class TwitchWebsocketChannelPointsVoting():

    def __init__(
        self,
        isEnabled: bool,
        amountPerVote: int
    ):
        if not utils.isValidBool(isEnabled):
            raise TypeError(f'isEnabled argument is malformed: \"{isEnabled}\"')
        elif not utils.isValidInt(amountPerVote):
            raise TypeError(f'amountPerVote argument is malformed: \"{amountPerVote}\"')
        elif amountPerVote < 0 or amountPerVote > utils.getLongMaxSafeSize():
            raise ValueError(f'amountPerVote argument is out of bounds: {amountPerVote}')

        self.__isEnabled: bool = isEnabled
        self.__amountPerVote: int = amountPerVote

    def isEnabled(self) -> bool:
        return self.__isEnabled

    def getAmountPerVote(self) -> int:
        return self.__amountPerVote

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'amountPerVote': self.__amountPerVote,
            'isEnabled': self.__isEnabled
        }
