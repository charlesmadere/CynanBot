from abc import ABC, abstractmethod

from ..models.absTimeoutDuration import AbsTimeoutDuration
from ..models.calculatedTimeoutDuration import CalculatedTimeoutDuration


class CalculateTimeoutDurationUseCaseInterface(ABC):

    @abstractmethod
    async def invoke(
        self,
        timeoutDuration: AbsTimeoutDuration,
    ) -> CalculatedTimeoutDuration:
        pass
