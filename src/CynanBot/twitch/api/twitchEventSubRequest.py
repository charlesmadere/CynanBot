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
class TwitchEventSubRequest():

    def __init__(
        self,
        condition: TwitchWebsocketCondition,
        subscriptionType: TwitchWebsocketSubscriptionType,
        transport: TwitchWebsocketTransport
    ):
        if not isinstance(condition, TwitchWebsocketCondition):
            raise TypeError(f'condition argument is malformed: \"{condition}\"')
        elif not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')
        elif not isinstance(transport, TwitchWebsocketTransport):
            raise TypeError(f'transport argument is malformed: \"{transport}\"')

        self.__condition: TwitchWebsocketCondition = condition
        self.__subscriptionType: TwitchWebsocketSubscriptionType = subscriptionType
        self.__transport: TwitchWebsocketTransport = transport

    def getCondition(self) -> TwitchWebsocketCondition:
        return self.__condition

    def getSubscriptionType(self) -> TwitchWebsocketSubscriptionType:
        return self.__subscriptionType

    def getTransport(self) -> TwitchWebsocketTransport:
        return self.__transport

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'condition': self.__condition.toDictionary(),
            'subscriptionType': self.__subscriptionType,
            'transport': self.__transport.toDictionary(),
        }

    def toJson(self) -> dict[str, Any]:
        dictionary: dict[str, Any] = {
            'transport': {
                'method': self.__transport.method.toStr(),
                'session_id': self.__transport.requireSessionId()
            },
            'type': self.__subscriptionType.toStr(),
            'version': self.__subscriptionType.getVersion()
        }

        condition: dict[str, Any] = dict()
        dictionary['condition'] = condition

        if utils.isValidStr(self.__condition.getBroadcasterUserId()):
            condition['broadcaster_user_id'] = self.__condition.requireBroadcasterUserId()

        if utils.isValidStr(self.__condition.getClientId()):
            condition['client_id'] = self.__condition.requireClientId()

        if utils.isValidStr(self.__condition.getFromBroadcasterUserId()):
            condition['from_broadcaster_user_id'] = self.__condition.requireFromBroadcasterUserId()

        if utils.isValidStr(self.__condition.getModeratorUserId()):
            condition['moderator_user_id'] = self.__condition.requireModeratorUserId()

        if utils.isValidStr(self.__condition.getRewardId()):
            condition['reward_id'] = self.__condition.requireRewardId()

        if utils.isValidStr(self.__condition.getToBroadcasterUserId()):
            condition['to_broadcaster_user_id'] = self.__condition.requireToBroadcasterUserId()

        if utils.isValidStr(self.__condition.getUserId()):
            condition['user_id'] = self.__condition.requireUserId()

        return dictionary
