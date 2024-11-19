from abc import ABC, abstractmethod

from .crowdControlMessage import CrowdControlMessage


class CrowdControlMessageHandler(ABC):

    @abstractmethod
    async def sendMessage(self, crowdControlMessage: CrowdControlMessage):
        pass
