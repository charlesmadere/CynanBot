from ..listener.twitchWebsocketConnectionsFinishedListener import TwitchWebsocketConnectionsFinishedListener
from ..listener.twitchWebsocketDataBundleListener import TwitchWebsocketDataBundleListener
from ..twitchWebsocketClientInterface import TwitchWebsocketClientInterface


class StubTwitchWebsocketClient(TwitchWebsocketClientInterface):

    def setConnectionsFinishedListener(self, listener: TwitchWebsocketConnectionsFinishedListener | None):
        # this method is intentionally empty
        pass

    def setDataBundleListener(self, listener: TwitchWebsocketDataBundleListener | None):
        # this method is intentionally empty
        pass

    def start(self):
        # this method is intentionally empty
        pass
