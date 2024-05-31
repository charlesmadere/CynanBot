from dataclasses import dataclass
from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.twitch.api.websocket.twitchWebsocketCondition import \
    TwitchWebsocketCondition
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
from CynanBot.twitch.api.websocket.twitchWebsocketTransport import \
    TwitchWebsocketTransport


# This class intends to directly correspond to Twitch's "Create EventSub Subscription" API:
# https://dev.twitch.tv/docs/api/reference/#create-eventsub-subscription
@dataclass(frozen = True)
class TwitchEventSubRequest():
    condition: TwitchWebsocketCondition
    subscriptionType: TwitchWebsocketSubscriptionType
    transport: TwitchWebsocketTransport

    def toJson(self) -> dict[str, Any]:
        dictionary: dict[str, Any] = {
            'transport': {
                'method': self.transport.method.toStr(),
                'session_id': self.transport.requireSessionId()
            },
            'type': self.subscriptionType.toStr(),
            'version': self.subscriptionType.getVersion()
        }

        condition: dict[str, Any] = dict()
        dictionary['condition'] = condition

        if utils.isValidStr(self.condition.broadcasterUserId):
            condition['broadcaster_user_id'] = self.condition.requireBroadcasterUserId()

        if utils.isValidStr(self.condition.clientId):
            condition['client_id'] = self.condition.requireClientId()

        if utils.isValidStr(self.condition.fromBroadcasterUserId):
            condition['from_broadcaster_user_id'] = self.condition.requireFromBroadcasterUserId()

        if utils.isValidStr(self.condition.moderatorUserId):
            condition['moderator_user_id'] = self.condition.requireModeratorUserId()

        if utils.isValidStr(self.condition.rewardId):
            condition['reward_id'] = self.condition.requireRewardId()

        if utils.isValidStr(self.condition.toBroadcasterUserId):
            condition['to_broadcaster_user_id'] = self.condition.requireToBroadcasterUserId()

        if utils.isValidStr(self.condition.userId):
            condition['user_id'] = self.condition.requireUserId()

        return dictionary
