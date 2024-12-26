from abc import ABC, abstractmethod

from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle


class TwitchWebsocketDataBundleListener(ABC):

    @abstractmethod
    async def onNewWebsocketDataBundle(self, dataBundle: TwitchWebsocketDataBundle):
        pass
