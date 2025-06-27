from dataclasses import dataclass
from datetime import datetime

from .twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod
from ....misc import utils as utils


# This class intends to directly correspond to the "transport" field from Twitch's "Create
# EventSub Subscription" API: https://dev.twitch.tv/docs/api/reference/#create-eventsub-subscription
@dataclass(frozen = True)
class TwitchWebsocketTransport:
    connectedAt: datetime | None
    disconnectedAt: datetime | None
    callbackUrl: str | None
    conduitId: str | None
    secret: str | None
    sessionId: str | None
    method: TwitchWebsocketTransportMethod

    def requireCallbackUrl(self) -> str:
        if not utils.isValidUrl(self.callbackUrl):
            raise ValueError(f'callbackUrl has not been set: \"{self}\"')

        return self.callbackUrl

    def requireConduitId(self) -> str:
        if not utils.isValidStr(self.conduitId):
            raise ValueError(f'conduitId has not been set: \"{self}\"')

        return self.conduitId

    def requireSecret(self) -> str:
        if not utils.isValidStr(self.secret):
            raise ValueError(f'secret argument has not been set: \"{self}\"')

        return self.secret

    def requireSessionId(self) -> str:
        if not utils.isValidStr(self.sessionId):
            raise ValueError(f'sessionId has not been set: \"{self}\"')

        return self.sessionId
