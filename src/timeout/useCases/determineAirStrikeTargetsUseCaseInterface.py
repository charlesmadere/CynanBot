from abc import ABC, abstractmethod

from frozenlist import FrozenList

from ..models.actions.airStrikeTimeoutAction import AirStrikeTimeoutAction
from ..models.timeoutTarget import TimeoutTarget


class DetermineAirStrikeTargetsUseCaseInterface(ABC):

    @abstractmethod
    async def invoke(
        self,
        timeoutAction: AirStrikeTimeoutAction,
    ) -> FrozenList[TimeoutTarget]:
        pass
