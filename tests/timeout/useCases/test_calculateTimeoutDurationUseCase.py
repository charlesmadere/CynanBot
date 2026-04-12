from typing import Final

import pytest

from src.timeout.models.exactTimeoutDuration import ExactTimeoutDuration
from src.timeout.models.randomExponentialTimeoutDuration import RandomExponentialTimeoutDuration
from src.timeout.models.randomLinearTimeoutDuration import RandomLinearTimeoutDuration
from src.timeout.useCases.calculateTimeoutDurationUseCase import CalculateTimeoutDurationUseCase
from src.timeout.useCases.calculateTimeoutDurationUseCaseInterface import CalculateTimeoutDurationUseCaseInterface


class TestCalculateTimeoutDurationUseCase:

    useCase: Final[CalculateTimeoutDurationUseCaseInterface] = CalculateTimeoutDurationUseCase()

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
            scale = float(9),
            maximumSeconds = 300,
            minimumSeconds = 30,
        )

        for _ in range(100):
            calculatedTimeoutDuration = await self.useCase.invoke(
                timeoutDuration = timeoutDuration,
            )

            assert calculatedTimeoutDuration.seconds >= timeoutDuration.minimumSeconds
            assert calculatedTimeoutDuration.seconds <= timeoutDuration.maximumSeconds

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
