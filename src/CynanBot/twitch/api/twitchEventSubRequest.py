from typing import Any, Dict

import CynanBot.misc.utils as utils
from CynanBot.twitch.websocket.websocketCondition import WebsocketCondition
from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from CynanBot.twitch.websocket.websocketTransport import WebsocketTransport


# This class intends to directly correspond to Twitch's "Create EventSub Subscription" API:
# https://dev.twitch.tv/docs/api/reference/#create-eventsub-subscription
class TwitchEventSubRequest():

    def __init__(
        self,
        condition: WebsocketCondition,
        subscriptionType: WebsocketSubscriptionType,
        transport: WebsocketTransport
    ):
        if not isinstance(condition, WebsocketCondition):
            raise ValueError(f'condition argument is malformed: \"{condition}\"')
        elif not isinstance(subscriptionType, WebsocketSubscriptionType):
            raise ValueError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')
        elif not isinstance(transport, WebsocketTransport):
            raise ValueError(f'transport argument is malformed: \"{transport}\"')

        self.__condition: WebsocketCondition = condition
        self.__subscriptionType: WebsocketSubscriptionType = subscriptionType
        self.__transport: WebsocketTransport = transport

    def getCondition(self) -> WebsocketCondition:
        return self.__condition

    def getSubscriptionType(self) -> WebsocketSubscriptionType:
        return self.__subscriptionType

    def getTransport(self) -> WebsocketTransport:
        return self.__transport

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'condition': self.__condition.toDictionary(),
            'subscriptionType': self.__subscriptionType,
            'transport': self.__transport.toDictionary(),
        }

    def toJson(self) -> Dict[str, Any]:
        dictionary: Dict[str, Any] = {
            'transport': {
                'method': self.__transport.getMethod().toStr(),
                'session_id': self.__transport.requireSessionId()
            },
            'type': self.__subscriptionType.toStr(),
            'version': self.__subscriptionType.getVersion()
        }

        condition: Dict[str, Any] = dict()
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
