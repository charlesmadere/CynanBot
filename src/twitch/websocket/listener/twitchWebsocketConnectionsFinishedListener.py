from abc import ABC, abstractmethod


class TwitchWebsocketConnectionsFinishedListener(ABC):

    @abstractmethod
    async def onWebsocketConnectionsFinished(self):
        pass
