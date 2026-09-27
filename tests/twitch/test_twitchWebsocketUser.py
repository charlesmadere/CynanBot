from src.twitch.websocket.twitchWebsocketUser import TwitchWebsocketUser


class TestTwitchWebsocketUser:

    def test_equals_withDifferentUserIds(self):
        userLogin = 'smcharly'
        userName = 'smCharly'

        user1 = TwitchWebsocketUser(
            userId = '123',
            userLogin = userLogin,
            userName = userName,
        )

        user2 = TwitchWebsocketUser(
            userId = '456',
            userLogin = userLogin,
            userName = userName,
        )

        assert user1 != user2

    def test_equals_withSameUserIds(self):
        userId = 'abc123'

        user1 = TwitchWebsocketUser(
            userId = userId,
            userLogin = 'anny',
            userName = 'Anny',
        )

        user2 = TwitchWebsocketUser(
            userId = userId,
            userLogin = 'silvervale',
            userName = 'Silvervale',
        )

        assert user1 == user2

    def test_hash_withDifferentUserIds(self):
        userLogin = 'oatsngoats'
        userName = 'Oatsngoats'

        user1 = TwitchWebsocketUser(
            userId = '123',
            userLogin = userLogin,
            userName = userName,
        )

        user2 = TwitchWebsocketUser(
            userId = '456',
            userLogin = userLogin,
            userName = userName,
        )

        assert hash(user1) != hash(user2)

    def test_hash_withSameUserIds(self):
        userId = 'abc123'

        user1 = TwitchWebsocketUser(
            userId = userId,
            userLogin = 'imyt',
            userName = 'imyt',
        )

        user2 = TwitchWebsocketUser(
            userId = userId,
            userLogin = 'jay_cee',
            userName = 'jay_cee',
        )

        assert hash(user1) == hash(user2)
