from ..listener.twitchWebsocketDataBundleListener import TwitchWebsocketDataBundleListener
from ..twitchWebsocketClientInterface import TwitchWebsocketClientInterface


class StubTwitchWebsocketClient(TwitchWebsocketClientInterface):

    def setDataBundleListener(self, listener: TwitchWebsocketDataBundleListener | None):
        # this method is intentionally empty
        pass

    def start(self):
        # this method is intentionally empty
        pass
