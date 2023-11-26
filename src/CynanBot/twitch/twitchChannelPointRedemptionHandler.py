import CynanBot.misc.utils as utils
from CynanBot.pointRedemptions import (AbsPointRedemption, CutenessRedemption,
                                       PkmnBattleRedemption,
                                       PkmnCatchRedemption,
                                       PkmnEvolveRedemption,
                                       PkmnShinyRedemption,
                                       StubPointRedemption,
                                       SuperTriviaGameRedemption,
                                       TriviaGameRedemption)
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.absTwitchChannelPointRedemptionHandler import \
    AbsTwitchChannelPointRedemptionHandler
from CynanBot.twitch.twitchChannelPointsMessage import (
    TwitchChannelPointsMessage, TwitchChannelPointsMessageStub)
from CynanBot.twitch.twitchChannelProvider import TwitchChannelProvider
from CynanBot.twitch.websocket.websocketDataBundle import WebsocketDataBundle
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.userInterface import UserInterface


class TwitchChannelPointRedemptionHandler(AbsTwitchChannelPointRedemptionHandler):

    def __init__(
        self,
        cutenessRedemption: AbsPointRedemption,
        pkmnBattleRedemption: AbsPointRedemption,
        pkmnCatchRedemption: AbsPointRedemption,
        pkmnEvolveRedemption: AbsPointRedemption,
        pkmnShinyRedemption: AbsPointRedemption,
        superTriviaGameRedemption: AbsPointRedemption,
        triviaGameRedemption: AbsPointRedemption,
        timber: TimberInterface,
        twitchChannelProvider: TwitchChannelProvider,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(cutenessRedemption, CutenessRedemption) and not isinstance(cutenessRedemption, StubPointRedemption):
            raise ValueError(f'cutenessRedemption argument is malformed: \"{cutenessRedemption}\"')
        elif not isinstance(pkmnBattleRedemption, PkmnBattleRedemption) and not isinstance(pkmnBattleRedemption, StubPointRedemption):
            raise ValueError(f'pkmnBattleRedemption argument is malformed: \"{pkmnBattleRedemption}\"')
        elif not isinstance(pkmnCatchRedemption, PkmnCatchRedemption) and not isinstance(pkmnCatchRedemption, StubPointRedemption):
            raise ValueError(f'pkmnCatchRedemption argument is malformed: \"{pkmnCatchRedemption}\"')
        elif not isinstance(pkmnEvolveRedemption, PkmnEvolveRedemption) and not isinstance(pkmnEvolveRedemption, StubPointRedemption):
            raise ValueError(f'pkmnEvolveRedemption argument is malformed: \"{pkmnEvolveRedemption}\"')
        elif not isinstance(pkmnShinyRedemption, PkmnShinyRedemption) and not isinstance(pkmnShinyRedemption, StubPointRedemption):
            raise ValueError(f'pkmnShinyRedemption argument is malformed: \"{pkmnShinyRedemption}\"')
        elif not isinstance(superTriviaGameRedemption, SuperTriviaGameRedemption) and not isinstance(superTriviaGameRedemption, StubPointRedemption):
            raise ValueError(f'superTriviaGameRedemption argument is malformed: \"{superTriviaGameRedemption}\"')
        elif not isinstance(triviaGameRedemption, TriviaGameRedemption) and not isinstance(triviaGameRedemption, StubPointRedemption):
            raise ValueError(f'triviaGameRedemption argument is malformed: \"{triviaGameRedemption}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise ValueError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__cutenessRedemption: AbsPointRedemption = cutenessRedemption
        self.__pkmnBattleRedemption: AbsPointRedemption = pkmnBattleRedemption
        self.__pkmnCatchRedemption: AbsPointRedemption = pkmnCatchRedemption
        self.__pkmnEvolveRedemption: AbsPointRedemption = pkmnEvolveRedemption
        self.__pkmnShinyRedemption: AbsPointRedemption = pkmnShinyRedemption
        self.__superTriviaGameRedemption: AbsPointRedemption = superTriviaGameRedemption
        self.__triviaGameRedemption: AbsPointRedemption = triviaGameRedemption
        self.__timber: TimberInterface = timber
        self.__twitchChannelProvider: TwitchChannelProvider = twitchChannelProvider
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

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
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that has no event: \"{dataBundle}\"')
            return

        eventId = dataBundle.getMetadata().getMessageId()
        reward = event.getReward()
        redemptionUserId = event.getUserId()
        redemptionUserInput = event.getUserInput()
        redemptionUserLogin = event.getUserLogin()

        if not utils.isValidStr(eventId) or reward is None or not utils.isValidStr(redemptionUserId) or not utils.isValidStr(redemptionUserLogin):
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that is missing crucial data: ({eventId=}) ({reward=}) ({redemptionUserId=}) ({redemptionUserInput=}) ({redemptionUserLogin=})')
            return

        self.__timber.log('TwitchChannelPointRedemptionHandler', f'Channel point reward ({reward}) redeemed by {redemptionUserLogin}:{redemptionUserId} in {user.getHandle()}:{userId}')

        await self.__userIdsRepository.setUser(
            userId = redemptionUserId,
            userName = redemptionUserLogin
        )

        twitchChannel = await self.__twitchChannelProvider.getTwitchChannel(user.getHandle())

        channelPointsMessage: TwitchChannelPointsMessage = TwitchChannelPointsMessageStub(
            eventId = eventId,
            redemptionMessage = redemptionUserInput,
            rewardId = reward.getRewardId(),
            twitchUser = user,
            userId = redemptionUserId,
            userName = redemptionUserLogin
        )

        if user.isCutenessEnabled() and user.hasCutenessBoosterPacks():
            if await self.__cutenessRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isPkmnEnabled():
            if channelPointsMessage.getRewardId() == user.getPkmnBattleRewardId():
                if await self.__pkmnBattleRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

            if user.hasPkmnCatchBoosterPacks():
                if await self.__pkmnCatchRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

            if channelPointsMessage.getRewardId() == user.getPkmnEvolveRewardId():
                if await self.__pkmnEvolveRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

            if channelPointsMessage.getRewardId() == user.getPkmnShinyRewardId():
                if await self.__pkmnShinyRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

        if user.isTriviaGameEnabled() and channelPointsMessage.getRewardId() == user.getTriviaGameRewardId():
            if await self.__triviaGameRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isSuperTriviaGameEnabled() and channelPointsMessage.getRewardId() == user.getSuperTriviaGameRewardId():
            if await self.__superTriviaGameRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return
