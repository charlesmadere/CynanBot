from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.twitch.websocket.twitchWebsocketDataBundleListener import \
    TwitchWebsocketDataBundleListener


class TwitchWebsocketClientInterface(ABC):

    @abstractmethod
    def setDataBundleListener(self, listener: Optional[TwitchWebsocketDataBundleListener]):
        pass

    @abstractmethod
    def start(self):
        pass
