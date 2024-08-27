from abc import ABC, abstractmethod

from .crowdControlInput import CrowdControlInput


class CrowdControlInputHandler(ABC):

    @abstractmethod
    async def handleInput(self, input: CrowdControlInput) -> bool:
        pass
