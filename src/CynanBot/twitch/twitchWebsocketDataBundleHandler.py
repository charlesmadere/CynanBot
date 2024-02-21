from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.absTwitchChannelPointRedemptionHandler import \
    AbsTwitchChannelPointRedemptionHandler
from CynanBot.twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from CynanBot.twitch.absTwitchPollHandler import AbsTwitchPollHandler
from CynanBot.twitch.absTwitchPredictionHandler import \
    AbsTwitchPredictionHandler
from CynanBot.twitch.absTwitchRaidHandler import AbsTwitchRaidHandler
from CynanBot.twitch.absTwitchSubscriptionHandler import \
    AbsTwitchSubscriptionHandler
from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.twitch.api.websocket.twitchWebsocketEvent import \
    TwitchWebsocketEvent
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
from CynanBot.twitch.websocket.twitchWebsocketDataBundleListener import \
    TwitchWebsocketDataBundleListener
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class TwitchWebsocketDataBundleHandler(TwitchWebsocketDataBundleListener):

    def __init__(
        self,
        channelPointRedemptionHandler: Optional[AbsTwitchChannelPointRedemptionHandler],
        cheerHandler: Optional[AbsTwitchCheerHandler],
        pollHandler: Optional[AbsTwitchPollHandler],
        predictionHandler: Optional[AbsTwitchPredictionHandler],
        raidHandler: Optional[AbsTwitchRaidHandler],
        subscriptionHandler: Optional[AbsTwitchSubscriptionHandler],
        timber: TimberInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert channelPointRedemptionHandler is None or isinstance(channelPointRedemptionHandler, AbsTwitchChannelPointRedemptionHandler), f"malformed {channelPointRedemptionHandler=}"
        assert cheerHandler is None or isinstance(cheerHandler, AbsTwitchCheerHandler), f"malformed {cheerHandler=}"
        assert pollHandler is None or isinstance(pollHandler, AbsTwitchPollHandler), f"malformed {pollHandler=}"
        assert predictionHandler is None or isinstance(predictionHandler, AbsTwitchPredictionHandler), f"malformed {predictionHandler=}"
        assert raidHandler is None or isinstance(raidHandler, AbsTwitchRaidHandler), f"malformed {raidHandler=}"
        assert subscriptionHandler is None or isinstance(subscriptionHandler, AbsTwitchSubscriptionHandler), f"malformed {subscriptionHandler=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

        self.__channelPointRedemptionHandler: Optional[AbsTwitchChannelPointRedemptionHandler] = channelPointRedemptionHandler
        self.__cheerHandler: Optional[AbsTwitchCheerHandler] = cheerHandler
        self.__pollHandler: Optional[AbsTwitchPollHandler] = pollHandler
        self.__predictionHandler: Optional[AbsTwitchPredictionHandler] = predictionHandler
        self.__raidHandler: Optional[AbsTwitchRaidHandler] = raidHandler
        self.__subscriptionHandler: Optional[AbsTwitchSubscriptionHandler] = subscriptionHandler
        self.__timber: TimberInterface = timber
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __isChannelPointsRedemptionType(
        self,
        subscriptionType: Optional[TwitchWebsocketSubscriptionType]
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION

    async def __isCheerType(
        self,
        subscriptionType: Optional[TwitchWebsocketSubscriptionType]
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHEER

    async def __isPollType(
        self,
        subscriptionType: Optional[TwitchWebsocketSubscriptionType]
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_END \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS

    async def __isPredictionType(
        self,
        subscriptionType: Optional[TwitchWebsocketSubscriptionType]
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK \
            or subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS

    async def __isRaidType(
        self,
        subscriptionType: Optional[TwitchWebsocketSubscriptionType]
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.RAID

    async def __isSubscriptionType(
        self,
        subscriptionType: Optional[TwitchWebsocketSubscriptionType]
    ) -> bool:
        return subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIBE \
            or subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT \
            or subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE

    async def onNewWebsocketDataBundle(self, dataBundle: TwitchWebsocketDataBundle):
        assert isinstance(dataBundle, TwitchWebsocketDataBundle), f"malformed {dataBundle=}"

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

    async def __persistUserInfo(self, event: Optional[TwitchWebsocketEvent]):
        if event is None:
            return
        elassert isinstance(event, TwitchWebsocketEvent), f"malformed {event=}"

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
