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
from pointRedemptions import AbsPointRedemption, CutenessRedemption
from twitch.twitchChannelPointsMessage import (TwitchChannelPointsMessage,
                                               TwitchChannelPointsMessageStub)
from twitch.twitchChannelProvider import TwitchChannelProvider


class TwitchChannelPointRedemptionHandler():

    def __init__(
        self,
        cutenessRedemption: CutenessRedemption,
        timber: TimberInterface,
        twitchChannelProvider: TwitchChannelProvider,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(cutenessRedemption, CutenessRedemption):
            raise ValueError(f'cutenessRedemption argument is malformed: \"{cutenessRedemption}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise ValueError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__cutenessRedemption: AbsPointRedemption = cutenessRedemption
        self.__timber: TimberInterface = timber
        self.__twitchChannelProvider: TwitchChannelProvider = twitchChannelProvider
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def onNewChannelPointRedemption(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: WebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, WebsocketDataBundle):
            raise ValueError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.getPayload().getEvent()

        if event is None:
            self.__timber.log('TwitchChannelPointRedemptionHandler', 'Received a data bundle that has no event')
            return

        eventId = event.getEventId()
        rewardId = event.getRewardId()
        redemptionUserId = event.getUserId()
        redemptionUserInput = event.getUserInput()
        redemptionUserLogin = event.getUserLogin()

        if not utils.isValidStr(eventId):
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that has no eventId: \"{eventId}\"')
            return
        elif not utils.isValidStr(rewardId):
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that has no rewardId: \"{rewardId}\"')
            return
        elif not utils.isValidStr(redemptionUserId):
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that has no userId: \"{redemptionUserId}\"')
            return
        elif not utils.isValidStr(redemptionUserLogin):
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that has no userLogin: \"{redemptionUserLogin}\"')
            return

        await self.__userIdsRepository.setUser(
            userId = redemptionUserId,
            userName = redemptionUserLogin
        )

        twitchChannel = await self.__twitchChannelProvider.getTwitchChannel(user.getHandle())

        twitchChannelPointsMessage: TwitchChannelPointsMessage = TwitchChannelPointsMessageStub(
            eventId = eventId,
            redemptionMessage = redemptionUserInput,
            rewardId = rewardId,
            user = user,
            userId = redemptionUserId,
            userName = redemptionUserLogin
        )

        if user.isCutenessEnabled() and user.hasCutenessBoosterPacks():
            await self.__cutenessRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = twitchChannelPointsMessage
            )
        # TODO
        pass
