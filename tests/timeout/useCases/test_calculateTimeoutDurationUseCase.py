from collections import OrderedDict
from typing import Final

import pytest

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.timeout.models.exactTimeoutDuration import ExactTimeoutDuration
from src.timeout.models.randomExponentialTimeoutDuration import RandomExponentialTimeoutDuration
from src.timeout.models.randomLinearTimeoutDuration import RandomLinearTimeoutDuration
from src.timeout.useCases.calculateTimeoutDurationUseCase import CalculateTimeoutDurationUseCase
from src.timeout.useCases.calculateTimeoutDurationUseCaseInterface import CalculateTimeoutDurationUseCaseInterface


class TestCalculateTimeoutDurationUseCase:

    useCase: Final[CalculateTimeoutDurationUseCaseInterface] = CalculateTimeoutDurationUseCase()

    timber: Final[TimberInterface] = TimberStub()

    @pytest.mark.asyncio
    async def test_invoke_withExactTimeoutDuration(self):
        timeoutDuration = ExactTimeoutDuration(
            seconds = 30,
        )

        for _ in range(100):
            calculatedTimeoutDuration = await self.useCase.invoke(
                timeoutDuration = timeoutDuration,
            )

            assert calculatedTimeoutDuration.seconds == timeoutDuration.seconds

    @pytest.mark.asyncio
    async def test_invoke_withRandomExponentialTimeoutDuration(self):
        timeoutDuration = RandomExponentialTimeoutDuration(
            scale = float(12),
            maximumSeconds = 300,
            minimumSeconds = 30,
        )

        # this dictionary is just used for debugging purposes, it will
        # help us understand the distribution of timeout duration amounts
        timeoutDistribution: dict[int, int] = OrderedDict()

        index = timeoutDuration.minimumSeconds
        while index <= timeoutDuration.maximumSeconds:
            timeoutDistribution[index] = 0
            index += 1

        for _ in range(1000):
            calculatedTimeoutDuration = await self.useCase.invoke(
                timeoutDuration = timeoutDuration,
            )

            assert calculatedTimeoutDuration.seconds >= timeoutDuration.minimumSeconds
            assert calculatedTimeoutDuration.seconds <= timeoutDuration.maximumSeconds

            timeoutDistribution[calculatedTimeoutDuration.seconds] = timeoutDistribution[calculatedTimeoutDuration.seconds] + 1

        self.timber.log('TestCalculateTimeoutDurationUseCase', f'RandomExponentialTimeoutDuration distribution:\n{timeoutDistribution}')

    @pytest.mark.asyncio
    async def test_invoke_withRandomLinearTimeoutDuration(self):
        timeoutDuration = RandomLinearTimeoutDuration(
            maximumSeconds = 300,
            minimumSeconds = 30,
        )

        for _ in range(100):
            calculatedTimeoutDuration = await self.useCase.invoke(
                timeoutDuration = timeoutDuration,
            )

            assert calculatedTimeoutDuration.seconds >= timeoutDuration.minimumSeconds
            assert calculatedTimeoutDuration.seconds <= timeoutDuration.maximumSeconds

    def test_sanity(self):
        assert self.useCase is not None
        assert isinstance(self.useCase, CalculateTimeoutDurationUseCase)
