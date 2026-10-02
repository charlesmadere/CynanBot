from typing import Final

from .calculateTimeoutDurationUseCaseInterface import CalculateTimeoutDurationUseCaseInterface
from ..models.absTimeoutDuration import AbsTimeoutDuration
from ..models.calculatedTimeoutDuration import CalculatedTimeoutDuration
from ..models.exactTimeoutDuration import ExactTimeoutDuration
from ..models.randomExponentialTimeoutDuration import RandomExponentialTimeoutDuration
from ..models.randomLinearTimeoutDuration import RandomLinearTimeoutDuration
from ...misc import utils as utils
from ...misc.randomUtilsInterface import RandomUtilsInterface


class CalculateTimeoutDurationUseCase(CalculateTimeoutDurationUseCaseInterface):

    def __init__(self, randomUtils: RandomUtilsInterface):
        if not isinstance(randomUtils, RandomUtilsInterface):
            raise TypeError(f'randomUtils argument is malformed: \"{randomUtils}\"')

        self.__randomUtils: Final[RandomUtilsInterface] = randomUtils

    async def __calculateExactTimeoutDurationSeconds(
        self,
        timeoutDuration: ExactTimeoutDuration,
    ) -> int:
        if not isinstance(timeoutDuration, ExactTimeoutDuration):
            raise TypeError(f'timeoutDuration argument is malformed: \"{timeoutDuration}\"')

        return timeoutDuration.seconds

    async def __calculateExponentialTimeoutDurationSeconds(
        self,
        timeoutDuration: RandomExponentialTimeoutDuration,
    ) -> int:
        if not isinstance(timeoutDuration, RandomExponentialTimeoutDuration):
            raise TypeError(f'timeoutDuration argument is malformed: \"{timeoutDuration}\"')

        maxSeconds = float(timeoutDuration.maximumSeconds)
        minSeconds = float(timeoutDuration.minimumSeconds)
        randomScale = self.__randomUtils.float()

        timeoutDurationSeconds = pow(randomScale, timeoutDuration.exponent) * (maxSeconds - minSeconds) + minSeconds
        return int(round(timeoutDurationSeconds))

    async def __calculateLinearTimeoutDurationSeconds(
        self,
        timeoutDuration: RandomLinearTimeoutDuration,
    ) -> int:
        if not isinstance(timeoutDuration, RandomLinearTimeoutDuration):
            raise TypeError(f'timeoutDuration argument is malformed: \"{timeoutDuration}\"')

        return self.__randomUtils.int(
            low = timeoutDuration.minimumSeconds,
            high = timeoutDuration.maximumSeconds,
        )

    async def invoke(
        self,
        timeoutDuration: AbsTimeoutDuration,
    ) -> CalculatedTimeoutDuration:
        if not isinstance(timeoutDuration, AbsTimeoutDuration):
            raise TypeError(f'timeoutDuration argument is malformed: \"{timeoutDuration}\"')

        durationSeconds: int

        if isinstance(timeoutDuration, ExactTimeoutDuration):
            durationSeconds = await self.__calculateExactTimeoutDurationSeconds(
                timeoutDuration = timeoutDuration,
            )

        elif isinstance(timeoutDuration, RandomExponentialTimeoutDuration):
            durationSeconds = await self.__calculateExponentialTimeoutDurationSeconds(
                timeoutDuration = timeoutDuration,
            )

        elif isinstance(timeoutDuration, RandomLinearTimeoutDuration):
            durationSeconds = await self.__calculateLinearTimeoutDurationSeconds(
                timeoutDuration = timeoutDuration,
            )

        else:
            raise ValueError(f'Encountered unknown AbsTimeoutDuration type: \"{timeoutDuration}\"')

        message = utils.secondsToDurationMessage(
            secondsDuration = durationSeconds,
            includeMinutesAndSeconds = True,
        )

        return CalculatedTimeoutDuration(
            seconds = durationSeconds,
            message = message,
        )
