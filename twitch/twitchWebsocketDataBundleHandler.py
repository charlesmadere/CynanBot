from typing import Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from CynanBotCommon.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBotCommon.users.userInterface import UserInterface
from CynanBotCommon.users.usersRepositoryInterface import \
    UsersRepositoryInterface
from twitch.twitchChannelPointRedemptionHandler import \
    TwitchChannelPointRedemptionHandler
from twitch.twitchSubscriptionHandler import TwitchSubscriptionHandler


class TwitchWebsocketDataBundleHandler():

    def __init__(
        self,
        timber: TimberInterface,
        channelPointRedemptionHandler: TwitchChannelPointRedemptionHandler,
        subscriptionHandler: TwitchSubscriptionHandler,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(channelPointRedemptionHandler, TwitchChannelPointRedemptionHandler):
            raise ValueError(f'channelPointRedemptionHandler argument is malformed: \"{channelPointRedemptionHandler}\"')
        elif not isinstance(subscriptionHandler, TwitchSubscriptionHandler):
            raise ValueError(f'subscriptionHandler argument is malformed: \"{subscriptionHandler}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__timber: TimberInterface = timber
        self.__channelPointRedemptionHandler: TwitchChannelPointRedemptionHandler = channelPointRedemptionHandler
        self.__subscriptionHandler: TwitchSubscriptionHandler = subscriptionHandler
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

        event = dataBundle.getPayload().getEvent()

        if event is None:
            return

        userId = event.getBroadcasterUserId()

        if not utils.isValidStr(userId):
            userId = event.getToBroadcasterUserId()

            if not utils.isValidStr(userId):
                self.__timber.log('TwitchWebsocketDataBundleHandler', f'Unable to find user ID for data bundle: \"{dataBundle}\"')
                return

        userLogin = event.getBroadcasterUserLogin()

        if not utils.isValidStr(userLogin):
            userLogin = event.getToBroadcasterUserLogin()

            if not utils.isValidStr(userLogin):
                self.__timber.log('TwitchWebsocketDataBundleHandler', f'Unable to find user login for data bundle: \"{dataBundle}\"')
                return

        user: Optional[UserInterface] = None

        try:
            user = await self.__usersRepository.getUserAsync(userLogin)
        except:
            pass

        if user is None:
            self.__timber.log('TwitchWebsocketDataBundleHandler', f'Unable to retrieve user \"{userLogin}\" in users repository (userId=\"{userId}\")')
            return

        await self.__userIdsRepository.setUser(
            userId = userId,
            userName = userLogin
        )

        subscriptionType = dataBundle.getMetadata().getSubscriptionType()

        if await self.__isChannelPointsRedemptionType(subscriptionType):
            await self.__channelPointRedemptionHandler.onNewChannelPointRedemption(
                userId = userId,
                dataBundle = dataBundle,
                user = user
            )
        elif await self.__isCheerType(subscriptionType):
            pass
        elif await self.__isSubscriptionType(subscriptionType):
            await self.__subscriptionHandler.onNewSubscription(
                dataBundle = dataBundle,
                user = user
            )
        else:
            self.__timber.log('TwitchWebsocketDataBundleHandler', f'Received unhandled data bundle: \"{dataBundle}\"')
