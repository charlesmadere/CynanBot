from typing import Final

from .absTwitchChannelPointRedemptionHandler import AbsTwitchChannelPointRedemptionHandler
from .absTwitchChatHandler import AbsTwitchChatHandler
from .absTwitchCheerHandler import AbsTwitchCheerHandler
from .absTwitchFollowHandler import AbsTwitchFollowHandler
from .absTwitchPollHandler import AbsTwitchPollHandler
from .absTwitchPredictionHandler import AbsTwitchPredictionHandler
from .absTwitchRaidHandler import AbsTwitchRaidHandler
from .absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler
from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .api.models.twitchWebsocketEvent import TwitchWebsocketEvent
from .api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from .websocket.listener.twitchWebsocketDataBundleListener import TwitchWebsocketDataBundleListener
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class TwitchWebsocketDataBundleHandler(TwitchWebsocketDataBundleListener):

    def __init__(
        self,
        channelPointRedemptionHandler: AbsTwitchChannelPointRedemptionHandler | None,
        chatHandler: AbsTwitchChatHandler | None,
        cheerHandler: AbsTwitchCheerHandler | None,
        followHandler: AbsTwitchFollowHandler | None,
        pollHandler: AbsTwitchPollHandler | None,
        predictionHandler: AbsTwitchPredictionHandler | None,
        raidHandler: AbsTwitchRaidHandler | None,
        subscriptionHandler: AbsTwitchSubscriptionHandler | None,
        timber: TimberInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if channelPointRedemptionHandler is not None and not isinstance(channelPointRedemptionHandler, AbsTwitchChannelPointRedemptionHandler):
            raise TypeError(f'channelPointRedemptionHandler argument is malformed: \"{channelPointRedemptionHandler}\"')
        elif chatHandler is not None and not isinstance(chatHandler, AbsTwitchChatHandler):
            raise TypeError(f'chatHandler argument is malformed: \"{chatHandler}\"')
        elif cheerHandler is not None and not isinstance(cheerHandler, AbsTwitchCheerHandler):
            raise TypeError(f'cheerHandler argument is malformed: \"{cheerHandler}\"')
        elif followHandler is not None and not isinstance(followHandler, AbsTwitchFollowHandler):
            raise TypeError(f'followHandler argument is malformed: \"{followHandler}\"')
        elif pollHandler is not None and not isinstance(pollHandler, AbsTwitchPollHandler):
            raise TypeError(f'pollHandler argument is malformed: \"{pollHandler}\"')
        elif predictionHandler is not None and not isinstance(predictionHandler, AbsTwitchPredictionHandler):
            raise TypeError(f'predictionHandler argument is malformed: \"{predictionHandler}\"')
        elif raidHandler is not None and not isinstance(raidHandler, AbsTwitchRaidHandler):
            raise TypeError(f'raidHandler argument is malformed: \"{raidHandler}\"')
        elif subscriptionHandler is not None and not isinstance(subscriptionHandler, AbsTwitchSubscriptionHandler):
            raise TypeError(f'subscriptionHandler argument is malformed: \"{subscriptionHandler}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__channelPointRedemptionHandler: Final[AbsTwitchChannelPointRedemptionHandler | None] = channelPointRedemptionHandler
        self.__chatHandler: Final[AbsTwitchChatHandler | None] = chatHandler
        self.__cheerHandler: Final[AbsTwitchCheerHandler | None] = cheerHandler
        self.__followHandler: Final[AbsTwitchFollowHandler | None] = followHandler
        self.__pollHandler: Final[AbsTwitchPollHandler | None] = pollHandler
        self.__predictionHandler: Final[AbsTwitchPredictionHandler | None] = predictionHandler
        self.__raidHandler: Final[AbsTwitchRaidHandler | None] = raidHandler
        self.__subscriptionHandler: Final[AbsTwitchSubscriptionHandler | None] = subscriptionHandler
        self.__timber: Final[TimberInterface] = timber
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def __isChannelPointsRedemptionType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION

    async def __isChatType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE

    async def __isCheerType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHEER

    async def __isFollowType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.FOLLOW

    async def __isPollType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_END \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS

    async def __isPredictionType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS

    async def __isRaidType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.RAID

    async def __isSubscriptionType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIBE \
            or subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT \
            or subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE

    async def onNewWebsocketDataBundle(self, dataBundle: TwitchWebsocketDataBundle):
        if not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        if dataBundle.payload is None:
            return

        event = dataBundle.payload.event

        if event is None:
            return

        userId: str | None = None
        userLogin: str | None = None

        if utils.isValidStr(event.broadcasterUserId):
            userId = event.broadcasterUserId
        elif utils.isValidStr(event.toBroadcasterUserId):
            userId = event.toBroadcasterUserId

        if utils.isValidStr(event.broadcasterUserLogin):
            userLogin = event.broadcasterUserLogin
        elif utils.isValidStr(event.toBroadcasterUserLogin):
            userLogin = event.toBroadcasterUserLogin

        if not utils.isValidStr(userId) or not utils.isValidStr(userLogin):
            self.__timber.log('TwitchWebsocketDataBundleHandler', f'Unable to find broadcaster user information in data bundle ({userId=}) ({userLogin=}) ({dataBundle=})')
            return

        await self.__persistUserInfo(event)
        user = await self.__usersRepository.getUserAsync(userLogin)
        subscriptionType = dataBundle.metadata.subscriptionType

        if await self.__isChannelPointsRedemptionType(subscriptionType):
            if self.__channelPointRedemptionHandler is not None:
                await self.__channelPointRedemptionHandler.onNewChannelPointRedemption(
                    userId = userId,
                    user = user,
                    dataBundle = dataBundle,
                )

        elif await self.__isChatType(subscriptionType):
            if self.__chatHandler is not None:
                await self.__chatHandler.onNewChatDataBundle(
                    broadcasterUserId = userId,
                    user = user,
                    dataBundle = dataBundle,
                )

        elif await self.__isCheerType(subscriptionType):
            if self.__cheerHandler is not None:
                await self.__cheerHandler.onNewCheerDataBundle(
                    broadcasterUserId = userId,
                    user = user,
                    dataBundle = dataBundle,
                )

        elif await self.__isFollowType(subscriptionType):
            if self.__followHandler is not None:
                await self.__followHandler.onNewFollowDataBundle(
                    userId = userId,
                    user = user,
                    dataBundle = dataBundle,
                )

        elif await self.__isPollType(subscriptionType):
            if self.__pollHandler is not None:
                await self.__pollHandler.onNewPollDataBundle(
                    userId = userId,
                    user = user,
                    dataBundle = dataBundle,
                )

        elif await self.__isPredictionType(subscriptionType):
            if self.__predictionHandler is not None:
                await self.__predictionHandler.onNewPrediction(
                    userId = userId,
                    user = user,
                    dataBundle = dataBundle,
                )

        elif await self.__isRaidType(subscriptionType):
            if self.__raidHandler is not None:
                await self.__raidHandler.onNewRaid(
                    userId = userId,
                    user = user,
                    dataBundle = dataBundle,
                )

        elif await self.__isSubscriptionType(subscriptionType):
            if self.__subscriptionHandler is not None:
                await self.__subscriptionHandler.onNewSubscriptionDataBundle(
                    broadcasterUserId = userId,
                    user = user,
                    dataBundle = dataBundle,
                )

        else:
            self.__timber.log('TwitchWebsocketDataBundleHandler', f'Received unhandled data bundle ({userId=}) ({user=}) ({dataBundle=})')

    async def __persistUserInfo(self, event: TwitchWebsocketEvent | None):
        if event is None:
            return
        elif not isinstance(event, TwitchWebsocketEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        userIdsToUserNames: dict[str, str] = dict()
        await self.__addToUserIdsToUserNames(userIdsToUserNames, event.broadcasterUserId, event.broadcasterUserLogin)
        await self.__addToUserIdsToUserNames(userIdsToUserNames, event.fromBroadcasterUserId, event.fromBroadcasterUserLogin)
        await self.__addToUserIdsToUserNames(userIdsToUserNames, event.toBroadcasterUserId, event.toBroadcasterUserLogin)
        await self.__addToUserIdsToUserNames(userIdsToUserNames, event.userId, event.userLogin)

        if event.subGift is not None:
            await self.__addToUserIdsToUserNames(userIdsToUserNames, event.subGift.recipientUserId, event.subGift.recipientUserLogin)

        if event.outcomes is not None and len(event.outcomes) >= 1:
            for outcome in event.outcomes:
                topPredictors = outcome.topPredictors

                if topPredictors is not None and len(topPredictors) >= 1:
                    for topPredictor in topPredictors:
                        await self.__addToUserIdsToUserNames(userIdsToUserNames, topPredictor.userId, topPredictor.userLogin)

        if event.chatMessage is not None and event.chatMessage.fragments is not None:
            for fragment in event.chatMessage.fragments:
                if fragment.mention is not None:
                    await self.__addToUserIdsToUserNames(userIdsToUserNames, fragment.mention.userId, fragment.mention.userLogin)

        if len(userIdsToUserNames) >= 1:
            await self.__userIdsRepository.setUsers(userIdsToUserNames)

    async def __addToUserIdsToUserNames(
        self,
        userIdsToUserNames: dict[str, str],
        userId: str | None,
        userLogin: str | None
    ):
        if not utils.isValidStr(userId) or not utils.isValidStr(userLogin):
            return

        userIdsToUserNames[userId] = userLogin
