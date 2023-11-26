from abc import ABC, abstractmethod

from CynanBot.twitch.websocket.websocketDataBundle import WebsocketDataBundle


class TwitchWebsocketDataBundleListener(ABC):

    @abstractmethod
    async def onNewWebsocketDataBundle(self, dataBundle: WebsocketDataBundle):
        pass
