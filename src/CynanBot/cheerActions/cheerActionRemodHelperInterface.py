from abc import ABC, abstractmethod

from CynanBot.cheerActions.cheerActionRemodData import CheerActionRemodData


class CheerActionRemodHelperInterface(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    async def submitRemodData(self, action: CheerActionRemodData):
        pass
