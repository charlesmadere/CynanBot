from abc import ABC, abstractmethod

from ..actions.crowdControlButton import CrowdControlButton
from ...users.crowdControl.crowdControlInputType import CrowdControlInputType


class CrowdControlInputTypeMapperInterface(ABC):

    @abstractmethod
    async def toButton(
        self,
        inputType: CrowdControlInputType | None,
    ) -> CrowdControlButton | None:
        pass
