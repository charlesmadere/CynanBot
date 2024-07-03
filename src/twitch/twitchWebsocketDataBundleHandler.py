from .absTwitchChannelPointRedemptionHandler import \
    AbsTwitchChannelPointRedemptionHandler
from .absTwitchCheerHandler import AbsTwitchCheerHandler
from .absTwitchFollowHandler import AbsTwitchFollowHandler
from .absTwitchPollHandler import AbsTwitchPollHandler
from .absTwitchPredictionHandler import AbsTwitchPredictionHandler
from .absTwitchRaidHandler import AbsTwitchRaidHandler
from .absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler
from .api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from .api.websocket.twitchWebsocketEvent import TwitchWebsocketEvent
from .api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
from .websocket.twitchWebsocketDataBundleListener import \
    TwitchWebsocketDataBundleListener
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class TwitchWebsocketDataBundleHandler(TwitchWebsocketDataBundleListener):

    def __init__(
        self,
        channelPointRedemptionHandler: AbsTwitchChannelPointRedemptionHandler | None,
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

        self.__channelPointRedemptionHandler: AbsTwitchChannelPointRedemptionHandler | None = channelPointRedemptionHandler
        self.__cheerHandler: AbsTwitchCheerHandler | None = cheerHandler
        self.__followHandler: AbsTwitchFollowHandler | None = followHandler
        self.__pollHandler: AbsTwitchPollHandler | None = pollHandler
        self.__predictionHandler: AbsTwitchPredictionHandler | None = predictionHandler
        self.__raidHandler: AbsTwitchRaidHandler | None = raidHandler
        self.__subscriptionHandler: AbsTwitchSubscriptionHandler | None = subscriptionHandler
        self.__timber: TimberInterface = timber
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __isChannelPointsRedemptionType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType | None
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION

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

        if utils.isValidStr(event.broadcasterUserId):
            userId = event.broadcasterUserId
        elif utils.isValidStr(event.toBroadcasterUserId):
            userId = event.toBroadcasterUserId
        else:
            self.__timber.log('TwitchWebsocketDataBundleHandler', f'Unable to find broadcaster user ID for data bundle ({userId=}) ({event.broadcasterUserId=}) ({event.toBroadcasterUserId=}): \"{dataBundle}\"')
            return

        userLogin: str | None = None

        if utils.isValidStr(event.broadcasterUserLogin):
            userLogin = event.broadcasterUserLogin
        elif utils.isValidStr(event.toBroadcasterUserLogin):
            userLogin = event.toBroadcasterUserLogin
        else:
            self.__timber.log('TwitchWebsocketDataBundleHandler', f'Unable to find broadcaster user login for data bundle ({userLogin=}) ({event.broadcasterUserLogin=}) ({event.toBroadcasterUserLogin=}): \"{dataBundle}\"')
            return

        await self.__persistUserInfo(event)
        user = await self.__usersRepository.getUserAsync(userLogin)
        subscriptionType = dataBundle.metadata.subscriptionType

        if await self.__isChannelPointsRedemptionType(subscriptionType):
            channelPointRedemptionHandler = self.__channelPointRedemptionHandler

            if channelPointRedemptionHandler is not None:
                await channelPointRedemptionHandler.onNewChannelPointRedemption(
                    userId = userId,
                    user = user,
                    dataBundle = dataBundle
                )
        elif await self.__isCheerType(subscriptionType):
            cheerHandler = self.__cheerHandler

            if cheerHandler is not None:
                await cheerHandler.onNewCheer(
                    userId = userId,
                    user = user,
                    dataBundle = dataBundle
                )
        elif await self.__isFollowType(subscriptionType):
            followHandler = self.__followHandler

            if followHandler is not None:
                await followHandler.onNewFollow(
                    userId = userId,
                    user = user,
                    dataBundle = dataBundle
                )
        elif await self.__isPollType(subscriptionType):
            pollHandler = self.__pollHandler

            if pollHandler is not None:
                await pollHandler.onNewPoll(
                    userId = userId,
                    user = user,
                    dataBundle = dataBundle
                )
        elif await self.__isPredictionType(subscriptionType):
            predictionHandler = self.__predictionHandler

            if predictionHandler is not None:
                await predictionHandler.onNewPrediction(
                    userId = userId,
                    user = user,
                    dataBundle = dataBundle
                )
        elif await self.__isRaidType(subscriptionType):
            raidHandler = self.__raidHandler

            if raidHandler is not None:
                await raidHandler.onNewRaid(
                    userId = userId,
                    user = user,
                    dataBundle = dataBundle
                )
        elif await self.__isSubscriptionType(subscriptionType):
            subscriptionHandler = self.__subscriptionHandler

            if subscriptionHandler is not None:
                await subscriptionHandler.onNewSubscription(
                    userId = userId,
                    user = user,
                    dataBundle = dataBundle
                )
        else:
            self.__timber.log('TwitchWebsocketDataBundleHandler', f'Received unhandled data bundle: \"{dataBundle}\"')

    async def __persistUserInfo(self, event: TwitchWebsocketEvent | None):
        if event is None:
            return
        elif not isinstance(event, TwitchWebsocketEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        await self.__userIdsRepository.optionallySetUser(
            userId = event.broadcasterUserId,
            userName = event.broadcasterUserLogin
        )

        await self.__userIdsRepository.optionallySetUser(
            userId = event.fromBroadcasterUserId,
            userName = event.fromBroadcasterUserLogin
        )

        await self.__userIdsRepository.optionallySetUser(
            userId = event.toBroadcasterUserId,
            userName = event.toBroadcasterUserLogin
        )

        await self.__userIdsRepository.optionallySetUser(
            userId = event.userId,
            userName = event.userLogin
        )

        if event.subGift is not None:
            await self.__userIdsRepository.setUser(
                userId = event.subGift.recipientUserId,
                userName = event.subGift.recipientUserLogin
            )

        if event.outcomes is not None and len(event.outcomes) >= 1:
            for outcome in event.outcomes:
                topPredictors = outcome.topPredictors

                if topPredictors is not None and len(topPredictors) >= 1:
                    for topPredictor in topPredictors:
                        await self.__userIdsRepository.setUser(
                            userId = topPredictor.userId,
                            userName = topPredictor.userLogin
                        )
