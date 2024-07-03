from src.twitch.api.twitchEventSubRequest import TwitchEventSubRequest
from src.twitch.api.websocket.twitchWebsocketCondition import \
    TwitchWebsocketCondition
from src.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
from src.twitch.api.websocket.twitchWebsocketTransport import \
    TwitchWebsocketTransport
from src.twitch.api.websocket.twitchWebsocketTransportMethod import \
    TwitchWebsocketTransportMethod


class TestTwitchEventSubRequest():

    def test_toJson1(self):
        condition = TwitchWebsocketCondition(
            broadcasterUserId = 'abc123'
        )

        subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION

        transport = TwitchWebsocketTransport(
            method = TwitchWebsocketTransportMethod.WEBSOCKET,
            sessionId = 'qwerty'
        )

        request = TwitchEventSubRequest(
            condition = condition,
            subscriptionType = subscriptionType,
            transport = transport
        )

        dictionary = request.toJson()

        assert isinstance(dictionary, dict)

        assert 'condition' in dictionary
        assert 'broadcaster_user_id' in dictionary['condition']
        assert condition.broadcasterUserId == dictionary['condition']['broadcaster_user_id']
        assert 'client_id' not in dictionary['condition']
        assert 'from_broadcaster_user_id' not in dictionary['condition']
        assert 'moderator_user_id' not in dictionary['condition']
        assert 'reward_id' not in dictionary['condition']
        assert 'to_broadcaster_user_id' not in dictionary['condition']
        assert 'user_id' not in dictionary['condition']

        assert 'transport' in dictionary
        assert 'method' in dictionary['transport']
        assert dictionary['transport']['method'] == transport.method.toStr()
        assert 'session_id' in dictionary['transport']
        assert dictionary['transport']['session_id'] == transport.sessionId

        assert 'type' in dictionary
        assert dictionary['type'] == subscriptionType.toStr()

        assert 'version' in dictionary
        assert dictionary['version'] == subscriptionType.getVersion()

    def test_toJson2(self):
        condition = TwitchWebsocketCondition(
            broadcasterUserId = 'def987'
        )

        subscriptionType = TwitchWebsocketSubscriptionType.SUBSCRIBE

        transport = TwitchWebsocketTransport(
            method = TwitchWebsocketTransportMethod.WEBSOCKET,
            sessionId = 'azerty'
        )

        request = TwitchEventSubRequest(
            condition = condition,
            subscriptionType = subscriptionType,
            transport = transport
        )

        dictionary = request.toJson()

        assert isinstance(dictionary, dict)

        assert 'condition' in dictionary
        assert 'broadcaster_user_id' in dictionary['condition']
        assert condition.broadcasterUserId == dictionary['condition']['broadcaster_user_id']
        assert 'client_id' not in dictionary['condition']
        assert 'from_broadcaster_user_id' not in dictionary['condition']
        assert 'moderator_user_id' not in dictionary['condition']
        assert 'reward_id' not in dictionary['condition']
        assert 'to_broadcaster_user_id' not in dictionary['condition']
        assert 'user_id' not in dictionary['condition']

        assert 'transport' in dictionary
        assert 'method' in dictionary['transport']
        assert dictionary['transport']['method'] == transport.method.toStr()
        assert 'session_id' in dictionary['transport']
        assert dictionary['transport']['session_id'] == transport.sessionId

        assert 'type' in dictionary
        assert dictionary['type'] == subscriptionType.toStr()

        assert 'version' in dictionary
        assert dictionary['version'] == subscriptionType.getVersion()

    def test_toJson3(self):
        condition = TwitchWebsocketCondition(
            broadcasterUserId = 'foo',
            moderatorUserId = 'bar'
        )

        subscriptionType = TwitchWebsocketSubscriptionType.SUBSCRIBE

        transport = TwitchWebsocketTransport(
            method = TwitchWebsocketTransportMethod.WEBSOCKET,
            sessionId = 'azerty'
        )

        request = TwitchEventSubRequest(
            condition = condition,
            subscriptionType = subscriptionType,
            transport = transport
        )

        dictionary = request.toJson()

        assert isinstance(dictionary, dict)

        assert 'condition' in dictionary
        assert 'broadcaster_user_id' in dictionary['condition']
        assert condition.broadcasterUserId == dictionary['condition']['broadcaster_user_id']
        assert 'client_id' not in dictionary['condition']
        assert 'from_broadcaster_user_id' not in dictionary['condition']
        assert 'moderator_user_id' in dictionary['condition']
        assert condition.moderatorUserId == dictionary['condition']['moderator_user_id']
        assert 'reward_id' not in dictionary['condition']
        assert 'to_broadcaster_user_id' not in dictionary['condition']
        assert 'user_id' not in dictionary['condition']

        assert 'transport' in dictionary
        assert 'method' in dictionary['transport']
        assert dictionary['transport']['method'] == transport.method.toStr()
        assert 'session_id' in dictionary['transport']
        assert dictionary['transport']['session_id'] == transport.sessionId

        assert 'type' in dictionary
        assert dictionary['type'] == subscriptionType.toStr()

        assert 'version' in dictionary
        assert dictionary['version'] == subscriptionType.getVersion()
