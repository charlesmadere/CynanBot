from abc import ABC, abstractmethod

from .listener.twitchWebsocketDataBundleListener import TwitchWebsocketDataBundleListener
from ...misc.startable import Startable


class TwitchWebsocketClientInterface(Startable, ABC):

    @abstractmethod
    def setDataBundleListener(self, listener: TwitchWebsocketDataBundleListener | None):
        pass
