from typing import Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.twitch.websocket.twitchWebsocketDataBundleListener import \
    TwitchWebsocketDataBundleListener
from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from CynanBotCommon.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBotCommon.users.userInterface import UserInterface
from CynanBotCommon.users.usersRepositoryInterface import \
    UsersRepositoryInterface
from twitch.absTwitchChannelPointRedemptionHandler import \
    AbsTwitchChannelPointRedemptionHandler
from twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from twitch.absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler


class TwitchWebsocketDataBundleHandler(TwitchWebsocketDataBundleListener):

    def __init__(
        self,
        timber: TimberInterface,
        channelPointRedemptionHandler: Optional[AbsTwitchChannelPointRedemptionHandler],
        cheerHandler: Optional[AbsTwitchCheerHandler],
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
        elif subscriptionHandler is not None and not isinstance(subscriptionHandler, AbsTwitchSubscriptionHandler):
            raise ValueError(f'subscriptionHandler argument is malformed: \"{subscriptionHandler}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__timber: TimberInterface = timber
        self.__channelPointRedemptionHandler: Optional[AbsTwitchChannelPointRedemptionHandler] = channelPointRedemptionHandler
        self.__cheerHandler: Optional[AbsTwitchCheerHandler] = cheerHandler
        self.__subscriptionHandler: Optional[AbsTwitchSubscriptionHandler] = subscriptionHandler
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __isChannelPointsRedemptionType(self, subscriptionType: WebsocketSubscriptionType) -> bool:
        return subscriptionType is WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION

    async def __isCheerType(self, subscriptionType: WebsocketSubscriptionType) -> bool:
        return subscriptionType is WebsocketSubscriptionType.CHEER

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

        user: Optional[UserInterface] = None

        try:
            user = await self.__usersRepository.getUserAsync(userLogin)
        except:
            pass

        if user is None:
            self.__timber.log('TwitchWebsocketDataBundleHandler', f'Unable to retrieve broadcast user in users repository (userId=\"{userId}\") (userLogin=\"{userLogin}\")')
            return

        await self.__userIdsRepository.setUser(
            userId = userId,
            userName = userLogin
        )

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
