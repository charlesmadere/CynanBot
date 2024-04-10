import locale
from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.cheerActions.cheerActionBitRequirement import \
    CheerActionBitRequirement
from CynanBot.cheerActions.cheerActionStreamStatusRequirement import \
    CheerActionStreamStatusRequirement
from CynanBot.cheerActions.cheerActionType import CheerActionType
from CynanBot.cheerActions.exceptions import \
    TimeoutDurationSecondsTooLongException


class CheerAction():

    def __init__(
        self,
        bitRequirement: CheerActionBitRequirement,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        actionType: CheerActionType,
        amount: int,
        durationSeconds: int,
        actionId: str,
        userId: str,
        userName: str
    ):
        if not isinstance(bitRequirement, CheerActionBitRequirement):
            raise TypeError(f'bitRequirement argument is malformed: \"{bitRequirement}\"')
        elif not isinstance(streamStatusRequirement, CheerActionStreamStatusRequirement):
            raise TypeError(f'streamStatusRequirement argument is malformed: \"{streamStatusRequirement}\"')
        elif not isinstance(actionType, CheerActionType):
            raise TypeError(f'actionType argument is malformed: \"{actionType}\"')
        elif not utils.isValidInt(amount):
            raise TypeError(f'amount argument is malformed: \"{amount}\"')
        elif amount < 1 or amount > utils.getIntMaxSafeSize():
            raise ValueError(f'amount argument is out of bounds: {amount}')
        elif not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1:
            raise ValueError(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif durationSeconds > 1209600:
            raise TimeoutDurationSecondsTooLongException(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif not utils.isValidStr(actionId):
            raise TypeError(f'actionId argument is malformed: \"{actionId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__bitRequirement: CheerActionBitRequirement = bitRequirement
        self.__streamStatusRequirement: CheerActionStreamStatusRequirement = streamStatusRequirement
        self.__actionType: CheerActionType = actionType
        self.__amount: int = amount
        self.__durationSeconds: int = durationSeconds
        self.__actionId: str = actionId
        self.__userId: str = userId
        self.__userName: str = userName

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CheerAction):
            return False

        return self.__actionId == other.__actionId and self.__userId == other.__userId

    def getActionId(self) -> str:
        return self.__actionId

    def getActionType(self) -> CheerActionType:
        return self.__actionType

    def getAmount(self) -> int:
        return self.__amount

    def getAmountStr(self) -> str:
        return locale.format_string("%d", self.__amount, grouping = True)

    def getBitRequirement(self) -> CheerActionBitRequirement:
        return self.__bitRequirement

    def getDurationSeconds(self) -> int:
        return self.__durationSeconds

    def getStreamStatusRequirement(self) -> CheerActionStreamStatusRequirement:
        return self.__streamStatusRequirement

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def __hash__(self) -> int:
        return hash((self.__actionId, self.__userId))

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'actionId': self.__actionId,
            'actionType': self.__actionType,
            'amount': self.__amount,
            'bitRequirement': self.__bitRequirement,
            'durationSeconds': self.__durationSeconds,
            'streamStatusRequirement': self.__streamStatusRequirement,
            'userId': self.__userId,
            'userName': self.__userName
        }
