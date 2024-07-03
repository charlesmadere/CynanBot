from abc import ABC, abstractmethod

from ..api.websocket.twitchWebsocketDataBundle import TwitchWebsocketDataBundle


class TwitchWebsocketDataBundleListener(ABC):

    @abstractmethod
    async def onNewWebsocketDataBundle(self, dataBundle: TwitchWebsocketDataBundle):
        pass
