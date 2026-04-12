import random

from .calculateTimeoutDurationUseCaseInterface import CalculateTimeoutDurationUseCaseInterface
from ..models.absTimeoutDuration import AbsTimeoutDuration
from ..models.calculatedTimeoutDuration import CalculatedTimeoutDuration
from ..models.exactTimeoutDuration import ExactTimeoutDuration
from ..models.randomExponentialTimeoutDuration import RandomExponentialTimeoutDuration
from ..models.randomLinearTimeoutDuration import RandomLinearTimeoutDuration
from ...misc import utils as utils


class CalculateTimeoutDurationUseCase(CalculateTimeoutDurationUseCaseInterface):

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

        maxFloat = float(timeoutDuration.maximumSeconds)
        minFloat = float(timeoutDuration.minimumSeconds)
        randomScale = random.random()

        timeoutDurationSeconds = pow(randomScale, timeoutDuration.scale) * (maxFloat - minFloat) + minFloat
        return int(round(timeoutDurationSeconds))

    async def __calculateLinearTimeoutDurationSeconds(
        self,
        timeoutDuration: RandomLinearTimeoutDuration,
    ) -> int:
        if not isinstance(timeoutDuration, RandomLinearTimeoutDuration):
            raise TypeError(f'timeoutDuration argument is malformed: \"{timeoutDuration}\"')

        return random.randint(timeoutDuration.minimumSeconds, timeoutDuration.maximumSeconds)

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
