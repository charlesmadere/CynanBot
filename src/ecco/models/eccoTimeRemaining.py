from .absEccoTimeRemaining import AbsEccoTimeRemaining
from .eccoTimeRemainingType import EccoTimeRemainingType
from ...misc import utils as utils


class EccoTimeRemaining(AbsEccoTimeRemaining):

    def __init__(
        self,
        hours: int,
        minutes: int,
        seconds: int
    ):
        if not utils.isValidInt(hours):
            raise TypeError(f'hours argument is malformed: \"{hours}\"')
        elif hours < 0 or hours > utils.getIntMaxSafeSize():
            raise ValueError(f'hours argument is out of bounds: {hours}')
        elif not utils.isValidInt(minutes):
            raise TypeError(f'minutes argument is malformed: \"{minutes}\"')
        elif minutes < 0 or minutes > utils.getIntMaxSafeSize():
            raise ValueError(f'minutes argument is out of bounds: {minutes}')
        elif not utils.isValidInt(seconds):
            raise TypeError(f'seconds argument is malformed: \"{seconds}\"')
        elif seconds < 0 or seconds > utils.getIntMaxSafeSize():
            raise ValueError(f'seconds argument is out of bounds: {seconds}')

        self.__hours: int = hours
        self.__minutes: int = minutes
        self.__seconds: int = seconds

    @property
    def hours(self) -> int:
        return self.__hours

    @property
    def minutes(self) -> int:
        return self.__minutes

    @property
    def seconds(self) -> int:
        return self.__seconds

    @property
    def timeRemainingType(self) -> EccoTimeRemainingType:
        return EccoTimeRemainingType.TIME_REMAINING
