from abc import ABC, abstractmethod

from .crowdControlMessage import CrowdControlMessage


class CrowdControlMessageListener(ABC):

    @abstractmethod
    async def onNewCrowdControlMessage(self, crowdControlMessage: CrowdControlMessage):
        pass
