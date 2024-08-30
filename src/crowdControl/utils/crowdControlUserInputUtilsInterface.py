from abc import ABC, abstractmethod

from ..actions.crowdControlButton import CrowdControlButton


class CrowdControlUserInputUtilsInterface(ABC):

    @abstractmethod
    async def parseButtonFromUserInput(
        self,
        userInput: str | None
    ) -> CrowdControlButton | None:
        pass
