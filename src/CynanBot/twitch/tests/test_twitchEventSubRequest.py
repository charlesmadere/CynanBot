from typing import Dict

from CynanBot.twitch.twitchEventSubRequest import TwitchEventSubRequest
from CynanBot.twitch.websocket.websocketCondition import WebsocketCondition
from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from CynanBot.twitch.websocket.websocketTransport import WebsocketTransport
from CynanBot.twitch.websocket.websocketTransportMethod import \
    WebsocketTransportMethod


class TestTwitchEventSubRequest():

    def test_toJson1(self):
        condition = WebsocketCondition(
            broadcasterUserId = 'abc123'
        )

        subscriptionType = WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION

        transport = WebsocketTransport(
            method = WebsocketTransportMethod.WEBSOCKET,
            sessionId = 'qwerty'
        )

        request = TwitchEventSubRequest(
            condition = condition,
            subscriptionType = subscriptionType,
            transport = transport
        )

        dictionary = request.toJson()

        assert isinstance(dictionary, Dict)

        assert 'condition' in dictionary
        assert 'broadcaster_user_id' in dictionary['condition']
        assert condition.getBroadcasterUserId() == dictionary['condition']['broadcaster_user_id']
        assert 'client_id' not in dictionary['condition']
        assert 'from_broadcaster_user_id' not in dictionary['condition']
        assert 'moderator_user_id' not in dictionary['condition']
        assert 'reward_id' not in dictionary['condition']
        assert 'to_broadcaster_user_id' not in dictionary['condition']
        assert 'user_id' not in dictionary['condition']

        assert 'transport' in dictionary
        assert 'method' in dictionary['transport']
        assert dictionary['transport']['method'] == transport.getMethod().toStr()
        assert 'session_id' in dictionary['transport']
        assert dictionary['transport']['session_id'] == transport.getSessionId()

        assert 'type' in dictionary
        assert dictionary['type'] == subscriptionType.toStr()

        assert 'version' in dictionary
        assert dictionary['version'] == subscriptionType.getVersion()

    def test_toJson2(self):
        condition = WebsocketCondition(
            broadcasterUserId = 'def987'
        )

        subscriptionType = WebsocketSubscriptionType.SUBSCRIBE

        transport = WebsocketTransport(
            method = WebsocketTransportMethod.WEBSOCKET,
            sessionId = 'azerty'
        )

        request = TwitchEventSubRequest(
            condition = condition,
            subscriptionType = subscriptionType,
            transport = transport
        )

        dictionary = request.toJson()

        assert isinstance(dictionary, Dict)

        assert 'condition' in dictionary
        assert 'broadcaster_user_id' in dictionary['condition']
        assert condition.getBroadcasterUserId() == dictionary['condition']['broadcaster_user_id']
        assert 'client_id' not in dictionary['condition']
        assert 'from_broadcaster_user_id' not in dictionary['condition']
        assert 'moderator_user_id' not in dictionary['condition']
        assert 'reward_id' not in dictionary['condition']
        assert 'to_broadcaster_user_id' not in dictionary['condition']
        assert 'user_id' not in dictionary['condition']

        assert 'transport' in dictionary
        assert 'method' in dictionary['transport']
        assert dictionary['transport']['method'] == transport.getMethod().toStr()
        assert 'session_id' in dictionary['transport']
        assert dictionary['transport']['session_id'] == transport.getSessionId()

        assert 'type' in dictionary
        assert dictionary['type'] == subscriptionType.toStr()

        assert 'version' in dictionary
        assert dictionary['version'] == subscriptionType.getVersion()

    def test_toJson3(self):
        condition = WebsocketCondition(
            broadcasterUserId = 'foo',
            moderatorUserId = 'bar'
        )

        subscriptionType = WebsocketSubscriptionType.SUBSCRIBE

        transport = WebsocketTransport(
            method = WebsocketTransportMethod.WEBSOCKET,
            sessionId = 'azerty'
        )

        request = TwitchEventSubRequest(
            condition = condition,
            subscriptionType = subscriptionType,
            transport = transport
        )

        dictionary = request.toJson()

        assert isinstance(dictionary, Dict)

        assert 'condition' in dictionary
        assert 'broadcaster_user_id' in dictionary['condition']
        assert condition.getBroadcasterUserId() == dictionary['condition']['broadcaster_user_id']
        assert 'client_id' not in dictionary['condition']
        assert 'from_broadcaster_user_id' not in dictionary['condition']
        assert 'moderator_user_id' in dictionary['condition']
        assert condition.getModeratorUserId() == dictionary['condition']['moderator_user_id']
        assert 'reward_id' not in dictionary['condition']
        assert 'to_broadcaster_user_id' not in dictionary['condition']
        assert 'user_id' not in dictionary['condition']

        assert 'transport' in dictionary
        assert 'method' in dictionary['transport']
        assert dictionary['transport']['method'] == transport.getMethod().toStr()
        assert 'session_id' in dictionary['transport']
        assert dictionary['transport']['session_id'] == transport.getSessionId()

        assert 'type' in dictionary
        assert dictionary['type'] == subscriptionType.toStr()

        assert 'version' in dictionary
        assert dictionary['version'] == subscriptionType.getVersion()
