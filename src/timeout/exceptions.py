from typing import Final

from .models.bananaTimeoutTarget import BananaTimeoutTarget
from .models.timeoutDiceRoll import TimeoutDiceRoll


class BananaTimeoutDiceRollFailedException(Exception):

    def __init__(
        self,
        timeoutTarget: BananaTimeoutTarget,
        diceRoll: TimeoutDiceRoll,
    ):
        if not isinstance(timeoutTarget, BananaTimeoutTarget):
            raise TypeError(f'timeoutTarget argument is malformed: \"{timeoutTarget}\"')
        elif not isinstance(diceRoll, TimeoutDiceRoll):
            raise TypeError(f'diceRoll argument is malformed: \"{diceRoll}\"')

        self.__timeoutTarget: Final[BananaTimeoutTarget] = timeoutTarget
        self.__diceRoll: Final[TimeoutDiceRoll] = diceRoll

    @property
    def diceRoll(self) -> TimeoutDiceRoll:
        return self.__diceRoll

    @property
    def timeoutTarget(self) -> BananaTimeoutTarget:
        return self.__timeoutTarget


class UnknownTimeoutActionTypeException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class UnknownTimeoutTargetException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
