from dataclasses import dataclass

from .websocket.twitchWebsocketCondition import TwitchWebsocketCondition
from .websocket.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from .websocket.twitchWebsocketTransport import TwitchWebsocketTransport


# This class intends to directly correspond to Twitch's "Create EventSub Subscription" API:
# https://dev.twitch.tv/docs/api/reference/#create-eventsub-subscription
@dataclass(frozen = True)
class TwitchEventSubRequest:
    condition: TwitchWebsocketCondition
    subscriptionType: TwitchWebsocketSubscriptionType
    transport: TwitchWebsocketTransport
