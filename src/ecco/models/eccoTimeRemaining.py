from datetime import datetime

from .absEccoTimeRemaining import AbsEccoTimeRemaining
from .eccoTimeRemainingType import EccoTimeRemainingType
from ...misc import utils as utils


class EccoTimeRemaining(AbsEccoTimeRemaining):

    def __init__(
        self,
        timerDateTime: datetime,
        remainingSeconds: int
    ):
        if not isinstance(timerDateTime, datetime):
            raise TypeError(f'timerDateTime argument is malformed: \"{timerDateTime}\"')
        elif not utils.isValidInt(remainingSeconds):
            raise TypeError(f'remainingSeconds argument is malformed: \"{remainingSeconds}\"')
        elif remainingSeconds < 0 or remainingSeconds > utils.getLongMaxSafeSize():
            raise ValueError(f'remainingSeconds argument is out of bounds: {remainingSeconds}')

        self.__timerDateTime: datetime = timerDateTime
        self.__remainingSeconds: int = remainingSeconds

    @property
    def remainingSeconds(self) -> int:
        return self.__remainingSeconds

    @property
    def timerDateTime(self) -> datetime:
        return self.__timerDateTime

    @property
    def timeRemainingType(self) -> EccoTimeRemainingType:
        return EccoTimeRemainingType.TIME_REMAINING
