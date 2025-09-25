from typing import Final

from .models.bananaTimeoutTarget import BananaTimeoutTarget
from .models.timeoutDiceRoll import TimeoutDiceRoll
from .models.timeoutDiceRollFailureData import TimeoutDiceRollFailureData
from .models.voreTimeoutTarget import VoreTimeoutTarget


class BananaTimeoutDiceRollFailedException(Exception):

    def __init__(
        self,
        timeoutTarget: BananaTimeoutTarget,
        diceRoll: TimeoutDiceRoll,
        diceRollFailureData: TimeoutDiceRollFailureData,
    ):
        if not isinstance(timeoutTarget, BananaTimeoutTarget):
            raise TypeError(f'timeoutTarget argument is malformed: \"{timeoutTarget}\"')
        elif not isinstance(diceRoll, TimeoutDiceRoll):
            raise TypeError(f'diceRoll argument is malformed: \"{diceRoll}\"')
        elif not isinstance(diceRollFailureData, TimeoutDiceRollFailureData):
            raise TypeError(f'diceRollFailureData argument is malformed: \"{diceRollFailureData}\"')

        self.__timeoutTarget: Final[BananaTimeoutTarget] = timeoutTarget
        self.__diceRoll: Final[TimeoutDiceRoll] = diceRoll
        self.__diceRollFailureData: Final[TimeoutDiceRollFailureData] = diceRollFailureData

    @property
    def diceRoll(self) -> TimeoutDiceRoll:
        return self.__diceRoll

    @property
    def diceRollFailureData(self) -> TimeoutDiceRollFailureData:
        return self.__diceRollFailureData

    @property
    def timeoutTarget(self) -> BananaTimeoutTarget:
        return self.__timeoutTarget


class ImmuneTimeoutTargetException(Exception):

    def __init__(
        self,
        timeoutTarget: VoreTimeoutTarget,
    ):
        if not isinstance(timeoutTarget, VoreTimeoutTarget):
            raise TypeError(f'timeoutTarget argument is malformed: \"{timeoutTarget}\"')

        self.__timeoutTarget: Final[VoreTimeoutTarget] = timeoutTarget

    @property
    def timeoutTarget(self) -> VoreTimeoutTarget:
        return self.__timeoutTarget


class UnknownTimeoutActionTypeException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class UnknownTimeoutTargetException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
