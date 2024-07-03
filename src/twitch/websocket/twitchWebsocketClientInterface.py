from abc import ABC, abstractmethod

from twitch.websocket.twitchWebsocketDataBundleListener import \
    TwitchWebsocketDataBundleListener


class TwitchWebsocketClientInterface(ABC):

    @abstractmethod
    def setDataBundleListener(self, listener: TwitchWebsocketDataBundleListener | None):
        pass

    @abstractmethod
    def start(self):
        pass
