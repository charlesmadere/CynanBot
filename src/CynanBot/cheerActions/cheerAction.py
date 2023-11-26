import locale
from typing import Any, Dict

import CynanBot.misc.utils as utils
from CynanBot.cheerActions.cheerActionRequirement import CheerActionRequirement
from CynanBot.cheerActions.cheerActionType import CheerActionType
from CynanBot.cheerActions.exceptions import \
    TimeoutDurationSecondsTooLongException


class CheerAction():

    def __init__(
        self,
        actionRequirement: CheerActionRequirement,
        actionType: CheerActionType,
        amount: int,
        durationSeconds: int,
        actionId: str,
        userId: str,
        userName: str
    ):
        if not isinstance(actionRequirement, CheerActionRequirement):
            raise ValueError(f'actionRequirement argument is malformed: \"{actionRequirement}\"')
        elif not isinstance(actionType, CheerActionType):
            raise ValueError(f'actionType argument is malformed: \"{actionType}\"')
        elif not utils.isValidInt(amount):
            raise ValueError(f'amount argument is malformed: \"{amount}\"')
        elif amount < 1 or amount > utils.getIntMaxSafeSize():
            raise ValueError(f'amount argument is out of bounds: {amount}')
        elif not utils.isValidInt(durationSeconds):
            raise ValueError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1:
            raise ValueError(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif durationSeconds > 1209600:
            raise TimeoutDurationSecondsTooLongException(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif not utils.isValidStr(actionId):
            raise ValueError(f'actionId argument is malformed: \"{actionId}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__actionRequirement: CheerActionRequirement = actionRequirement
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

    def getActionRequirement(self) -> CheerActionRequirement:
        return self.__actionRequirement

    def getActionType(self) -> CheerActionType:
        return self.__actionType

    def getAmount(self) -> int:
        return self.__amount

    def getAmountStr(self) -> str:
        return locale.format_string("%d", self.__amount, grouping = True)

    def getDurationSeconds(self) -> int:
        return self.__durationSeconds

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def __hash__(self) -> int:
        return hash((self.__actionId, self.__userId))

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'actionId': self.__actionId,
            'actionRequirement': self.__actionRequirement,
            'actionType': self.__actionType,
            'amount': self.__amount,
            'durationSeconds': self.__durationSeconds,
            'userId': self.__userId,
            'userName': self.__userName
        }
