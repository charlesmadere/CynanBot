from dataclasses import dataclass

from .twitchWebsocketCondition import TwitchWebsocketCondition
from .twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from .twitchWebsocketTransport import TwitchWebsocketTransport


# This class intends to directly correspond to Twitch's "Create EventSub Subscription" API:
# https://dev.twitch.tv/docs/api/reference/#create-eventsub-subscription
@dataclass(frozen = True)
class TwitchEventSubRequest:
    condition: TwitchWebsocketCondition
    subscriptionType: TwitchWebsocketSubscriptionType
    transport: TwitchWebsocketTransport
