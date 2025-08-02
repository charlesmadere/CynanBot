import random

from ..models.randomExponentialTimeoutDuration import RandomExponentialTimeoutDuration


class DetermineExponentialTimeoutDurationSecondsUseCase:

    async def invoke(
        self,
        timeoutDuration: RandomExponentialTimeoutDuration,
    ) -> int:
        if not isinstance(timeoutDuration, RandomExponentialTimeoutDuration):
            raise TypeError(f'timeoutDuration argument is malformed: \"{timeoutDuration}\"')

        maxFloat = float(timeoutDuration.maximumSeconds)
        minFloat = float(timeoutDuration.minimumSeconds)
        timeoutScale = timeoutDuration.scale
        randomScale = random.random()

        return round(pow(randomScale, timeoutScale) * (maxFloat - minFloat) + minFloat)
