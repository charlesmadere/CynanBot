from abc import ABC, abstractmethod

from .listener.twitchWebsocketConnectionsFinishedListener import TwitchWebsocketConnectionsFinishedListener
from .listener.twitchWebsocketDataBundleListener import TwitchWebsocketDataBundleListener
from ...misc.startable import Startable


class TwitchWebsocketClientInterface(Startable, ABC):

    @abstractmethod
    def setConnectionsFinishedListener(self, listener: TwitchWebsocketConnectionsFinishedListener | None):
        pass

    @abstractmethod
    def setDataBundleListener(self, listener: TwitchWebsocketDataBundleListener | None):
        pass
