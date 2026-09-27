from abc import ABC, abstractmethod

from ..models.actions.grenadeTimeoutAction import GrenadeTimeoutAction
from ..models.timeoutTarget import TimeoutTarget


class DetermineGrenadeTargetUseCaseInterface(ABC):

    @abstractmethod
    async def invoke(
        self,
        timeoutAction: GrenadeTimeoutAction,
    ) -> TimeoutTarget | None:
        pass
