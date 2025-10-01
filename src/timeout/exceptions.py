from typing import Final

from .models.timeoutDiceRoll import TimeoutDiceRoll
from .models.timeoutDiceRollFailureData import TimeoutDiceRollFailureData
from .models.timeoutTarget import TimeoutTarget


class BananaTimeoutDiceRollFailedException(Exception):

    def __init__(
        self,
        diceRoll: TimeoutDiceRoll,
        diceRollFailureData: TimeoutDiceRollFailureData,
        timeoutTarget: TimeoutTarget,
    ):
        super().__init__(diceRoll, diceRollFailureData, timeoutTarget)
        self.__diceRoll: Final[TimeoutDiceRoll] = diceRoll
        self.__diceRollFailureData: Final[TimeoutDiceRollFailureData] = diceRollFailureData
        self.__timeoutTarget: Final[TimeoutTarget] = timeoutTarget

    @property
    def diceRoll(self) -> TimeoutDiceRoll:
        return self.__diceRoll

    @property
    def diceRollFailureData(self) -> TimeoutDiceRollFailureData:
        return self.__diceRollFailureData

    @property
    def timeoutTarget(self) -> TimeoutTarget:
        return self.__timeoutTarget


class ImmuneTimeoutTargetException(Exception):

    def __init__(
        self,
        timeoutTarget: TimeoutTarget,
    ):
        super().__init__(timeoutTarget)
        self.__timeoutTarget: Final[TimeoutTarget] = timeoutTarget

    @property
    def timeoutTarget(self) -> TimeoutTarget:
        return self.__timeoutTarget


class UnknownTimeoutActionTypeException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class UnknownTimeoutTargetException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
