import pytest

from src.twitch.api.models.twitchWebsocketCondition import TwitchWebsocketCondition
from src.twitch.api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from src.twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from src.twitch.websocket.conditionBuilder.twitchWebsocketConditionBuilder import TwitchWebsocketConditionBuilder
from src.twitch.websocket.conditionBuilder.twitchWebsocketConditionBuilderInterface import \
    TwitchWebsocketConditionBuilderInterface
from src.twitch.websocket.twitchWebsocketUser import TwitchWebsocketUser
from src.users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...fakeTwitchHandleProvider import FakeTwitchHandleProvider
from ....users.fakeUserIdsRepository import FakeUserIdsRepository


class TestTwitchWebsocketConditionBuilder:

    twitchHandleProvider: TwitchHandleProviderInterface = FakeTwitchHandleProvider()

    userIdsRepository: UserIdsRepositoryInterface = FakeUserIdsRepository()

    conditionBuilder: TwitchWebsocketConditionBuilderInterface = TwitchWebsocketConditionBuilder(
        twitchHandleProvider = twitchHandleProvider,
        userIdsRepository = userIdsRepository,
    )

    @pytest.mark.asyncio
    async def test_build_withChannelChatMessage(self):
        twitchHandle = await self.twitchHandleProvider.getTwitchHandle()
        twitchId = await self.userIdsRepository.requireUserId(twitchHandle)

        websocketUserName = 'stashiocat'
        websocketUser = TwitchWebsocketUser(
            userId = await self.userIdsRepository.requireUserId(websocketUserName),
            userName = websocketUserName,
        )

        result = await self.conditionBuilder.build(
            subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE,
            user = websocketUser,
        )

        assert isinstance(result, TwitchWebsocketCondition)
        assert result.broadcasterUserId == websocketUser.userId
        assert result.userId == websocketUser.userId

    @pytest.mark.asyncio
    async def test_build_withChannelPointsRedemption(self):
        websocketUserName = 'imyt'
        websocketUser = TwitchWebsocketUser(
            userId = await self.userIdsRepository.requireUserId(websocketUserName),
            userName = websocketUserName,
        )

        result = await self.conditionBuilder.build(
            subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION,
            user = websocketUser,
        )

        assert isinstance(result, TwitchWebsocketCondition)
        assert result.broadcasterUserId == websocketUser.userId

    def test_sanity(self):
        assert self.conditionBuilder is not None
        assert isinstance(self.conditionBuilder, TwitchWebsocketConditionBuilder)
        assert isinstance(self.conditionBuilder, TwitchWebsocketConditionBuilderInterface)
