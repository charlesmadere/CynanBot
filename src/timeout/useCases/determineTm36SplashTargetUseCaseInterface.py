from abc import ABC, abstractmethod
from typing import Collection

from ..models.actions.tm36TimeoutAction import Tm36TimeoutAction
from ..models.timeoutTarget import TimeoutTarget


class DetermineTm36SplashTargetUseCaseInterface(ABC):

    @abstractmethod
    async def invoke(
        self,
        timeoutAction: Tm36TimeoutAction,
    ) -> Collection[TimeoutTarget]:
        pass
