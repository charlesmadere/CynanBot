from ..listener.twitchWebsocketConnectionsFinishedListener import TwitchWebsocketConnectionsFinishedListener
from ..twitchWebsocketClientInterface import TwitchWebsocketClientInterface


class StubTwitchWebsocketClient(TwitchWebsocketClientInterface):

    def setConnectionsFinishedListener(self, listener: TwitchWebsocketConnectionsFinishedListener | None):
        # this method is intentionally empty
        pass

    def start(self):
        # this method is intentionally empty
        pass
