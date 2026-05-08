from abc import ABC, abstractmethod

from typing import Collection


class TwitchWebsocketConnectionsFinishedListener(ABC):

    @abstractmethod
    async def onWebsocketConnectionsFinished(self, userIds: Collection[str]):
        pass
