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
from twitch.twitchChannelProvider import TwitchChannelProvider


class TwitchChannelPointRedemptionHandler():

    def __init__(
        self,
        timber: TimberInterface,
        twitchChannelProvider: TwitchChannelProvider,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise ValueError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__timber: TimberInterface = timber
        self.__twitchChannelProvider: TwitchChannelProvider = twitchChannelProvider
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def onNewChannelPointRedemption(self, dataBundle: WebsocketDataBundle):
        if not isinstance(dataBundle, WebsocketDataBundle):
            raise ValueError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        subscription = dataBundle.getPayload().getSubscription()

        if subscription is None:
            self.__timber.log('TwitchChannelPointRedemptionHandler', 'Received a data bundle that has no subscription')
            return
        elif subscription.getSubscriptionType() is not WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION:
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that has an invalid subscription type: \"{subscription.getSubscriptionType()}\"')
            return

        condition = subscription.getCondition()
        broadcasterUserId = condition.getBroadcasterUserId()
        redemptionUserId = condition.getUserId()
        redemptionUserName = condition.getUserName()
        rewardId = condition.getRewardId()

        if not utils.isValidStr(broadcasterUserId):
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that has no broadcasterUserId: \"{broadcasterUserId}\"')
            return
        elif not utils.isValidStr(redemptionUserId):
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that has no userId: \"{redemptionUserId}\"')
            return
        elif not utils.isValidStr(redemptionUserName):
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that has no userName: \"{userName}\"')
            return
        elif not utils.isValidStr(rewardId):
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that has no rewardId: \"{rewardId}\"')
            return

        userName = await self.__userIdsRepository.fetchUserName(userId = broadcasterUserId)

        if not utils.isValidStr(userName):
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Couldn\'t find userName for broadcasterUserId: \"{broadcasterUserId}\"')
            return

        user: Optional[UserInterface] = None

        try:
            user = await self.__usersRepository.getUserAsync(userName)
        except:
            pass

        if user is None:
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Couldn\'t find user for userName \"{userName}\" and broadcasterUserId \"{broadcasterUserId}\"')
            return

        await self.__processChannelPointRedemption(
            redemptionUserId = redemptionUserId,
            redemptionUserName = redemptionUserName,
            rewardId = rewardId,
            userInput = condition.getUserInput(),
            user = user
        )

    async def __processChannelPointRedemption(
        self,
        redemptionUserId: str,
        redemptionUserName: str,
        rewardId: str,
        userInput: Optional[str],
        user: UserInterface
    ):
        if not utils.isValidStr(redemptionUserId):
            raise ValueError(f'redemptionUserId argument is malformed: \"{redemptionUserId}\"')
        elif not utils.isValidStr(redemptionUserName):
            raise ValueError(f'redemptionUserName argument is malformed: \"{redemptionUserName}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif userInput is not None and not isinstance(userInput, str):
            raise ValueError(f'userInput argument is malformed: \"{userInput}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        # TODO
        pass
