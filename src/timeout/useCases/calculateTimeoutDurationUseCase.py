import random

from ..models.actions.absTimeoutAction import AbsTimeoutAction
from ..models.calculatedTimeoutDuration import CalculatedTimeoutDuration
from ..models.exactTimeoutDuration import ExactTimeoutDuration
from ..models.randomExponentialTimeoutDuration import RandomExponentialTimeoutDuration
from ..models.randomLinearTimeoutDuration import RandomLinearTimeoutDuration
from ...misc import utils as utils


class CalculateTimeoutDurationUseCase:

    async def __calculateExponentialTimeoutDurationSeconds(
        self,
        timeoutDuration: RandomExponentialTimeoutDuration,
    ) -> int:
        maxFloat = float(timeoutDuration.maximumSeconds)
        minFloat = float(timeoutDuration.minimumSeconds)
        randomScale = random.random()

        timeoutDurationSeconds = pow(randomScale, timeoutDuration.scale) * (maxFloat - minFloat) + minFloat
        return int(round(timeoutDurationSeconds))

    async def invoke(
        self,
        timeoutAction: AbsTimeoutAction,
    ) -> CalculatedTimeoutDuration:
        if not isinstance(timeoutAction, AbsTimeoutAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')

        timeoutDuration = timeoutAction.getTimeoutDuration()
        durationSeconds: int

        if isinstance(timeoutDuration, ExactTimeoutDuration):
            durationSeconds = timeoutDuration.seconds

        elif isinstance(timeoutDuration, RandomExponentialTimeoutDuration):
            durationSeconds = await self.__calculateExponentialTimeoutDurationSeconds(timeoutDuration)

        elif isinstance(timeoutDuration, RandomLinearTimeoutDuration):
            durationSeconds = random.randint(timeoutDuration.minimumSeconds, timeoutDuration.maximumSeconds)

        else:
            raise ValueError(f'Encountered unknown AbsTimeoutDuration type: \"{timeoutDuration}\"')

        message = utils.secondsToDurationMessage(durationSeconds)

        return CalculatedTimeoutDuration(
            seconds = durationSeconds,
            message = message,
        )
