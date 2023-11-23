from typing import Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.twitch.websocket.twitchWebsocketDataBundleListener import \
    TwitchWebsocketDataBundleListener
from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.twitch.websocket.websocketEvent import WebsocketEvent
from CynanBotCommon.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from CynanBotCommon.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBotCommon.users.usersRepositoryInterface import \
    UsersRepositoryInterface
from twitch.absTwitchChannelPointRedemptionHandler import \
    AbsTwitchChannelPointRedemptionHandler
from twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from twitch.absTwitchPredictionHandler import AbsTwitchPredictionHandler
from twitch.absTwitchRaidHandler import AbsTwitchRaidHandler
from twitch.absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler


class TwitchWebsocketDataBundleHandler(TwitchWebsocketDataBundleListener):

    def __init__(
        self,
        timber: TimberInterface,
        channelPointRedemptionHandler: Optional[AbsTwitchChannelPointRedemptionHandler],
        cheerHandler: Optional[AbsTwitchCheerHandler],
        predictionHandler: Optional[AbsTwitchPredictionHandler],
        raidHandler: Optional[AbsTwitchRaidHandler],
        subscriptionHandler: Optional[AbsTwitchSubscriptionHandler],
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif channelPointRedemptionHandler is not None and not isinstance(channelPointRedemptionHandler, AbsTwitchChannelPointRedemptionHandler):
            raise ValueError(f'channelPointRedemptionHandler argument is malformed: \"{channelPointRedemptionHandler}\"')
        elif cheerHandler is not None and not isinstance(cheerHandler, AbsTwitchCheerHandler):
            raise ValueError(f'cheerHandler argument is malformed: \"{cheerHandler}\"')
        elif predictionHandler is not None and not isinstance(predictionHandler, AbsTwitchPredictionHandler):
            raise ValueError(f'predictionHandler argument is malformed: \"{predictionHandler}\"')
        elif raidHandler is not None and not isinstance(raidHandler, AbsTwitchRaidHandler):
            raise ValueError(f'raidHandler argument is malformed: \"{raidHandler}\"')
        elif subscriptionHandler is not None and not isinstance(subscriptionHandler, AbsTwitchSubscriptionHandler):
            raise ValueError(f'subscriptionHandler argument is malformed: \"{subscriptionHandler}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__timber: TimberInterface = timber
        self.__channelPointRedemptionHandler: Optional[AbsTwitchChannelPointRedemptionHandler] = channelPointRedemptionHandler
        self.__cheerHandler: Optional[AbsTwitchCheerHandler] = cheerHandler
        self.__predictionHandler: Optional[AbsTwitchPredictionHandler] = predictionHandler
        self.__raidHandler: Optional[AbsTwitchRaidHandler] = raidHandler
        self.__subscriptionHandler: Optional[AbsTwitchSubscriptionHandler] = subscriptionHandler
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __isChannelPointsRedemptionType(self, subscriptionType: WebsocketSubscriptionType) -> bool:
        return subscriptionType is WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION

    async def __isCheerType(self, subscriptionType: WebsocketSubscriptionType) -> bool:
        return subscriptionType is WebsocketSubscriptionType.CHEER

    async def __isPredictionType(self, subscriptionType: WebsocketSubscriptionType) -> bool:
        return subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN \
            or subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_END \
            or subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK \
            or subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS

    async def __isRaidType(self, subscriptionType: WebsocketSubscriptionType) -> bool:
        return subscriptionType is WebsocketSubscriptionType.RAID

    async def __isSubscriptionType(self, subscriptionType: WebsocketSubscriptionType) -> bool:
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

        await self.__userIdsRepository.setUser(
            userId = userId,
            userName = userLogin
        )

        await self.__setOtherUserInfo(event)
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

    async def __setOtherUserInfo(self, event: WebsocketEvent):
        if not isinstance(event, WebsocketEvent):
            raise ValueError(f'event argument is malformed: \"{event}\"')

        if utils.isValidStr(event.getFromBroadcasterUserId()) and utils.isValidStr(event.getFromBroadcasterUserLogin()):
            await self.__userIdsRepository.setUser(
                userId = event.getFromBroadcasterUserId(),
                userName = event.getFromBroadcasterUserLogin()
            )

        if utils.isValidStr(event.getToBroadcasterUserId()) and utils.isValidStr(event.getToBroadcasterUserLogin()):
            await self.__userIdsRepository.setUser(
                userId = event.getToBroadcasterUserId(),
                userName = event.getToBroadcasterUserLogin()
            )

        if utils.isValidStr(event.getUserId()) and utils.isValidStr(event.getUserName()):
            await self.__userIdsRepository.setUser(
                userId = event.getUserId(),
                userName = event.getUserLogin()
            )

        if event.getSubGift() is not None:
            await self.__userIdsRepository.setUser(
                userId = event.getSubGift().getRecipientUserId(),
                userName = event.getSubGift().getRecipientUserLogin()
            )
