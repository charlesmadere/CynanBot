import traceback
from typing import Final

from .absTwitchBitsHandler import AbsTwitchBitsHandler
from .absTwitchChannelPointRedemptionHandler import AbsTwitchChannelPointRedemptionHandler
from .absTwitchChatHandler import AbsTwitchChatHandler
from .absTwitchFollowHandler import AbsTwitchFollowHandler
from .absTwitchHypeTrainHandler import AbsTwitchHypeTrainHandler
from .absTwitchPollHandler import AbsTwitchPollHandler
from .absTwitchPowerUpRedemptionHandler import AbsTwitchPowerUpRedemptionHandler
from .absTwitchPredictionHandler import AbsTwitchPredictionHandler
from .absTwitchRaidHandler import AbsTwitchRaidHandler
from .absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler
from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .api.models.twitchWebsocketEvent import TwitchWebsocketEvent
from .api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from .websocket.listener.twitchWebsocketDataBundleListener import TwitchWebsocketDataBundleListener
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..users.exceptions import NoSuchUserException
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class TwitchWebsocketDataBundleHandler(TwitchWebsocketDataBundleListener):

    def __init__(
        self,
        bitsHandler: AbsTwitchBitsHandler | None,
        channelPointRedemptionHandler: AbsTwitchChannelPointRedemptionHandler | None,
        chatHandler: AbsTwitchChatHandler | None,
        followHandler: AbsTwitchFollowHandler | None,
        hypeTrainHandler: AbsTwitchHypeTrainHandler | None,
        pollHandler: AbsTwitchPollHandler | None,
        powerUpRedemptionHandler: AbsTwitchPowerUpRedemptionHandler | None,
        predictionHandler: AbsTwitchPredictionHandler | None,
        raidHandler: AbsTwitchRaidHandler | None,
        subscriptionHandler: AbsTwitchSubscriptionHandler | None,
        timber: TimberInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if bitsHandler is not None and not isinstance(bitsHandler, AbsTwitchBitsHandler):
            raise TypeError(f'bitsHandler argument is malformed: \"{bitsHandler}\"')
        elif channelPointRedemptionHandler is not None and not isinstance(channelPointRedemptionHandler, AbsTwitchChannelPointRedemptionHandler):
            raise TypeError(f'channelPointRedemptionHandler argument is malformed: \"{channelPointRedemptionHandler}\"')
        elif chatHandler is not None and not isinstance(chatHandler, AbsTwitchChatHandler):
            raise TypeError(f'chatHandler argument is malformed: \"{chatHandler}\"')
        elif followHandler is not None and not isinstance(followHandler, AbsTwitchFollowHandler):
            raise TypeError(f'followHandler argument is malformed: \"{followHandler}\"')
        elif hypeTrainHandler is not None and not isinstance(hypeTrainHandler, AbsTwitchHypeTrainHandler):
            raise TypeError(f'hypeTrainHandler argument is malformed: \"{hypeTrainHandler}\"')
        elif pollHandler is not None and not isinstance(pollHandler, AbsTwitchPollHandler):
            raise TypeError(f'pollHandler argument is malformed: \"{pollHandler}\"')
        elif powerUpRedemptionHandler is not None and not isinstance(powerUpRedemptionHandler, AbsTwitchPowerUpRedemptionHandler):
            raise TypeError(f'powerUpRedemptionHandler argument is malformed: \"{powerUpRedemptionHandler}\"')
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

        self.__bitsHandler: Final[AbsTwitchBitsHandler | None] = bitsHandler
        self.__channelPointRedemptionHandler: Final[AbsTwitchChannelPointRedemptionHandler | None] = channelPointRedemptionHandler
        self.__chatHandler: Final[AbsTwitchChatHandler | None] = chatHandler
        self.__followHandler: Final[AbsTwitchFollowHandler | None] = followHandler
        self.__hypeTrainHandler: Final[AbsTwitchHypeTrainHandler | None] = hypeTrainHandler
        self.__pollHandler: Final[AbsTwitchPollHandler | None] = pollHandler
        self.__powerUpRedemptionHandler: Final[AbsTwitchPowerUpRedemptionHandler | None] = powerUpRedemptionHandler
        self.__predictionHandler: Final[AbsTwitchPredictionHandler | None] = predictionHandler
        self.__raidHandler: Final[AbsTwitchRaidHandler | None] = raidHandler
        self.__subscriptionHandler: Final[AbsTwitchSubscriptionHandler | None] = subscriptionHandler
        self.__timber: Final[TimberInterface] = timber
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def __isBitsType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None,
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_BITS_USE

    async def __isChannelPointsRedemptionType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None,
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION

    async def __isChatType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None,
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_CHAT_NOTIFICATION

    async def __isFollowType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None,
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_FOLLOW

    async def __isHypeTrainType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None,
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_HYPE_TRAIN_BEGIN \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_HYPE_TRAIN_END \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_HYPE_TRAIN_PROGRESS

    async def __isPollType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None,
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_END \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS

    async def __isPowerUpRedemptionType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None,
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_CUSTOM_POWER_UP_REDEMPTION

    async def __isPredictionType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None,
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS

    async def __isRaidType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None,
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.RAID

    async def __isSubscriptionType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None,
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

        twitchChannelId: str | None = None
        twitchChannelLogin: str | None = None

        if utils.isValidStr(event.broadcasterUserId):
            twitchChannelId = event.broadcasterUserId
        elif utils.isValidStr(event.toBroadcasterUserId):
            twitchChannelId = event.toBroadcasterUserId

        if utils.isValidStr(event.broadcasterUserLogin):
            twitchChannelLogin = event.broadcasterUserLogin
        elif utils.isValidStr(event.toBroadcasterUserLogin):
            twitchChannelLogin = event.toBroadcasterUserLogin

        if not utils.isValidStr(twitchChannelId) or not utils.isValidStr(twitchChannelLogin):
            self.__timber.log('TwitchWebsocketDataBundleHandler', f'Unable to find broadcaster user information in data bundle ({twitchChannelId=}) ({twitchChannelLogin=}) ({dataBundle=})')
            return

        await self.__persistUserInfo(
            event = event,
        )

        try:
            twitchUser = await self.__usersRepository.getUserAsync(
                handle = twitchChannelLogin,
            )
        except NoSuchUserException as e:
            self.__timber.log('TwitchWebsocketDataBundleHandler', f'Unable to find user ({twitchChannelId=}) ({twitchChannelLogin=}) ({dataBundle=})', e, traceback.format_exc())
            return

        subscriptionType = dataBundle.metadata.subscriptionType

        if await self.__isBitsType(subscriptionType):
            if self.__bitsHandler is not None:
                await self.__bitsHandler.onNewBitsDataBundle(
                    twitchChannelId = twitchChannelId,
                    user = twitchUser,
                    dataBundle = dataBundle,
                )

        elif await self.__isChannelPointsRedemptionType(subscriptionType):
            if self.__channelPointRedemptionHandler is not None:
                await self.__channelPointRedemptionHandler.onNewChannelPointRedemptionDataBundle(
                    twitchChannelId = twitchChannelId,
                    user = twitchUser,
                    dataBundle = dataBundle,
                )

        elif await self.__isChatType(subscriptionType):
            if self.__chatHandler is not None:
                await self.__chatHandler.onNewChatDataBundle(
                    twitchChannelId = twitchChannelId,
                    user = twitchUser,
                    dataBundle = dataBundle,
                )

        elif await self.__isFollowType(subscriptionType):
            if self.__followHandler is not None:
                await self.__followHandler.onNewFollowDataBundle(
                    twitchChannelId = twitchChannelId,
                    user = twitchUser,
                    dataBundle = dataBundle,
                )

        elif await self.__isHypeTrainType(subscriptionType):
            if self.__hypeTrainHandler is not None:
                await self.__hypeTrainHandler.onNewHypeTrainDataBundle(
                    twitchChannelId = twitchChannelId,
                    user = twitchUser,
                    dataBundle = dataBundle,
                )

        elif await self.__isPollType(subscriptionType):
            if self.__pollHandler is not None:
                await self.__pollHandler.onNewPollDataBundle(
                    twitchChannelId = twitchChannelId,
                    user = twitchUser,
                    dataBundle = dataBundle,
                )

        elif await self.__isPowerUpRedemptionType(subscriptionType):
            if self.__powerUpRedemptionHandler is not None:
                await self.__powerUpRedemptionHandler.onNewPowerUpRedemptionDataBundle(
                    twitchChannelId = twitchChannelId,
                    user = twitchUser,
                    dataBundle = dataBundle,
                )

        elif await self.__isPredictionType(subscriptionType):
            if self.__predictionHandler is not None:
                await self.__predictionHandler.onNewPredictionDataBundle(
                    twitchChannelId = twitchChannelId,
                    user = twitchUser,
                    dataBundle = dataBundle,
                )

        elif await self.__isRaidType(subscriptionType):
            if self.__raidHandler is not None:
                await self.__raidHandler.onNewRaidDataBundle(
                    twitchChannelId = twitchChannelId,
                    user = twitchUser,
                    dataBundle = dataBundle,
                )

        elif await self.__isSubscriptionType(subscriptionType):
            if self.__subscriptionHandler is not None:
                await self.__subscriptionHandler.onNewSubscriptionDataBundle(
                    twitchChannelId = twitchChannelId,
                    user = twitchUser,
                    dataBundle = dataBundle,
                )

        else:
            self.__timber.log('TwitchWebsocketDataBundleHandler', f'Received unhandled data bundle ({twitchChannelId=}) ({twitchUser=}) ({subscriptionType=}) ({dataBundle=})')

    async def __persistUserInfo(self, event: TwitchWebsocketEvent):
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

        if event.chatMessage is not None:
            for fragment in event.chatMessage.fragments:
                if fragment.mention is not None:
                    await self.__addToUserIdsToUserNames(userIdsToUserNames, fragment.mention.userId, fragment.mention.userLogin)

        if event.reply is not None:
            await self.__addToUserIdsToUserNames(userIdsToUserNames, event.reply.parentUserId, event.reply.parentUserLogin)
            await self.__addToUserIdsToUserNames(userIdsToUserNames, event.reply.threadUserId, event.reply.threadUserLogin)

        if len(userIdsToUserNames) >= 1:
            await self.__userIdsRepository.setUsers(userIdsToUserNames)

    async def __addToUserIdsToUserNames(
        self,
        userIdsToUserNames: dict[str, str],
        userId: str | None,
        userLogin: str | None,
    ):
        if not utils.isValidStr(userId) or not utils.isValidStr(userLogin):
            return

        userIdsToUserNames[userId] = userLogin
