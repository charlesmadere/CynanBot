from ..models.randomExponentialTimeoutDuration import RandomExponentialTimeoutDuration


class DetermineExponentialTimeoutDurationSecondsUseCase:

    async def invoke(
        self,
        timeoutDuration: RandomExponentialTimeoutDuration,
    ) -> int:
        if not isinstance(timeoutDuration, RandomExponentialTimeoutDuration):
            raise TypeError(f'timeoutDuration argument is malformed: \"{timeoutDuration}\"')

        # TODO
        pass

        raise RuntimeError()
