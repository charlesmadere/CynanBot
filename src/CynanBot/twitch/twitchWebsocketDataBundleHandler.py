from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.absTwitchChannelPointRedemptionHandler import \
    AbsTwitchChannelPointRedemptionHandler
from CynanBot.twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from CynanBot.twitch.absTwitchPredictionHandler import \
    AbsTwitchPredictionHandler
from CynanBot.twitch.absTwitchRaidHandler import AbsTwitchRaidHandler
from CynanBot.twitch.absTwitchSubscriptionHandler import \
    AbsTwitchSubscriptionHandler
from CynanBot.twitch.websocket.twitchWebsocketDataBundleListener import \
    TwitchWebsocketDataBundleListener
from CynanBot.twitch.websocket.websocketDataBundle import WebsocketDataBundle
from CynanBot.twitch.websocket.websocketEvent import WebsocketEvent
from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class TwitchWebsocketDataBundleHandler(TwitchWebsocketDataBundleListener):

    def __init__(
        self,
        channelPointRedemptionHandler: Optional[AbsTwitchChannelPointRedemptionHandler],
        cheerHandler: Optional[AbsTwitchCheerHandler],
        predictionHandler: Optional[AbsTwitchPredictionHandler],
        raidHandler: Optional[AbsTwitchRaidHandler],
        subscriptionHandler: Optional[AbsTwitchSubscriptionHandler],
        timber: TimberInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if channelPointRedemptionHandler is not None and not isinstance(channelPointRedemptionHandler, AbsTwitchChannelPointRedemptionHandler):
            raise ValueError(f'channelPointRedemptionHandler argument is malformed: \"{channelPointRedemptionHandler}\"')
        elif cheerHandler is not None and not isinstance(cheerHandler, AbsTwitchCheerHandler):
            raise ValueError(f'cheerHandler argument is malformed: \"{cheerHandler}\"')
        elif predictionHandler is not None and not isinstance(predictionHandler, AbsTwitchPredictionHandler):
            raise ValueError(f'predictionHandler argument is malformed: \"{predictionHandler}\"')
        elif raidHandler is not None and not isinstance(raidHandler, AbsTwitchRaidHandler):
            raise ValueError(f'raidHandler argument is malformed: \"{raidHandler}\"')
        elif subscriptionHandler is not None and not isinstance(subscriptionHandler, AbsTwitchSubscriptionHandler):
            raise ValueError(f'subscriptionHandler argument is malformed: \"{subscriptionHandler}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__channelPointRedemptionHandler: Optional[AbsTwitchChannelPointRedemptionHandler] = channelPointRedemptionHandler
        self.__cheerHandler: Optional[AbsTwitchCheerHandler] = cheerHandler
        self.__predictionHandler: Optional[AbsTwitchPredictionHandler] = predictionHandler
        self.__raidHandler: Optional[AbsTwitchRaidHandler] = raidHandler
        self.__subscriptionHandler: Optional[AbsTwitchSubscriptionHandler] = subscriptionHandler
        self.__timber: TimberInterface = timber
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __isChannelPointsRedemptionType(
        self,
        subscriptionType: Optional[WebsocketSubscriptionType]
    ) -> bool:
        return subscriptionType is WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION

    async def __isCheerType(
        self,
        subscriptionType: Optional[WebsocketSubscriptionType]
    ) -> bool:
        return subscriptionType is WebsocketSubscriptionType.CHEER

    async def __isPredictionType(
        self,
        subscriptionType: Optional[WebsocketSubscriptionType]
    ) -> bool:
        return subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN \
            or subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_END \
            or subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK \
            or subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS

    async def __isRaidType(
        self,
        subscriptionType: Optional[WebsocketSubscriptionType]
    ) -> bool:
        return subscriptionType is WebsocketSubscriptionType.RAID

    async def __isSubscriptionType(
        self,
        subscriptionType: Optional[WebsocketSubscriptionType]
    ) -> bool:
        return subscriptionType is WebsocketSubscriptionType.SUBSCRIBE \
            or subscriptionType is WebsocketSubscriptionType.SUBSCRIPTION_GIFT \
            or subscriptionType is WebsocketSubscriptionType.SUBSCRIPTION_MESSAGE

    async def onNewWebsocketDataBundle(self, dataBundle: WebsocketDataBundle):
        if not isinstance(dataBundle, WebsocketDataBundle):
            raise ValueError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        payload = dataBundle.getPayload()
        if payload is None:
            return

        event = payload.getEvent()
        if event is None:
            return

        userId = event.getBroadcasterUserId()

        if not utils.isValidStr(userId):
            userId = event.getToBroadcasterUserId()

            if not utils.isValidStr(userId):
                self.__timber.log('TwitchWebsocketDataBundleHandler', f'Unable to find broadcaster user ID (\"{userId}\") for data bundle: \"{dataBundle}\"')
                return

        userLogin = event.getBroadcasterUserLogin()

        if not utils.isValidStr(userLogin):
            userLogin = event.getToBroadcasterUserLogin()

            if not utils.isValidStr(userLogin):
                self.__timber.log('TwitchWebsocketDataBundleHandler', f'Unable to find broadcaster user login (\"{userLogin}\") for data bundle: \"{dataBundle}\"')
                return

        await self.__persistUserInfo(event)
        user = await self.__usersRepository.getUserAsync(userLogin)
        subscriptionType = dataBundle.getMetadata().getSubscriptionType()

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

    async def __persistUserInfo(self, event: Optional[WebsocketEvent]):
        if event is None:
            return
        elif not isinstance(event, WebsocketEvent):
            raise ValueError(f'event argument is malformed: \"{event}\"')

        await self.__userIdsRepository.optionallySetUser(
            userId = event.getBroadcasterUserId(),
            userName = event.getBroadcasterUserLogin()
        )

        await self.__userIdsRepository.optionallySetUser(
            userId = event.getFromBroadcasterUserId(),
            userName = event.getFromBroadcasterUserLogin()
        )

        await self.__userIdsRepository.optionallySetUser(
            userId = event.getToBroadcasterUserId(),
            userName = event.getToBroadcasterUserLogin()
        )

        await self.__userIdsRepository.optionallySetUser(
            userId = event.getUserId(),
            userName = event.getUserLogin()
        )

        subGift = event.getSubGift()
        if subGift is not None:
            await self.__userIdsRepository.setUser(
                userId = subGift.getRecipientUserId(),
                userName = subGift.getRecipientUserLogin()
            )

        outcomes = event.getOutcomes()
        if outcomes is not None and len(outcomes) >= 1:
            for outcome in outcomes:
                topPredictors = outcome.getTopPredictors()

                if topPredictors is not None and len(topPredictors) >= 1:
                    for topPredictor in topPredictors:
                        await self.__userIdsRepository.setUser(
                            userId = topPredictor.getUserId(),
                            userName = topPredictor.getUserLogin()
                        )
