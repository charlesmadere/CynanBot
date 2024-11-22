from abc import ABC, abstractmethod

from .crowdControlMessage import CrowdControlMessage


class CrowdControlMessagePresenterInterface(ABC):

    @abstractmethod
    async def toString(self, message: CrowdControlMessage) -> str | None:
        pass
