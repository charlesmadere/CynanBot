from abc import ABC, abstractmethod
from typing import Any

from ..actions.crowdControlButton import CrowdControlButton


class CrowdControlUserInputUtilsInterface(ABC):

    @abstractmethod
    async def parseButtonFromUserInput(
        self,
        userInput: str | Any | None,
    ) -> CrowdControlButton | None:
        pass
