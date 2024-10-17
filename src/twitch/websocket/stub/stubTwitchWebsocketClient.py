from ..twitchWebsocketClientInterface import TwitchWebsocketClientInterface
from ..twitchWebsocketDataBundleListener import TwitchWebsocketDataBundleListener


class StubTwitchWebsocketClient(TwitchWebsocketClientInterface):

    def setDataBundleListener(self, listener: TwitchWebsocketDataBundleListener | None):
        # this method is intentionally empty
        pass

    def start(self):
        # this method is intentionally empty
        pass
