from abc import ABC, abstractmethod

from ..models.actions.absTimeoutAction import AbsTimeoutAction
from ..models.timeoutTarget import TimeoutTarget


class DetermineTimeoutTargetUseCaseInterface(ABC):

    @abstractmethod
    async def invoke(
        self,
        timeoutAction: AbsTimeoutAction,
    ) -> TimeoutTarget:
        pass
